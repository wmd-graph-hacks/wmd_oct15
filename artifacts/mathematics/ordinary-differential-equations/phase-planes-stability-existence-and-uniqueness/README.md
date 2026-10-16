---
id: math-ordinary-differential-equations-phase-planes-stability-existence-and-uniqueness
type: subtopic
title: Phase planes, stability, existence and uniqueness
parent_topic: math-ordinary-differential-equations
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-ordinary-differential-equations-matrix-exponentials-and-laplace-transforms
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in phase planes, stability, existence and uniqueness
  - apply a standard method from phase planes, stability, existence and uniqueness to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - ordinary-differential-equations
  - advanced-core
---

# Phase Planes, Stability, Existence, and Uniqueness

For a planar autonomous system x′=f(x,y), y′=g(x,y), trajectories form a phase portrait. Equilibria solve f=g=0. Linearize near an equilibrium using the Jacobian matrix; eigenvalues indicate local behavior: negative real parts suggest attraction, positive suggest instability, and mixed signs give a saddle. Purely imaginary eigenvalues need nonlinear analysis.

Existence and uniqueness theorems justify whether initial data determine a solution. For y′=f(t,y), continuity of f gives local existence; a local Lipschitz condition in y gives uniqueness (Picard–Lindelöf). Without uniqueness, multiple solution curves may pass through the same initial point.

**Example.** y′=√|y| with y(0)=0 has the zero solution and also solutions that remain zero until an arbitrary time then depart as a quadratic curve. The right-hand side is continuous but not locally Lipschitz at zero, so uniqueness can fail.

Stability describes behavior under small perturbations, not merely whether a formula exists. Draw nullclines and arrow directions to build intuition, then support claims with eigenvalues or a Lyapunov argument.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: equilibria, phase portraits, and well-posedness

For an autonomous system x′=f(x), equilibria solve f(x*)=0. In one dimension, a sign chart for f determines whether nearby trajectories move toward or away from the equilibrium. For systems, linearize near x*: x′≈J(x*)(x−x*). Eigenvalues with negative real parts indicate local asymptotic stability; any positive real part indicates instability. Purely imaginary eigenvalues require nonlinear analysis.

Existence and uniqueness theorems state conditions for solutions through initial data. If f is continuous, local existence is often guaranteed; local Lipschitz continuity in the state gives uniqueness. A failure of a sufficient condition does not by itself prove nonuniqueness. Solutions can cease to exist globally by blowing up or reaching a domain boundary.

**Worked example.** For x′=x(1−x), equilibria are 0 and 1. If 0<x<1, derivative is positive so solutions rise toward 1; if x>1, derivative is negative so they decrease toward 1. Thus 1 is stable and 0 is unstable for positive perturbations.

**Practice with answers.** (1) x′=−2x has stable equilibrium 0. (2) x′=x has unstable equilibrium 0. (3) A continuous vector field gives local existence, while local Lipschitz is a standard uniqueness condition. (4) A phase portrait shows direction and qualitative behavior, not necessarily exact time values.

**Common pitfalls:** classifying stability from a single trajectory; assuming every solution exists for all time; and claiming theorem failure when only a sufficient condition is absent.
