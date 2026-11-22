#!/usr/bin/env python3
"""Bounded checks of a proved identity; not a solver or endpoint search.

Six retained schedule fixtures are re-expanded and replayed independently.
All other contexts/inputs are labelled algebra-only, without admissibility.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import struct

ROOT = Path(__file__).resolve().parent
M = 0xffffffff


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


n = load('local_normal_form', 'normal_form.py')
r = load('bound_forward_reference', 'reference.py')


def hx(seq):
    return [f'{x:08x}' for x in seq]


def inverse_small0():
    # Independent exact GF(2) inversion, checked on a basis in both directions.
    rows = [sum(((r.s0(1<<j)>>i)&1)<<j for j in range(32)) | (1<<(32+i))
            for i in range(32)]
    for j in range(32):
        pivot = next(i for i in range(j,32) if (rows[i]>>j)&1)
        rows[j],rows[pivot] = rows[pivot],rows[j]
        for i in range(32):
            if i!=j and (rows[i]>>j)&1:
                rows[i] ^= rows[j]
    assert [x&M for x in rows] == [1<<i for i in range(32)]
    invrows = [x>>32 for x in rows]
    def inv(v):
        return sum(((v&row).bit_count()&1)<<i for i,row in enumerate(invrows))
    for i in range(32):
        assert inv(r.s0(1<<i)) == 1<<i
        assert r.s0(inv(1<<i)) == 1<<i
    return inv


def check_one(ctx, v):
    key, origin, cp, cq = n.representation(ctx)
    p, q = n.direct(ctx, v)
    pn, qn = n.normalized(key, (v+origin)&M)
    assert (p, q) == ((pn+cp)&M, (qn+cq)&M)
    return key, origin, cp, cq


def main():
    bindings = json.loads((ROOT/'SOURCE_BINDINGS.json').read_text())
    for name, info in bindings.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == info['sha256']
    rng = random.Random(0x391540)
    examples = json.loads((ROOT/'INPUTS.json').read_text())['examples']
    inv0 = inverse_small0()
    records = []
    for ex in examples:
        ll = [int(x,16) for x in ex['left_W0_W15']]
        rr = [int(x,16) for x in ex['right_W0_W15']]
        entry = [int(x,16) for x in ex['entry_words']]
        lb, rb = struct.pack('>16I',*ll), struct.pack('>16I',*rr)
        assert hashlib.sha256(lb+rb).hexdigest() == ex['pair_sha256_be']
        _, tl, wl = r.compress(entry, lb, 16)
        _, tr, wr = r.compress(entry, rb, 16)
        dw = [(b-a)&M for a,b in zip(wl,wr)]
        assert [i for i in range(39) if dw[i]] == ex['support']
        assert wl[22] == int(ex['fixed_W22'],16)
        assert dw[37] == int(ex['fixed_dW37'],16)
        assert wl[38] == wr[38]
        recovered_v = inv0((wl[29]-r.s1(wl[27])-wl[22]-ll[13])&M)
        assert recovered_v == ll[14]
        fixed = ({6:0x31de0240,7:0xfffffffc,9:0x00028000,14:4,
                  22:0x07ff0000,23:0xfffffffc} if ex['arm']=='p4' else
                 {6:0xf7d2c329,7:0xfd3be488,8:0xd0007c70,9:0x0000a000,
                  14:1,22:0xfdffc000,23:0xffffffff})
        assert all(dw[i] == d for i,d in fixed.items())
        v = ll[14]
        ctx = n.from_s15(tl[15], tr[15], v)
        key, origin, cp, cq = check_one(ctx,v)
        p,q = n.direct(ctx,v)
        delta = [(b-a)&M for a,b in zip(tl[15],tr[15])]
        predicted = [(p+q)&M,delta[0],delta[1],delta[2],
                     (delta[3]+q)&M,delta[4],delta[5],delta[6]]
        assert predicted == [(b-a)&M for a,b in zip(tl[16],tr[16])]
        records.append({'arm':ex['arm'],'entry':ex['entry'],
                        'key':hx(key),'origin':f'{origin:08x}',
                        'output_offsets':hx((cp,cq)),
                        'P_Q':hx((p,q)),
                        'V_recovered_from_W27_W29':f'{recovered_v:08x}',
                        'status':'PASS'})
    arbitrary = 0
    translations = 0
    for i in range(2048):
        ctx = {k:rng.getrandbits(32) for k in (
            'alpha_l','alpha_r','beta_l','beta_r','b_l','c_l','b_r','c_r',
            'f_l','g_l','f_r','g_r','delta_h')}
        v = [0,M,0x80000000,0x7fffffff][i%4] if i<16 else rng.getrandbits(32)
        key,origin,cp,cq = check_one(ctx,v)
        arbitrary += 1
        if i<256:
            shift = rng.getrandbits(32)
            shifted = dict(ctx)
            for label in ('alpha_l','alpha_r','beta_l','beta_r'):
                shifted[label] = (shifted[label]-shift)&M
            key2,origin2,cp2,cq2 = check_one(shifted,(v+shift)&M)
            assert (key,cp,cq) == (key2,cp2,cq2)
            assert n.direct(ctx,v) == n.direct(shifted,(v+shift)&M)
            translations += 1
    result = {
        'status':'PASS', 'admissible_fixture_replays':len(records),
        'arbitrary_context_identity_checks':arbitrary,
        'synthetic_input_origin_covariance_checks':translations,
        'row29_inverse_coordinate_checks':len(records),
        'small_sigma0_inverse_two_sided_basis_checks':64,
        'fixtures':records,
        'key_semantics':'Sufficient representation of the normalized unrestricted immediate map; not a minimal classification.',
        'scope':{
            'fixtures':'Genuine retained schedules, complete expansion through W38 and state replay through S16.',
            'arbitrary_contexts':'Algebra identity only; schedule admissibility is not asserted.',
            'origin_shifts':'Synthetic coordinate changes only; no reachable-context or domain equivalence is asserted.',
            'excluded_claims':['endpoint witness','endpoint probability','independent lanes','cross-context admissible-fibre reuse','speedup','Yukon cost']},
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
