
import hashlib, json, struct
M=(1<<32)-1
IV=[int(v,16) for v in '6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19'.split()]
K=[int(v,16) for v in '''428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5 d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174 e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da 983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967 27b70a85 2e1b2138 4d2c6dfc 53380d13 650a7354 766a0abb 81c2c92e 92722c85 a2bfe8a1 a81a664b c24b8b70 c76c51a3 d192e819 d6990624 f40e3585 106aa070 19a4c116 1e376c08 2748774c 34b0bcb5 391c0cb3 4ed8aa4a 5b9cca4f 682e6ff3 748f82ee 78a5636f 84c87814 8cc70208 90befffa a4506ceb bef9a3f7 c67178f2'''.split()]
def rr(x,n): return ((x>>n)|(x<<(32-n)))&M
def s0(x): return rr(x,7)^rr(x,18)^(x>>3)
def s1(x): return rr(x,17)^rr(x,19)^(x>>10)
def S0(x): return rr(x,2)^rr(x,13)^rr(x,22)
def S1(x): return rr(x,6)^rr(x,11)^rr(x,25)
def expand(block):
    w=list(struct.unpack('>16I',block))
    for t in range(16,64): w.append((s1(w[t-2])+w[t-7]+s0(w[t-15])+w[t-16])&M)
    return w
def compress(cv, block, r):
    w=expand(block); state=list(cv); trace=[state]
    for t in range(r):
        a,b,c,d,e,f,g,h=state
        t1=(h+S1(e)+((e&f)^((~e)&g))+K[t]+w[t])&M
        t2=(S0(a)+((a&b)^(a&c)^(b&c)))&M
        state=[(t1+t2)&M,a,b,c,(d+t1)&M,e,f,g]; trace.append(state)
    return [(x+y)&M for x,y in zip(cv,state)],trace,w
def padded(msg): return msg+b'\x80'+b'\0'*((55-len(msg))%64)+(8*len(msg)).to_bytes(8,'big')
def hash_r(msg,r):
    p=padded(msg); cv=IV; cvs=[]; traces=[]
    for off in range(0,len(p),64):
        cv,tr,w=compress(cv,p[off:off+64],r); cvs.append(cv); traces.append(tr)
    return hx(cv),cvs,traces
def hx(words): return ''.join(f'{v:08x}' for v in words)
def diff(a,b): return [f'{(y-x)&M:08x}' for x,y in zip(a,b)]

