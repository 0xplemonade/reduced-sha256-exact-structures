"""Exact local P,Q normalization. No admissibility or endpoint claim."""

M = 0xffffffff


def rotr(x, n):
    return ((x >> n) | (x << (32-n))) & M


def sigma0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def sigma1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def maj(x, b, c):
    return (x & b) ^ (x & c) ^ (b & c)


def ch(x, f, g):
    return (x & f) ^ ((~x) & g)


def direct(ctx, v):
    al = (v + ctx['alpha_l']) & M
    ar = (v + ctx['alpha_r']) & M
    el = (v + ctx['beta_l']) & M
    er = (v + ctx['beta_r']) & M
    p = (sigma0(ar) + maj(ar, ctx['b_r'], ctx['c_r'])
         - sigma0(al) - maj(al, ctx['b_l'], ctx['c_l'])) & M
    q = (ctx['delta_h'] + sigma1(er) + ch(er, ctx['f_r'], ctx['g_r'])
         - sigma1(el) - ch(el, ctx['f_l'], ctx['g_l'])) & M
    return p, q


def representation(ctx):
    """Sufficient function key, input offset, and two output offsets.

    This is not a minimal/iff classification of functions. The admitted domain
    and all later schedule data are deliberately outside this local object.
    """
    key = (
        (ctx['alpha_r']-ctx['alpha_l']) & M,
        (ctx['beta_r']-ctx['beta_l']) & M,
        (ctx['beta_l']-ctx['alpha_l']) & M,
        ctx['b_l'] ^ ctx['c_l'], ctx['b_r'] ^ ctx['c_r'],
        ctx['f_l'] & ~ctx['g_l'], ~ctx['f_l'] & ctx['g_l'],
        ctx['f_r'] & ~ctx['g_r'], ~ctx['f_r'] & ctx['g_r'],
    )
    cp = ((ctx['b_r'] & ctx['c_r'])-(ctx['b_l'] & ctx['c_l'])) & M
    cq = (ctx['delta_h'] + ctx['g_r']-ctx['g_l']) & M
    return key, ctx['alpha_l'], cp, cq


def normalized(key, x):
    da, de, kappa, ml, mr, rl, sl, rr, sr = key
    xd = (x+da) & M
    y = (x+kappa) & M
    yd = (y+de) & M
    p = (sigma0(xd)-sigma0(x)+(xd & mr)-(x & ml)) & M
    q = (sigma1(yd)-sigma1(y)+(yd & rr)-(yd & sr)
         -(y & rl)+(y & sl)) & M
    return p, q


def from_s15(left, right, v):
    return {
        'alpha_l': (left[0]-v) & M, 'alpha_r': (right[0]-v) & M,
        'beta_l': (left[4]-v) & M, 'beta_r': (right[4]-v) & M,
        'b_l':left[1], 'c_l':left[2], 'b_r':right[1], 'c_r':right[2],
        'f_l':left[5], 'g_l':left[6], 'f_r':right[5], 'g_r':right[6],
        'delta_h':(right[7]-left[7]) & M,
    }
