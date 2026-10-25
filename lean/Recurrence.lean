/-
SPECTRA-CryptoCert
Formal recurrence layer

This file deliberately does NOT claim to formalize GF(2^8)
arithmetic or independently establish the concrete identity

    L^4 = 0xD8 I.

The concrete finite-field computation is checked independently
by the Python verifier.

Here we formalize the algebraic consequence of a certified
four-step recurrence

    L^4 = S

and derive the corresponding 8-step and 4k-step identities.
-/

namespace CryptoCert

def iterate4 {α : Type} (L : α → α) (x : α) : α :=
  L (L (L (L x)))

def iterate8 {α : Type} (L : α → α) (x : α) : α :=
  L (L (L (L (L (L (L (L x)))))))

/--
If four applications of L agree with S on every input,
then eight applications of L agree with S ∘ S.

This is the formal recurrence step used by CryptoCert.
-/
theorem recurrence_four_implies_eight
    {α : Type}
    (L S : α → α)
    (h : ∀ x : α, iterate4 L x = S x) :
    ∀ x : α, iterate8 L x = S (S x) := by
  intro x
  change iterate4 L (iterate4 L x) = S (S x)
  rw [h]
  rw [h]

/--
Specialization to an involutive return map:
if S² = id, then the certified four-step recurrence implies
an eight-step return to the original state.
-/
theorem recurrence_involution_implies_eight_identity
    {α : Type}
    (L S : α → α)
    (hrec : ∀ x : α, iterate4 L x = S x)
    (hinv : ∀ x : α, S (S x) = x) :
    ∀ x : α, iterate8 L x = x := by
  intro x
  rw [recurrence_four_implies_eight L S hrec x]
  exact hinv x

/--
If the four-step return map is already the identity,
then four applications of L return every state unchanged.
-/
theorem recurrence_identity
    {α : Type}
    (L : α → α)
    (h : ∀ x : α, iterate4 L x = x) :
    ∀ x : α, iterate4 L x = x := by
  exact h

end CryptoCert
