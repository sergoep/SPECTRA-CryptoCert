#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cryptocert.gf256 import mul
from cryptocert.matrix import matmul, scalar_matrix, scalar_mul, all_square_minors_nonzero
from cryptocert.ddt import ddt, validate_aes_ddt
from cryptocert.operator import verify_L4

M=[[0xCB,0x52,0x7B,0xD1],[0x52,0xCB,0xD1,0x7B],[0x7B,0xD1,0xCB,0x52],[0xD1,0x7B,0x52,0xCB]]

def main():
    checks=[]
    checks.append(("AES GF(2^8): 0x97 * 0x72 = 1", mul(0x97,0x72)==1))
    checks.append(("M^2 = 0x72 I", matmul(M,M)==scalar_matrix(0x72,4)))
    checks.append(("M^{-1} = 0x97 M (verified by multiplication)", matmul(M,scalar_mul(0x97,M))==scalar_matrix(1,4)))
    ok,bad=all_square_minors_nonzero(M)
    checks.append(("all square minors of M nonzero => 4x4 MDS / branch number 5",ok))
    okL,_,_=verify_L4()
    checks.append(("L^4 = 0xD8 I on all 16 GF(2^8) basis vectors",okL))
    info=validate_aes_ddt(ddt())
    checks.append(("AES DDT nonzero multiplicities are {2,4}",info["nonzero_multiplicities"]==[2,4]))
    for name,ok in checks: print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("\nCLAIM BOUNDARY")
    print("[CHECKED] L^4 = 0xD8 I for the stated GF(2^8)^16 serialization.")
    print("[NOT CHECKED] W_D(4) <= 164 witness: byte-level trail certificate is not present in the supplied grant files.")
    print("[NOT ESTABLISHED] W_D(4) = 164 global optimality.")
    return 0 if all(x[1] for x in checks) else 1
if __name__=='__main__': raise SystemExit(main())
