---
id: math-complex-analysis-residues-and-conformal-mappings
type: subtopic
title: Residues and conformal mappings
parent_topic: math-complex-analysis
phase: advanced-core
estimated_minutes: 60
prerequisites:
  - id: math-complex-analysis-taylor-and-laurent-series
    target_type: subtopic
    strength: soft
learning_outcomes:
  - define the central objects and notation in residues and conformal mappings
  - apply a standard method from residues and conformal mappings to a well-posed problem
  - justify the method’s assumptions and interpret the result
tags:
  - mathematics
  - complex-analysis
  - advanced-core
---

# Residues and Conformal Mappings

The residue at an isolated singularity a is the coefficient of (z−a)⁻¹ in the Laurent series. The residue theorem says ∮C f(z)dz=2πi times the sum of residues inside a positively oriented contour. For a simple pole, Res(f,a)=lim_{z→a}(z−a)f(z). Higher-order poles can be handled by derivatives or series expansion.

**Example.** Evaluate ∮_|z|=2 dz/(z²+1). Poles are i and −i, both inside. Residue at i is 1/(2i); at −i is 1/(−2i); they sum to zero, so integral is zero. This agrees with the function’s odd symmetry over the symmetric contour, but residue computation gives a systematic justification.

A holomorphic map with f′(z₀)≠0 is locally conformal: it preserves angles and orientation near z₀, while scaling lengths by |f′(z₀)|. Maps such as z↦z² can fail conformality where derivative vanishes and are globally many-to-one. A branch of log maps a slit plane to a strip; branch choice matters.

For real integrals evaluated by residues, justify contour choice and show arc contributions vanish. The residue theorem does not itself guarantee a real integral formula.

## Study sequence

Reproduce the worked argument without looking, solve a changed example, and state precisely which assumptions each theorem needs. Revisit after a delay and explain the central idea in your own words.

## Lesson: residues evaluate contour integrals

The residue theorem states ∮C f(z)dz=2πi times the sum of residues at isolated singularities inside a positively oriented contour. For a simple pole at a, Res(f,a)=lim_{z→a}(z−a)f(z). For higher-order poles, use a Laurent coefficient or derivative formula. Choose a contour enclosing exactly the singularities needed and check poles on the path separately.

Conformal maps are holomorphic functions with nonzero derivative locally; they preserve angles and locally scale lengths by |f′(z)|. Möbius maps (az+b)/(cz+d) send circles/lines to circles/lines when ad−bc≠0. They can simplify geometric regions, but branch points and global injectivity require care.

**Worked example.** ∮|z|=2 (z+1)/[z(z−1)] dz encloses poles 0 and 1. Residues are −1 at 0 and 2 at 1, sum 1, so integral is 2πi. Partial fractions, (z+1)/[z(z−1)]=−1/z+2/(z−1), confirms the residue calculation.

**Practice with answers.** (1) Res(1/(z−a),a)=1. (2) The integral of 1/z around a counterclockwise unit circle is 2πi. (3) z↦z² is conformal where z≠0 but not locally conformal at 0. (4) Pole location relative to contour determines whether its residue contributes.

**Common pitfalls:** including an exterior pole; missing a pole on the contour; using the simple-pole limit for higher-order poles; and assuming angle preservation globally implies one-to-one behavior.
