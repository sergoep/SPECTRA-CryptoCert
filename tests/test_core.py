import unittest
from cryptocert.gf256 import mul
from cryptocert.matrix import matmul, scalar_matrix, scalar_mul, all_square_minors_nonzero
from cryptocert.ddt import ddt,validate_aes_ddt
M=[[0xCB,0x52,0x7B,0xD1],[0x52,0xCB,0xD1,0x7B],[0x7B,0xD1,0xCB,0x52],[0xD1,0x7B,0x52,0xCB]]
class TestCore(unittest.TestCase):
 def test_inverse_constant(self): self.assertEqual(mul(0x97,0x72),1)
 def test_square(self): self.assertEqual(matmul(M,M),scalar_matrix(0x72,4))
 def test_inverse(self): self.assertEqual(matmul(M,scalar_mul(0x97,M)),scalar_matrix(1,4))
 def test_mds(self): self.assertTrue(all_square_minors_nonzero(M)[0])
 def test_ddt(self): self.assertEqual(validate_aes_ddt(ddt())["nonzero_multiplicities"],[2,4])
if __name__=='__main__':unittest.main()

def test_full_operator_recurrence():
    from cryptocert.operator import verify_L4
    assert verify_L4()[0]
