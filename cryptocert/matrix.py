from itertools import combinations
from .gf256 import mul, inv

def matmul(A,B):
    return [[_xor(mul(A[i][k],B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def _xor(xs):
    r=0
    for x in xs:r^=x
    return r

def scalar_matrix(c,n): return [[c if i==j else 0 for j in range(n)] for i in range(n)]
def scalar_mul(c,A): return [[mul(c,x) for x in row] for row in A]
def identity(n): return scalar_matrix(1,n)

def det(A):
    A=[r[:] for r in A]; n=len(A); d=1
    for c in range(n):
        p=next((r for r in range(c,n) if A[r][c]),None)
        if p is None:return 0
        if p!=c:A[c],A[p]=A[p],A[c]  # sign irrelevant in characteristic 2
        pivot=A[c][c]; d=mul(d,pivot); ip=inv(pivot)
        for r in range(c+1,n):
            if A[r][c]:
                f=mul(A[r][c],ip)
                for j in range(c,n): A[r][j]^=mul(f,A[c][j])
    return d

def all_square_minors_nonzero(A):
    m=len(A); n=len(A[0])
    for k in range(1,min(m,n)+1):
        for rs in combinations(range(m),k):
            for cs in combinations(range(n),k):
                if det([[A[i][j] for j in cs] for i in rs])==0:return False,(rs,cs)
    return True,None
