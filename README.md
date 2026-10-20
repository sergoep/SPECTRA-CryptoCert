# SPECTRA-CryptoCert v0.1

Minimal independent verification core accompanying the SPECTRA proposal **Beyond Branch Number: Recurrence-Aware Cryptanalysis and Machine-Certified Verification of Structured MDS Diffusion Layers**.

## Scientific principle

**Search is untrusted; verification is independently checkable.** Solver output is evidence only after its witness/proof object is checked against explicit conventions and a stated search domain.

## What v0.1 actually checks

Using the AES field polynomial `0x11B` and the concrete 4x4 matrix

`[[CB,52,7B,D1],[52,CB,D1,7B],[7B,D1,CB,52],[D1,7B,52,CB]]`,

v0.1 independently checks:

* `M^2 = 0x72 I`;
* `M^{-1} = 0x97 M`;
* every square minor of `M` is nonzero, hence the 4x4 matrix is superregular/MDS and has branch number 5;
* the AES S-box DDT has nonzero multiplicities only 2 and 4 (and differential uniformity 4).

## Claim boundary

The supplied grant documents state `L^4 = 0xD8 I` and report a four-layer characteristic of weight 164, but they do **not** contain the full 128-bit serialization of `L` or the byte-by-byte weight-164 trail. v0.1 therefore does not pretend to verify those two claims. They become the end-to-end v0.2 milestone once the exact machine-readable data are supplied.

v0.1 does **not** establish `W_D(4)=164`, differential/linear hull security, or nonlinear subspace exclusion.

## Reproduce

```bash
python -m unittest discover -s tests -v
python verifier/verify.py
```

No third-party Python dependency is required for v0.1.

## Repository map

* `cryptocert/` — small trusted arithmetic/checking core
* `instances/` — machine-readable public instances
* `certificates/` — certificates and explicit claim scope
* `verifier/` — command-line verifier
* `tests/` — regression tests
* `docs/` — trust model and certificate format
* `lean/` — next formalization milestone

## Reproducibility policy

All conventions affecting cryptographic meaning must be serialized: field polynomial, byte order, state layout, S-box, linear map, round order, and optimization domain. A result that cannot be reconstructed from these public artifacts is not labelled machine-certified.

## License

The proposal plans Apache-2.0 subject to NPUA approval. See `LICENSE-PENDING.md`. Do not publish an Apache-2.0 LICENSE as an institutional commitment until approval is confirmed.

## Citation

See `CITATION.cff`.
