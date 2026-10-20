from .aes import SBOX

def ddt(sbox=SBOX):
    T=[[0]*256 for _ in range(256)]
    for a in range(256):
        for x in range(256): T[a][sbox[x]^sbox[x^a]] += 1
    return T

def validate_aes_ddt(T):
    assert all(sum(r)==256 for r in T)
    assert T[0][0]==256 and sum(T[0][1:])==0
    vals={T[a][b] for a in range(1,256) for b in range(256) if T[a][b]}
    assert vals <= {2,4}
    return {"nonzero_multiplicities":sorted(vals),"differential_uniformity":max(max(r) for r in T[1:])}
