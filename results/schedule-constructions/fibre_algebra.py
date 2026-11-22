#!/usr/bin/env python3
"""Exact late-fibre algebra and bounded schedule/prefix replay; no endpoint search."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import struct

ROOT = Path(__file__).resolve().parent
M = (1 << 32) - 1


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


c = load('chart', 'chart.py')
r = load('reference', 'reference.py')


def gf2_solve(equations):
    rows = [mask | (rhs << 32) for mask, rhs in equations]
    rank = 0
    pivots = []
    for col in range(32):
        pivot = next((i for i in range(rank, len(rows)) if rows[i] & (1 << col)), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i] & (1 << col):
                rows[i] ^= rows[rank]
        pivots.append(col)
        rank += 1
    if any((row & M) == 0 and row >> 32 for row in rows):
        return None
    particular = sum(((rows[i] >> 32) & 1) << p for i, p in enumerate(pivots))
    basis = []
    for free in sorted(set(range(32)) - set(pivots)):
        vector = 1 << free
        for i, pivot in enumerate(pivots):
            if rows[i] & (1 << free):
                vector ^= 1 << pivot
        basis.append(vector)
    return {'rank': rank, 'dimension': 32-rank, 'particular': particular,
            'basis': basis, 'count': 1 << (32-rank)}


def fibre(power, sign, target0, target1):
    """Complete disjoint carry/borrow classes for +/-2^power."""
    maps = [(r.s0, target0), (r.s1, target1)]
    columns = [[fn(1 << j) for j in range(32)] for fn, _ in maps]
    classes = []
    for stop in list(range(power, 32)) + [None]:
        equations = []
        last = 31 if stop is None else stop
        for bit in range(power, last+1):
            if stop is None or bit < stop:
                value = 1 if sign == 1 else 0
            else:
                value = 0 if sign == 1 else 1
            equations.append((1 << bit, value))
        input_mask = (((1 << (last+1)) - 1) ^ ((1 << power) - 1)) & M
        rejected = False
        for (fn, target), cols in zip(maps, columns):
            output_mask = fn(input_mask)
            twice_masked = (output_mask - target) & M
            if twice_masked & 1:
                rejected = True
                break
            masked_low = twice_masked >> 1
            if masked_low & (~output_mask) & 0x7FFFFFFF:
                rejected = True
                break
            for bit in range(31):
                if output_mask & (1 << bit):
                    mask = sum(((cols[j] >> bit) & 1) << j for j in range(32))
                    equations.append((mask, (masked_low >> bit) & 1))
        solution = None if rejected else gf2_solve(equations)
        classes.append({'stop_bit': stop, 'input_xor_mask': f'{input_mask:08x}',
                        'solution': solution, 'count': 0 if solution is None else solution['count']})
    return {'power': power, 'sign': sign, 'target0': f'{target0:08x}',
            'target1': f'{target1:08x}', 'classes': classes,
            'count': sum(cls['count'] for cls in classes)}


def sample_component(component, rng):
    x = component['particular']
    for v in component['basis']:
        if rng.getrandbits(1):
            x ^= v
    return x


def pack(words):
    return struct.pack('>16I', *words)


def hx(words):
    return [f'{x:08x}' for x in words]


def main():
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    fibres = {
        'p4_W14': fibre(2, 1, 0xF8010000, 0xFFFD8000),
        'p4_W23': fibre(2, -1, 0xF8010000, 0xFFFD8000),
        'p1_W14': fibre(0, 1, 0x02004000, 0xFFFF6000),
        'p1_W23': fibre(0, -1, 0x02004000, 0xFFFF6000),
    }
    N = (1 << 27) + (1 << 22) + (1 << 19)
    assert fibres['p4_W14']['count'] == fibres['p4_W23']['count'] == 1 << 27
    assert fibres['p1_W14']['count'] == fibres['p1_W23']['count'] == N
    for key, f in fibres.items():
        dimensions = [cl['solution']['dimension'] for cl in f['classes'] if cl['count']]
        assert dimensions == ([27] if key.startswith('p4') else [27, 22, 19])
    rng = random.Random(2026110912)
    membership_checks = 0
    for key, f in fibres.items():
        delta = (f['sign'] * (1 << f['power'])) & M
        for cl in f['classes']:
            if not cl['count']:
                continue
            solution = cl['solution']
            values = [solution['particular']]
            values += [solution['particular'] ^ v for v in solution['basis']]
            values += [sample_component(solution, rng) for _ in range(12)]
            for x in values:
                assert ((x+delta)&M) ^ x == int(cl['input_xor_mask'], 16)
                assert (r.s0((x+delta)&M) - r.s0(x)) & M == int(f['target0'], 16)
                assert (r.s1((x+delta)&M) - r.s1(x)) & M == int(f['target1'], 16)
                membership_checks += 1
    first = bytes.fromhex(inputs['public_r38_common_first_block'])
    entries = [('standard_IV', r.IV),
               ('public_C39', r.compress(r.IV, first, 39)[0]),
               ('public_C40', r.compress(r.IV, first, 40)[0])]
    known = r.expand(pack([int(x,16) for x in inputs['retained_left']]))
    public37 = r.expand(bytes.fromhex(inputs['public_r37_left'])[64:])
    core4 = [known[i] for i in (6,7,8,9,14,22,23)]
    core1 = [public37[i] for i in (6,7,8,9,14,22,23)]
    core1[-1] = int(inputs['r37_joint_W23_example'],16)
    cases = 0
    contexts = []
    for arm, base_core, differences in [('p4',core4,c.DIFF_SHIFTED_R38),('p1',core1,c.DIFF_R37)]:
        f14 = fibres[arm+'_W14']; f23 = fibres[arm+'_W23']
        comp14 = [cl['solution'] for cl in f14['classes'] if cl['count']]
        comp23 = [cl['solution'] for cl in f23['classes'] if cl['count']]
        for label, entry in entries:
            six = [rng.getrandbits(32) for _ in range(6)]
            seed = c.generate_preserving_S10(entry,base_core,differences,six,[0,0,0])
            _, tl, _ = r.compress(entry,pack(seed['left']),10)
            _, tr, _ = r.compress(entry,pack(seed['right']),10)
            fixed_delta = (r.s0((base_core[5]+differences[22])&M)-r.s0(base_core[5]))&M
            assert fixed_delta != 0
            for n in range(64):
                core = list(base_core)
                core[4] = sample_component(comp14[n % len(comp14)],rng)
                core[6] = sample_component(comp23[(n // len(comp14)) % len(comp23)],rng)
                free = [rng.getrandbits(32) for _ in range(3)]
                generated = c.generate_preserving_S10(entry,core,differences,six,free)
                L,R = generated['left'],generated['right']
                assert L[:10] == seed['left'][:10] and R[:10] == seed['right'][:10]
                _, tl2, wl = r.compress(entry,pack(L),10)
                _, tr2, wr = r.compress(entry,pack(R),10)
                assert tl2==tl and tr2==tr
                assert wl[22] == base_core[5] and wr[22] == (base_core[5]+differences[22])&M
                delta = [(b-a)&M for a,b in zip(wl[:39],wr[:39])]
                assert [i for i,d in enumerate(delta) if d] == sorted([i for i,d in differences.items() if d]+[37])
                assert all(delta[i] == d for i,d in differences.items())
                assert delta[37] == fixed_delta and wl[38] == wr[38]
                assert (wl[14],wl[23],L[10],L[11],L[13]) == (core[4],core[6],*free)
                cases += 1
            contexts.append({'arm':arm,'entry':label,'fixed_left_prefix_W0_W9':hx(seed['left'][:10]),
                             'fixed_right_prefix_W0_W9':hx(seed['right'][:10]),
                             'fixed_W22_left':f'{base_core[5]:08x}','fixed_dW37':f'{fixed_delta:08x}',
                             'S10_left':hx(tl[10]),'S10_right':hx(tr[10]),'cases':64})
    result = {
        'status':'PASS','scope':'Exact fixed-prefix-and-W22 schedule slice; no endpoint search or solver',
        'parent_archive_sha256':'54d6d151e9eeca958ce3d3ed6e2969b5998670bee95dddec9361064491a92e05',
        'method':'Complete disjoint carry/borrow classes; exact GF(2) solving; bounded forward schedule/state replay',
        'fibre_results':fibres,'scalar_membership_checks':membership_checks,
        'completion_replay_cases':cases,'contexts':contexts,
        'slice_counts':{'p4':'2^150','p1':'(2^27+2^22+2^19)^2 * 2^96 = 70225 * 2^134',
                        'p1_log2':96+2*math.log2(N)},
        'invariants':['actual entry','both W0..W9 prefixes','both S10 states','absolute W22','derived dW37','declared support and numerical differences'],
        'released':['left absolute W14 within J14','left absolute W23 within J23','common W10,W11,W13'],
        'repairs':['common W15','common W12'],
        'not_claimed':['new total family cardinality','late state equalities','endpoint probability','independent lanes','solver speedup','attack-cost improvement'],
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
