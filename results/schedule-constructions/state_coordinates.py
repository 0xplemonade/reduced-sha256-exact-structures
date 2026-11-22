"""Exact state-oriented coordinates for the retained paired schedule slices.

A_t means the new a output of round t, so A_10 is S_11[a].
This module constructs schedules and early states; it performs no search.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('construction_chart', ROOT / 'chart.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
M = (1 << 32) - 1
K13 = tuple(int(s, 16) for s in '''
428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1
923f82a4 ab1c5ed5 d807aa98 12835b01 243185be 550c7dc3 72be5d74
'''.split())


def left_prefix_state(entry, prefix):
    state = list(entry)
    for i, word in enumerate(prefix):
        a,b,cc,d,e,f,g,h = state
        t1 = (h+c.big1(e)+c.ch(e,f,g)+K13[i]+word) & M
        t2 = c.T(a,b,cc)
        state = [(t1+t2)&M,a,b,cc,(d+t1)&M,e,f,g]
    return state


def words_for_left_outputs(s10, outputs):
    """Bijection from three desired LEFT A outputs to common W10..W12."""
    if len(outputs) != 3:
        raise ValueError('expected A10,A11,A12')
    state = list(s10)
    words = []
    for t, target in zip(range(10,13), outputs):
        a,b,cc,d,e,f,g,h = state
        t1 = (target-c.T(a,b,cc)) & M
        word = (t1-h-c.big1(e)-c.ch(e,f,g)-K13[t]) & M
        words.append(word)
        state = [target,a,b,cc,(d+t1)&M,e,f,g]
    return words, state


def complete_left(prefix10, U, V, Z, common3):
    """All Z are admitted here; paired admissibility is checked by build_pair.

    Free actual word coordinates W10,W11,W12; solve W13,W15.
    U=W22_left, V=W14_left, Z=W23_left.
    """
    if len(prefix10) != 10 or len(common3) != 3:
        raise ValueError('wrong coordinate dimensions')
    w = list(prefix10)+list(common3)+[None,V,None]
    w16 = (c.small1(V)+w[9]+c.small0(w[1])+w[0]) & M
    w21 = c.inv1((Z-w16-c.small0(w[8])-w[7]) & M)
    w19 = c.inv1((w21-V-c.small0(w[6])-w[5]) & M)
    w17 = c.inv1((w19-w[12]-c.small0(w[4])-w[3]) & M)
    w[15] = c.inv1((w17-w[10]-c.small0(w[2])-w[1]) & M)
    w20 = c.inv1((U-w[15]-c.small0(w[7])-w[6]) & M)
    w18 = (c.small1(w16)+w[11]+c.small0(w[3])+w[2]) & M
    w[13] = (w20-c.small1(w18)-c.small0(w[5])-w[4]) & M
    return w


def build_pair(prefix10, U, V, Z, common3, differences):
    core = [prefix10[i] for i in (6,7,8,9)]+[V,U,Z]
    if any(c.core7_residuals(core, differences)):
        raise ValueError('inadmissible fixed context or late fibre coordinates')
    left = complete_left(prefix10,U,V,Z,common3)
    right = list(left)
    for i in (6,7,8,9,14):
        right[i] = (right[i]+differences[i]) & M
    return left, right


def generate_from_left_A(entry, prefix10, U, V, Z, outputs, differences):
    s10 = left_prefix_state(entry,prefix10)
    common3, s13 = words_for_left_outputs(s10,outputs)
    left,right = build_pair(prefix10,U,V,Z,common3,differences)
    return {'left':left,'right':right,'common_W10_W12':common3,
            'left_S10':s10,'left_S13':s13,'left_A10_A12':list(outputs)}


def Z_for_fixed_W13(prefix10, U, V, common3, T):
    """The explicit one-word conditional map H_T(V) for S14 preservation.

    No assumption of injectivity as a function of V is made.
    At fixed V this is the inverse of Z -> common W13.
    """
    w = list(prefix10)+list(common3)+[T,V,None]
    w16 = (c.small1(V)+w[9]+c.small0(w[1])+w[0]) & M
    w18 = (c.small1(w16)+w[11]+c.small0(w[3])+w[2]) & M
    w20 = (c.small1(w18)+T+c.small0(w[5])+w[4]) & M
    w[15] = (U-c.small1(w20)-c.small0(w[7])-w[6]) & M
    w17 = (c.small1(w[15])+w[10]+c.small0(w[2])+w[1]) & M
    w19 = (c.small1(w17)+w[12]+c.small0(w[4])+w[3]) & M
    w21 = (c.small1(w19)+V+c.small0(w[6])+w[5]) & M
    Z = (c.small1(w21)+w16+c.small0(w[8])+w[7]) & M
    return Z
