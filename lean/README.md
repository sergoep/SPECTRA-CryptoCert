# Lean fragment
`Recurrence.lean` is deliberately small: it formalizes only the logical implication from a four-step scalar recurrence to a four-step projective return. It does **not** formalize AES-field arithmetic and must not be cited as a formal proof of `L^4 = 0xD8 I`. The latter is checked exhaustively on a field basis by `verifier/verify_operator.py`.
