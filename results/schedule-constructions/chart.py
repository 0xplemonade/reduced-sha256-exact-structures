"""Exact reachable-S6 coordinates for the shifted-r38 compensated family.

All words are uint32. This module constructs schedules, not collisions.
"""
M = (1 << 32) - 1
K6 = (0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1)
CORE_POS = (6, 7, 9, 14, 22, 23)
DIFF = {6: 0x31DE0240, 7: 0xFFFFFFFC, 9: 0x00028000,
        14: 4, 22: 0x07FF0000, 23: 0xFFFFFFFC}


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & M


def small0(x):
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def small1(x):
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def big0(x):
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def big1(x):
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def ch(e, f, g):
    return (e & f) ^ ((~e) & g)


def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def T(a, b, c):
    return (big0(a) + maj(a, b, c)) & M


def _inverse_rows(fn):
    columns = [fn(1 << j) for j in range(32)]
    rows = [sum(((columns[j] >> i) & 1) << j for j in range(32))
            | (1 << (32 + i)) for i in range(32)]
    for col in range(32):
        pivot = next(i for i in range(col, 32) if (rows[i] >> col) & 1)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for i in range(32):
            if i != col and ((rows[i] >> col) & 1):
                rows[i] ^= rows[col]
    assert all((rows[i] & M) == (1 << i) for i in range(32))
    return tuple(row >> 32 for row in rows)


INV0_ROWS = _inverse_rows(small0)
INV1_ROWS = _inverse_rows(small1)


def inv0(y):
    return sum(((row & y).bit_count() & 1) << i
               for i, row in enumerate(INV0_ROWS))


def inv1(y):
    return sum(((row & y).bit_count() & 1) << i
               for i, row in enumerate(INV1_ROWS))


DIFF_R37 = {6: 0xF7D2C329, 7: 0xFD3BE488, 8: 0xD0007C70,
            9: 0x0000A000, 14: 1, 22: 0xFDFFC000, 23: 0xFFFFFFFF}
DIFF_SHIFTED_R38 = dict(DIFF)
DIFF_SHIFTED_R38[8] = 0


def core7_residuals(core, differences):
    """Admitted core when W8 is also fixed (active or common)."""
    w = dict(zip((6, 7, 8, 9, 14, 22, 23), core))
    d = differences
    D = lambda fn, i: derivative(fn, w[i], d[i])
    return [
        (D(small1, 14) + d[9]) & M,
        (d[14] + D(small0, 6)) & M,
        (D(small0, 7) + d[6] - d[22]) & M,
        (D(small0, 8) + d[7] - d[23]) & M,
        (D(small1, 22) + D(small0, 9) + d[8]) & M,
        (D(small1, 23) + d[9]) & M,
        (d[22] + D(small0, 14)) & M,
        (d[23] + d[14]) & M,
        (D(small0, 23) + d[22]) & M,
    ]


def derivative(fn, x, delta):
    return (fn((x + delta) & M) - fn(x)) & M


def core_residuals(core):
    w6, w7, w9, w14, w22, w23 = core
    return [
        (derivative(small0, w6, DIFF[6]) - DIFF[7]) & M,
        (derivative(small0, w7, DIFF[7]) - 0xD620FDC0) & M,
        (derivative(small1, w14, 4) - 0xFFFD8000) & M,
        (derivative(small0, w14, 4) - 0xF8010000) & M,
        (derivative(small1, w22, DIFF[22])
         + derivative(small0, w9, DIFF[9])) & M,
        (derivative(small1, w23, DIFF[23]) - 0xFFFD8000) & M,
        (derivative(small0, w23, DIFF[23]) - 0xF8010000) & M,
    ]


def s6_from_first_six(entry, six):
    """Choose S6 a..f freely; derive its exact reachable g,h."""
    a, b, c, d, e, f = six
    A1 = (e - a + T(b, c, d)) & M
    A0 = (f - b + T(c, d, A1)) & M
    g = (entry[0] + c - T(d, A1, A0)) & M
    h = (entry[1] + d - T(A1, A0, entry[0])) & M
    return list(six) + [g, h], [A0, A1, d, c, b, a]


def s6_is_reachable(entry, state):
    wanted, _ = s6_from_first_six(entry, state[:6])
    return wanted == list(state)


