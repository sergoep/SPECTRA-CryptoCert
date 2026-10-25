import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERT = ROOT / "certificates" / "recurrence_L4_0xD8.json"


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def main(cert_path: str | None = None) -> int:
    path = Path(cert_path) if cert_path else DEFAULT_CERT

    if not path.is_absolute():
        path = ROOT / path

    if not path.exists():
        return fail(f"certificate not found: {path}")

    try:
        cert = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"invalid JSON: {exc}")

    if cert.get("schema") != "spectra-cryptocert-v0.3":
        return fail("unsupported certificate schema")

    claim = cert.get("claim", {})

    if claim.get("type") != "operator_scalar_power":
        return fail("unsupported claim type")

    if claim.get("power") != 4:
        return fail("unexpected operator power")

    if claim.get("scalar_hex") != "0xD8":
        return fail(
            f'certificate claims {claim.get("scalar_hex")}, '
            "but this verifier expects the independently checked 0xD8 claim"
        )

    if claim.get("dimension") != 16:
        return fail("unexpected state dimension")

    field = cert.get("field", {})

    if field.get("name") != "GF(2^8)":
        return fail("unexpected field")

    if field.get("modulus_hex") != "0x11B":
        return fail("unexpected GF(2^8) modulus")

    #
    # Important:
    # Do not trust the certificate merely because its metadata says 0xD8.
    # Execute the existing independent verifier, which recomputes the
    # finite-field/operator claim from the repository implementation.
    #
    verifier = ROOT / "verifier" / "verify.py"

    result = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    print(result.stdout, end="")

    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    if result.returncode != 0:
        return fail("independent verifier rejected the concrete claim")

    output = result.stdout

    required_markers = [
        "L^4",
        "0xD8",
    ]

    if not all(marker in output for marker in required_markers):
        return fail(
            "independent verifier completed but did not emit the "
            "required L^4 / 0xD8 evidence"
        )

    print("[PASS] certificate metadata validated")
    print("[PASS] independent verifier recomputed the concrete claim")
    print("[PASS] CryptoCert accepted: L^4 = 0xD8 I")

    return 0


if __name__ == "__main__":
    certificate = sys.argv[1] if len(sys.argv) > 1 else None
    raise SystemExit(main(certificate))
