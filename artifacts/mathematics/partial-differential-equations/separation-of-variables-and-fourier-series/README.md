---
id: math-partial-differential-equations-separation-of-variables-and-fourier-series
type: subtopic
title: Separation of variables and Fourier series
parent_topic: math-partial-differential-equations
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-partial-differential-equations-heat-wave-and-laplace-equations
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in separation of variables and fourier series
  - apply a standard method from separation of variables and fourier series to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - partial-differential-equations
  - advanced-core
---

# Separation of Variables and Fourier Series

Separation of variables seeks product solutions such as u(x,t)=X(x)T(t). Substitution into a linear PDE often separates an x-only expression from a t-only expression; each must equal a constant. Boundary conditions produce an eigenvalue problem for X, while the time equation determines modal evolution.

Fourier series express suitable functions as sums of orthogonal sines and cosines. On [0,L], fixed-zero endpoints naturally use sin(nπx/L). Coefficients are projections: bₙ=(2/L)∫₀ᴸf(x)sin(nπx/L)dx. The series represents the initial profile in the appropriate convergence sense; discontinuities converge to midpoint values under standard conditions.

**Example.** For initial profile f(x)=sin(πx/L), the heat solution is one mode: u=sin(πx/L)e^(−κπ²t/L²). Since it already satisfies the boundary values, no infinite expansion is needed.

Check orthogonality normalization and boundary conditions. Separation produces candidate modes; superposition is justified by linearity, and coefficients must match initial data.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: separate space and time modes

Assume u(x,t)=X(x)T(t), substitute into a linear PDE, and divide to separate a space-only expression from a time-only one; both equal a separation constant. Boundary conditions select eigenfunctions and eigenvalues. The general solution is a sum of modes, with coefficients chosen to match initial data through a Fourier series.

On [0,L] with zero endpoint values, the eigenfunctions are sin(nπx/L). Orthogonality lets each Fourier coefficient be calculated independently. Sine series suit odd extensions; cosine series suit even extensions. Convergence at discontinuities approaches the midpoint of one-sided limits, while endpoint behavior depends on the extension.

**Worked example.** For initial string shape f(x)=sin(πx/L), the wave solution is u(x,t)=sin(πx/L)cos(cπt/L) when initial velocity is zero. It is a single eigenmode, so no infinite sum is needed. Substitute into the PDE and check boundary and initial conditions.

**Practice with answers.** (1) Fixed zero ends yield sine modes. (2) A constant initial temperature under insulated boundaries uses a cosine/constant mode. (3) Fourier coefficients are projections onto orthogonal modes. (4) A piecewise smooth Fourier series converges to the function at continuity points and to the jump midpoint at jumps.

**Common pitfalls:** using eigenfunctions incompatible with boundaries; omitting the separation constant’s sign cases; and assuming every Fourier series converges pointwise to the original at a discontinuity.
