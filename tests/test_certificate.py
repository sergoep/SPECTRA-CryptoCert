import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "verifier" / "verify_certificate.py"
CERT = ROOT / "certificates" / "recurrence_L4_0xD8.json"


class CertificateTests(unittest.TestCase):

    def run_checker(self, path):
        return subprocess.run(
            [sys.executable, str(CHECKER), str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_valid_certificate_is_accepted(self):
        result = self.run_checker(CERT)

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout + result.stderr,
        )

        self.assertIn(
            "[PASS] CryptoCert accepted: L^4 = 0xD8 I",
            result.stdout,
        )

    def test_tampered_certificate_is_rejected(self):
        cert = json.loads(CERT.read_text(encoding="utf-8"))

        # Deliberately corrupt the claimed scalar.
        cert["claim"]["scalar_hex"] = "0xD9"

        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "tampered_certificate.json"

            bad.write_text(
                json.dumps(cert, indent=2),
                encoding="utf-8",
            )

            result = self.run_checker(bad)

        self.assertNotEqual(
            result.returncode,
            0,
            msg="Tampered certificate was incorrectly accepted",
        )

        self.assertIn("[FAIL]", result.stdout)


if __name__ == "__main__":
    unittest.main()
