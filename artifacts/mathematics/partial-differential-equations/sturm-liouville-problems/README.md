---
id: math-partial-differential-equations-sturm-liouville-problems
type: subtopic
title: Sturm–Liouville problems
parent_topic: math-partial-differential-equations
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-partial-differential-equations-separation-of-variables-and-fourier-series
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in sturm–liouville problems
  - apply a standard method from sturm–liouville problems to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - partial-differential-equations
  - advanced-core
---

# Sturm–Liouville Theory

A Sturm–Liouville problem has form −(p(x)y′)′+q(x)y=λw(x)y with boundary conditions and positive weight w. Under suitable regularity and self-adjoint boundary conditions, eigenvalues are real, eigenfunctions for distinct eigenvalues are orthogonal under weighted inner product ∫yₘyₙw dx, and eigenfunctions form a useful expansion basis.

This framework unifies Fourier sine/cosine modes and many PDE separation problems. The boundary conditions select allowed eigenvalues; changing the boundary conditions changes the spectrum. Orthogonality lets one compute expansion coefficients by projection.

**Example.** −y″=λy on [0,L] with y(0)=y(L)=0. Nontrivial solutions require λₙ=(nπ/L)² and yₙ=sin(nπx/L), n≥1. Distinct modes are orthogonal: ∫₀ᴸ sin(mπx/L)sin(nπx/L)dx=0 if m≠n.

The theorem needs hypotheses; singular endpoints and unusual weights require additional care. Keep track of the weight in the inner product rather than assuming ordinary orthogonality.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: eigenvalue problems for differential operators

A Sturm–Liouville problem has form −(p(x)y′)′+q(x)y=λw(x)y with boundary conditions and positive weight w. Under standard regularity and boundary assumptions, eigenvalues are real and eigenfunctions for distinct eigenvalues are orthogonal with respect to weighted inner product ∫u v w dx. These eigenfunctions form a basis suitable for expanding initial or forcing functions.

This theory generalizes Fourier sine and cosine series. The boundary conditions determine which eigenvalues are permitted; changing them changes the spectrum. Orthogonality simplifies coefficient calculations and decouples PDE modes.

**Worked example.** Solve −y″=λy on [0,L] with y(0)=y(L)=0. Nontrivial solutions require λₙ=(nπ/L)² and yₙ=sin(nπx/L), n=1,2,… . Different modes are orthogonal because ∫₀ᴸsin(mπx/L)sin(nπx/L)dx=0 for m≠n.

**Practice with answers.** (1) The first eigenvalue is (π/L)². (2) No λ≤0 gives a nontrivial solution in this fixed-end example. (3) Weight w changes the inner product used for orthogonality. (4) Boundary conditions are part of the eigenvalue problem.

**Common pitfalls:** dropping the weight function; assuming arbitrary boundary conditions give the same spectrum; and confusing a trivial zero solution with a valid eigenfunction.
