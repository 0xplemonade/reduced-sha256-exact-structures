#!/usr/bin/env python3
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
MASK = (1 << 32) - 1
IV = (
    0x6A09E667,
    0xBB67AE85,
    0x3C6EF372,
    0xA54FF53A,
    0x510E527F,
    0x9B05688C,
    0x1F83D9AB,
    0x5BE0CD19,
)
K = tuple(
    int(value, 16)
    for value in """
428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967
27b70a85 2e1b2138 4d2c6dfc 53380d13 650a7354 766a0abb 81c2c92e 92722c85
""".split()
)


def rotate_right(value, count):
    return ((value >> count) | (value << (32 - count))) & MASK


def small_sigma0(value):
    return rotate_right(value, 7) ^ rotate_right(value, 18) ^ (value >> 3)


def small_sigma1(value):
    return rotate_right(value, 17) ^ rotate_right(value, 19) ^ (value >> 10)


def big_sigma0(value):
    return rotate_right(value, 2) ^ rotate_right(value, 13) ^ rotate_right(value, 22)


def big_sigma1(value):
    return rotate_right(value, 6) ^ rotate_right(value, 11) ^ rotate_right(value, 25)


def choose(x, y, z):
    return (x & y) ^ ((~x) & z)


def majority(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def expand(seed):
    words = list(seed)
    for index in range(16, 40):
        words.append(
            (
                words[index - 16]
                + small_sigma0(words[index - 15])
                + words[index - 7]
                + small_sigma1(words[index - 2])
            )
            & MASK
        )
    return words


def step(state, word, index):
    a, b, c, d, e, f, g, h = state
    first = (h + big_sigma1(e) + choose(e, f, g) + K[index] + word) & MASK
    second = (big_sigma0(a) + majority(a, b, c)) & MASK
    return (
        (first + second) & MASK,
        a,
        b,
        c,
        (d + first) & MASK,
        e,
        f,
        g,
    )


def main():
    cores = json.loads((ROOT / "CORES.json").read_text())
    witnesses = json.loads((ROOT / "WITNESSES.json").read_text())["witnesses"]
    for row in witnesses:
        core = cores[row["ci"]]
        left = row["left"]
        right = row["right"]
        assert expand(left[:16]) == left
        assert expand(right[:16]) == right
        assert [i for i, (a, b) in enumerate(zip(left, right)) if a != b] == core["support"]
        left_trace = [IV]
        right_trace = [IV]
        for index in range(40):
            left_trace.append(step(left_trace[-1], left[index], index))
            right_trace.append(step(right_trace[-1], right[index], index))
        t = core["t"]
        assert list(left_trace[t]) == row["state_l"]
        assert list(right_trace[t]) == row["state_r"]
        assert list(left_trace[t + 1]) == row["next_l"]
        assert list(right_trace[t + 1]) == row["next_r"]
        assert list(left_trace[-1]) == row["final_l"]
        assert list(right_trace[-1]) == row["final_r"]
        left_state = left_trace[t]
        right_state = right_trace[t]
        left_operands = (
            left_state[7],
            big_sigma1(left_state[4]),
            choose(*left_state[4:7]),
            K[t],
            left[t],
            big_sigma0(left_state[0]),
            majority(*left_state[:3]),
        )
        right_operands = (
            right_state[7],
            big_sigma1(right_state[4]),
            choose(*right_state[4:7]),
            K[t],
            right[t],
            big_sigma0(right_state[0]),
            majority(*right_state[:3]),
        )
        left_carry = right_carry = 0
        sigma = []
        kappa = [0]
        beta = []
        for bit in range(32):
            left_sum = sum(value >> bit & 1 for value in left_operands)
            right_sum = sum(value >> bit & 1 for value in right_operands)
            sigma.append(right_sum - left_sum)
            beta.append(((right_sum + right_carry) & 1) - ((left_sum + left_carry) & 1))
            left_carry = (left_sum + left_carry) >> 1
            right_carry = (right_sum + right_carry) >> 1
            kappa.append(right_carry - left_carry)
            assert beta[-1] == sigma[-1] + kappa[-2] - 2 * kappa[-1]
        assert sigma == row["sigma"]
        assert kappa == row["kappa"]
        assert beta == row["beta"]
        b0 = (right_state[0] - left_state[0] + core["delta"][core["last"]]) & MASK
        b1 = (right_trace[t + 1][0] - left_trace[t + 1][0]) & MASK
        assert (b0, b1) == (row["B0"], row["B1"])
        assert not (b0 & 1023) and not (b1 & 1023)
        assert sigma[8] + kappa[8] == 2 * kappa[9]
        assert sigma[9] + kappa[9] == 0 and kappa[10] == 0

    local_cases = 0
    for left_sum in range(8):
        for right_sum in range(8):
            for left_carry in range(7):
                for right_carry in range(7):
                    sigma = right_sum - left_sum
                    kappa = right_carry - left_carry
                    beta = ((right_sum + right_carry) & 1) - ((left_sum + left_carry) & 1)
                    next_kappa = (right_sum + right_carry) // 2 - (left_sum + left_carry) // 2
                    assert beta == sigma + kappa - 2 * next_kappa
                    if (sigma + kappa) % 2 == 0:
                        assert beta == 0
                        assert next_kappa == (sigma + kappa) // 2
                    local_cases += 1

    print(
        json.dumps(
            {
                "status": "PASS",
                "witnesses_replayed": len(witnesses),
                "local_theorem_cases": local_cases,
                "transfer_and_reset_verified": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
