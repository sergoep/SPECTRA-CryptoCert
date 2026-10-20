from .gf256 import mul
from .matrix import matmul, identity
M=[[0xCB,0x52,0x7B,0xD1],[0x52,0xCB,0xD1,0x7B],[0x7B,0xD1,0xCB,0x52],[0xD1,0x7B,0x52,0xCB]]

def mix(state):
    # state[row][col]
    out=[[0]*4 for _ in range(4)]
    for j in range(4):
        col=[state[i][j] for i in range(4)]
        for i in range(4):
            x=0
            for k in range(4): x ^= mul(M[i][k],col[k])
            out[i][j]=x
    return out

def shear(state):
    out=[[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4): out[i][j^i]=state[i][j]
    return out

def L(state): return shear(mix(state))

def scale(c,state): return [[mul(c,x) for x in row] for row in state]

def basis_state(k):
    s=[[0]*4 for _ in range(4)]; s[k//4][k%4]=1; return s

def verify_L4():
    for k in range(16):
        s=basis_state(k); t=s
        for _ in range(4): t=L(t)
        if t != scale(0xD8,s): return False,k,t
    return True,None,None
