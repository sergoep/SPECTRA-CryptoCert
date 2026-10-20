#!/usr/bin/env python3
"""Deterministic pilot: target dyadic Cauchy MDS vs non-dyadic Cauchy-MDS controls.
Controls preserve field, 4x4 size, Cauchy superregularity/branch number 5, and the same shear.
They do NOT match circuit cost or coefficient multiset. This is a structural pilot, not a security benchmark.
"""
import random,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cryptocert.gf256 import inv,mul
from cryptocert.operator import M as TARGET, basis_state, scale

def mix(s,M):
 o=[[0]*4 for _ in range(4)]
 for j in range(4):
  for i in range(4):
   z=0
   for k in range(4): z ^= mul(M[i][k],s[k][j])
   o[i][j]=z
 return o
def shear(s):
 o=[[0]*4 for _ in range(4)]
 for i in range(4):
  for j in range(4):o[i][j^i]=s[i][j]
 return o
def L(s,M):return shear(mix(s,M))
def fourth_scalar(M):
 imgs=[]
 for k in range(16):
  t=basis_state(k)
  for _ in range(4):t=L(t,M)
  imgs.append(t)
 c=imgs[0][0][0]
 if c and all(imgs[k]==scale(c,basis_state(k)) for k in range(16)):return c
 return None
def cauchy(rng):
 pts=rng.sample(range(256),8); x,y=pts[:4],pts[4:]
 return [[inv(a^b) for b in y] for a in x]
def main(n=100,seed=20261021):
 rng=random.Random(seed); tc=fourth_scalar(TARGET); hits=0
 for _ in range(n):
  if fourth_scalar(cauchy(rng)) is not None:hits+=1
 out={'seed':seed,'controls':n,'target_L4_scalar':tc,'control_L4_scalar_hits':hits,
      'matching':'AES field; 4x4 Cauchy-MDS (hence branch number 5); four parallel columns; identical shear',
      'not_matched':'coefficient multiset and implementation cost'}
 print(json.dumps(out,indent=2)); return out
if __name__=='__main__':main()
