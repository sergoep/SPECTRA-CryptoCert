"""GF(2^8) arithmetic for the AES polynomial x^8+x^4+x^3+x+1 (0x11B)."""
AES_POLY = 0x11B

def add(a,b): return a ^ b

def mul(a,b):
    a &= 0xff; b &= 0xff; r=0
    for _ in range(8):
        if b & 1: r ^= a
        hi = a & 0x80
        a = (a << 1) & 0xff
        if hi: a ^= 0x1b
        b >>= 1
    return r

def pow_gf(a,n):
    r=1
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a); n>>=1
    return r

def inv(a):
    if a==0: raise ZeroDivisionError("0 has no inverse")
    return pow_gf(a,254)
