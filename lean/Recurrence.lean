/-
SPECTRA-CryptoCert
Minimal machine-checked consequence of a four-step recurrence.

Scope:
This file proves an algebraic consequence of the recurrence hypothesis
L^4 = lambda * I.  It does NOT formalize GF(2^8), the concrete
128-bit diffusion layer, or independently establish lambda = 0xD8.
Those finite computations are checked by the independent Python verifier.
-/

def fourthIterate {α : Type} (L : α → α) (x : α) : α :=
  L (L (L (L x)))

def iterate8 {α : Type} (L : α → α) (x : α) : α :=
  L (L (L (L (L (L (L (L x)))))))

theorem recurrence_four_implies_eight
    {α : Type}
    (L : α → α)
    (scale : α → α)
    (hrec : ∀ x : α, fourthIterate L x = scale x)
    (hcomm : ∀ x : α, fourthIterate L (scale x) = scale (scale x)) :
    ∀ x : α, iterate8 L x = scale (scale x) := by
  intro x
  change fourthIterate L (fourthIterate L x) = scale (scale x)
  rw [hrec x]
  exact hcomm x
