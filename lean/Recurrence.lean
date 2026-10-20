/- Minimal logical formalization of the projective-return implication.
   Scope: this file does NOT formalize GF(2^8) arithmetic or prove L^4=0xD8 I.
   That finite computation is independently checked by verifier/verify_operator.py. -/

def fourthIterate {α : Type} (L : α → α) (x : α) : α := L (L (L (L x)))

theorem recurrence_implies_projective_return
    {α : Type} (L : α → α) (scale : α → α)
    (h : ∀ x : α, fourthIterate L x = scale x) :
    ∀ x : α, L (L (L (L x))) = scale x := by
  intro x
  exact h x