def prefix_from_A(entry, outputs):
    """Invert each round's unit-coefficient dependence on its message word."""
    state = list(entry)
    words = []
    for i, A in enumerate(outputs):
        a, b, c, d, e, f, g, h = state
        t2 = T(a, b, c)
        t1 = (A - t2) & M
        words.append((t1 - h - big1(e) - ch(e, f, g) - K6[i]) & M)
        state = [A, a, b, c, (d + t1) & M, e, f, g]
    return words, state


def complete_from_prefix(core, prefix, later):
    """Free W0..5,W10..13; solve W15 then W8, preserving the core."""
    if len(core) != 6 or any(core_residuals(core)):
        raise ValueError("inadmissible six-word core")
    if len(prefix) != 6 or len(later) != 4:
        raise ValueError("wrong coordinate dimensions")
    w = [None] * 16
    w[:6] = prefix
    w[10:14] = later
    w[6], w[7], w[9], w[14], U, V = core
    w16 = (small1(w[14]) + w[9] + small0(w[1]) + w[0]) & M
    w18 = (small1(w16) + w[11] + small0(w[3]) + w[2]) & M
    w20 = (small1(w18) + w[13] + small0(w[5]) + w[4]) & M
    w[15] = (U - small1(w20) - small0(w[7]) - w[6]) & M
    w17 = (small1(w[15]) + w[10] + small0(w[2]) + w[1]) & M
    w19 = (small1(w17) + w[12] + small0(w[4]) + w[3]) & M
    w21 = (small1(w19) + w[14] + small0(w[6]) + w[5]) & M
    w[8] = inv0((V - small1(w21) - w16 - w[7]) & M)
    right = list(w)
    for i in (6, 7, 9, 14):
        right[i] = (right[i] + DIFF[i]) & M
    return w, right


def generate(entry, core, six, later):
    """Six free S6 words plus four free later common message words."""
    if len(entry) != 8 or len(six) != 6:
        raise ValueError("wrong state dimensions")
    if any(not 0 <= x <= M for x in (*entry, *core, *six, *later)):
        raise ValueError("coordinates must be uint32")
    s6, outputs = s6_from_first_six(entry, six)
    prefix, reconstructed_s6 = prefix_from_A(entry, outputs)
    assert reconstructed_s6 == s6
    left, right = complete_from_prefix(core, prefix, later)
    return {"left": left, "right": right, "S6": s6, "A0_A5": outputs}


def generate_preserving_S10(entry, core7, differences, six, later3):
    """W8 is fixed; free W10,W11,W13; repair W15 then W12."""
    if len(core7) != 7 or any(core7_residuals(core7, differences)):
        raise ValueError('inadmissible seven-word core')
    if len(later3) != 3:
        raise ValueError('expected W10,W11,W13')
    if len(entry) != 8 or len(six) != 6:
        raise ValueError('wrong state dimensions')
    if any(not 0 <= x <= M for x in (*entry, *core7, *six, *later3)):
        raise ValueError('coordinates must be uint32')
    if differences not in (DIFF_R37, DIFF_SHIFTED_R38):
        raise ValueError('unsupported numerical core differences')
    s6, outputs = s6_from_first_six(entry, six)
    prefix, expected_s6 = prefix_from_A(entry, outputs)
    assert expected_s6 == s6
    w = [None] * 16
    w[:6] = prefix
    w[6], w[7], w[8], w[9], w[14], U, V = core7
    w[10], w[11], w[13] = later3
    w16 = (small1(w[14]) + w[9] + small0(w[1]) + w[0]) & M
    w18 = (small1(w16) + w[11] + small0(w[3]) + w[2]) & M
    w20 = (small1(w18) + w[13] + small0(w[5]) + w[4]) & M
    w[15] = (U - small1(w20) - small0(w[7]) - w[6]) & M
    w17 = (small1(w[15]) + w[10] + small0(w[2]) + w[1]) & M
    w21 = inv1((V - w16 - small0(w[8]) - w[7]) & M)
    w19 = inv1((w21 - w[14] - small0(w[6]) - w[5]) & M)
    w[12] = (w19 - small1(w17) - small0(w[4]) - w[3]) & M
    right = list(w)
    for i in (6, 7, 8, 9, 14):
        right[i] = (right[i] + differences[i]) & M
    return {'left': w, 'right': right, 'S6': s6, 'A0_A5': outputs}
