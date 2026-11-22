#!/usr/bin/env python3
"""Bounded independent replay of the exact state-coordinate construction.

No solver, endpoint search, large enumeration, or timing inference.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import struct

ROOT = Path(__file__).resolve().parent
M = (1 << 32)-1


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name,ROOT/filename)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


c = load('parent_chart','chart.py')
r = load('independent_reference','reference.py')
f = load('joint_fibre_algebra','fibre_algebra.py')
s = load('state_coordinates','state_coordinates.py')


def pack(words): return struct.pack('>16I',*words)
def hx(words): return [f'{x:08x}' for x in words]


def main():
    data = json.loads((ROOT/'INPUTS.json').read_text())
    bound = json.loads((ROOT/'SOURCE_BINDINGS.json').read_text())
    for name,record in bound['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == record['sha256']
    fibres = {
        'p4_W14':f.fibre(2,1,0xF8010000,0xFFFD8000),
        'p4_W23':f.fibre(2,-1,0xF8010000,0xFFFD8000),
        'p1_W14':f.fibre(0,1,0x02004000,0xFFFF6000),
        'p1_W23':f.fibre(0,-1,0x02004000,0xFFFF6000),
    }
    N=(1<<27)+(1<<22)+(1<<19)
    assert fibres['p4_W14']['count']==fibres['p4_W23']['count']==1<<27
    assert fibres['p1_W14']['count']==fibres['p1_W23']['count']==N
    known=r.expand(pack([int(x,16) for x in data['retained_left']]))
    pub37=r.expand(bytes.fromhex(data['public_r37_left'])[64:])
    core4=[known[i] for i in (6,7,8,9,14,22,23)]
    core1=[pub37[i] for i in (6,7,8,9,14,22,23)]
    core1[-1]=int(data['r37_joint_W23_example'],16)
    first=bytes.fromhex(data['public_r38_common_first_block'])
    C39=r.compress(r.IV,first,39)[0]
    assert hx(C39)==data['expected_C39']
    entries=[('standard_IV',r.IV),('public_C39',C39),
             ('public_C40',r.compress(r.IV,first,40)[0])]
    rng=random.Random(2026110913)
    cases=0; inverses=0; contexts=[]; examples=[]
    for arm,base,diffs in [('p4',core4,c.DIFF_SHIFTED_R38),('p1',core1,c.DIFF_R37)]:
        comp14=[x['solution'] for x in fibres[arm+'_W14']['classes'] if x['count']]
        comp23=[x['solution'] for x in fibres[arm+'_W23']['classes'] if x['count']]
        for label,entry in entries:
            six=[rng.getrandbits(32) for _ in range(6)]
            seed=c.generate_preserving_S10(entry,base,diffs,six,[0,0,0])
            prefix=seed['left'][:10]
            expected_support=sorted([i for i,d in diffs.items() if d]+[37])
            delta37=(r.s0((base[5]+diffs[22])&M)-r.s0(base[5]))&M
            for group in range(2):
                outputs=[0,0,0] if group==0 else [rng.getrandbits(32) for _ in range(3)]
                saved_states=None; saved_diff14=None; seen13=set()
                for n in range(32):
                    V=f.sample_component(comp14[n%len(comp14)],rng)
                    Z=f.sample_component(comp23[(n//len(comp14))%len(comp23)],rng)
                    obj=s.generate_from_left_A(entry,prefix,base[5],V,Z,outputs,diffs)
                    L,R=obj['left'],obj['right']
                    _,tl,wl=r.compress(entry,pack(L),14)
                    _,tr,wr=r.compress(entry,pack(R),14)
                    assert [tl[t+1][0] for t in (10,11,12)]==outputs
                    assert tl[10]==obj['left_S10'] and tl[13]==obj['left_S13']
                    assert L[:10]==seed['left'][:10] and R[:10]==seed['right'][:10]
                    assert L[10:13]==R[10:13]==obj['common_W10_W12']
                    assert L[13]==R[13] and L[15]==R[15]
                    assert (wl[14],wl[22],wl[23])==(V,base[5],Z)
                    delta=[(b-a)&M for a,b in zip(wl[:39],wr[:39])]
                    assert [i for i,d in enumerate(delta) if d]==expected_support
                    assert all(delta[i]==d for i,d in diffs.items())
                    assert delta[37]==delta37 and delta37!=0 and wl[38]==wr[38]
                    if saved_states is None:
                        saved_states=(tl[:14],tr[:14])
                        saved_diff14=[(b-a)&M for a,b in zip(tl[14],tr[14])]
                    assert (tl[:14],tr[:14])==saved_states
                    assert [(b-a)&M for a,b in zip(tl[14],tr[14])]==saved_diff14
                    seen13.add(L[13])
                    # Round trip through the earlier, differently ordered chart.
                    old=c.generate_preserving_S10(entry,[prefix[i] for i in (6,7,8,9)]+[V,base[5],Z],
                                                   diffs,six,[L[10],L[11],L[13]])
                    assert old['left']==L and old['right']==R
                    assert s.Z_for_fixed_W13(prefix,base[5],V,L[10:13],L[13])==Z
                    if n==0 and group==0:
                        examples.append({'arm':arm,'entry':label,'entry_words':hx(entry),
                            'left_A10_A12':hx(outputs),'left_W0_W15':hx(L),'right_W0_W15':hx(R),
                            'S13_left':hx(tl[13]),'S13_right':hx(tr[13]),
                            'fixed_dS14':hx(saved_diff14),'fixed_W22':f'{base[5]:08x}',
                            'fixed_dW37':f'{delta37:08x}','support':expected_support,
                            'pair_sha256_be':hashlib.sha256(pack(L)+pack(R)).hexdigest()})
                    cases+=1
                contexts.append({'arm':arm,'entry':label,'left_A10_A12':hx(outputs),
                                 'joint_replays':32,'S13_pair_preserved':True,
                                 'dS14_preserved':True,'distinct_sample_W13':len(seen13)})
                # Round-trip the Z <-> W13 bijection without assuming late-fibre membership.
                # This is a bounded equation check, not a search for admissible roots.
                for _ in range(12):
                    V=rng.getrandbits(32); Z=rng.getrandbits(32); T=rng.getrandbits(32)
                    common3=obj['common_W10_W12']
                    left=s.complete_left(prefix,base[5],V,Z,common3)
                    forward=r.expand(pack(left))
                    assert forward[22]==base[5] and forward[23]==Z
                    assert s.Z_for_fixed_W13(prefix,base[5],V,common3,left[13])==Z
                    backZ=s.Z_for_fixed_W13(prefix,base[5],V,common3,T)
                    assert s.complete_left(prefix,base[5],V,backZ,common3)[13]==T
                    inverses+=1
    result={
        'status':'PASS','scope':'Exact state-oriented coordinate change and bounded early-state/schedule replay',
        'round_convention':'A_t is the new a output of round t, so A10=S11[a]',
        'admissible_pair_replays':cases,'unrestricted_Z_W13_inverse_checks':inverses,
        'fibre_counts':{key:val['count'] for key,val in fibres.items()},
        'entries':{key:hx(value) for key,value in entries},
        'contexts':contexts,'examples':examples,
        'exact_slice_counts':{'p4_S10_fixed':'2^150','p4_S13_fixed':'2^54',
                              'p1_S10_fixed':'N^2 * 2^96','p1_S13_fixed':'N^2',
                              'N':N},
        'S14_fibre_counting':{'p4_average_including_empty':1<<22,
                             'p1_average_including_empty':N*N//(1<<32),
                             'claim':'At least one W13 has at least the average count; no uniformity or extraction-cost assertion'},
        'not_claimed':['arbitrary right outputs','arbitrary differential outputs','late endpoint control',
                       'independent lane freedom','r39/r40 collision','efficient S14 large-fibre extraction',
                       'attack cost or probability','changes to frozen A/B/C']}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__': main()
