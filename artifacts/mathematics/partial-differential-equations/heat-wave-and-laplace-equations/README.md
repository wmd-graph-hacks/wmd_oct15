---
id: math-partial-differential-equations-heat-wave-and-laplace-equations
type: subtopic
title: Heat, wave, and Laplace equations
parent_topic: math-partial-differential-equations
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-multivariable-calculus
    target_type: topic
    strength: recommended
  - id: math-ordinary-differential-equations
    target_type: topic
    strength: recommended
  - id: math-linear-algebra
    target_type: topic
    strength: recommended
learning_outcomes:
  - define the central objects and notation in heat, wave, and laplace equations
  - apply a standard method from heat, wave, and laplace equations to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - partial-differential-equations
  - advanced-core
---

# Heat, Wave, and Laplace Equations

PDEs describe fields depending on multiple variables. The heat equation uₜ=κuₓₓ models diffusion: κ>0 smooths temperature differences over time. The wave equation uₜₜ=c²uₓₓ models propagation at speed c and needs both initial displacement and velocity. Laplace’s equation Δu=0 models steady-state potentials and has no time variable.

Initial conditions describe the state at a starting time; boundary conditions specify behavior at spatial edges. A PDE without enough compatible data generally has many solutions or none. Boundary conditions may be Dirichlet (value prescribed), Neumann (normal derivative prescribed), or Robin (combination).

**Example.** A rod of length L with fixed zero-temperature ends has u(0,t)=u(L,t)=0. Sine modes sin(nπx/L) satisfy these boundary values. For heat diffusion, each mode decays like exp(−κ(nπ/L)²t), with higher-frequency modes decaying faster. This explains smoothing.

The physical model determines coefficient signs and data. Check units: κ has length²/time; c has length/time. Do not apply an infinite-domain solution to a bounded domain without matching boundary conditions.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: three model equations

The heat equation u_t=κu_xx models diffusion and smooths temperature differences. The wave equation u_tt=c²u_xx models vibrations and propagates disturbances at finite speed c. Laplace’s equation u_xx+u_yy=0 models steady states such as electrostatic potential and has the mean-value property. Boundary conditions describe values or fluxes at the edges; initial conditions give the state and, for waves, initial velocity.

The type of PDE suggests behavior: heat is dissipative, wave is oscillatory, Laplace is elliptic and describes equilibrium. Units and physical assumptions determine coefficients. Solutions require compatible initial and boundary data; boundary conditions are part of the problem, not optional decorations.

**Worked example.** For a vibrating string of length L with fixed ends, u(0,t)=u(L,t)=0. A separated mode sin(nπx/L) has temporal frequency cnπ/L. Higher n means shorter wavelength and faster oscillation. Initial shape determines how much of each mode appears.

**Practice with answers.** (1) Heat flow decreases sharp temperature peaks over time. (2) Wave equation needs initial displacement and velocity. (3) A steady heat distribution with no sources satisfies Laplace’s equation. (4) Fixed-end string uses zero displacement at both boundaries.

**Common pitfalls:** swapping initial and boundary data; ignoring coefficient units; and expecting a unique solution without sufficient boundary/initial conditions.
