# Exact E8 Block Error Distribution

Status: **distribution specification and hardness-coverage analysis; not a protocol or security proof**

## Decision

The first concrete E8-shaped error family studied by this repository is a **truncated discrete Gaussian over the genuine E8 lattice**, sampled independently by 8-dimensional blocks.

For parameters `s > 0` and cutoff `R >= 0`, define

\[
S_R = \{x \in E_8 : \|x\|_2 \le R\}.
\]

For each `x in S_R`, define

\[
\rho_s(x) = \exp(-\pi \|x\|_2^2/s^2)
\]

and normalization

\[
Z_{s,R} = \sum_{z \in S_R} \rho_s(z).
\]

The one-block probability mass function is

\[
P_{s,R}[X=x] = \rho_s(x)/Z_{s,R} \quad (x \in S_R),
\]

and zero outside `S_R`.

This is an exact finite distribution. The cutoff is part of the distribution and must never be omitted from parameter sets.

## Why truncate

An untruncated lattice discrete Gaussian is mathematically natural, but it has infinite support. The current research goal includes checking modern Module-LWE results for **bounded** general distributions, so a finite cutoff makes the candidate distribution explicit and allows entropy, tail loss, and implementation behavior to be measured exactly.

Truncation changes the distribution. Any theorem covering an untruncated Gaussian does not automatically cover this truncated E8 distribution, and any theorem for arbitrary bounded distributions still has its own entropy, parameter, and sample-count hypotheses that must be checked.

## Coordinate representation

The E8 model used in this repository contains both integer and half-integer coordinates. To avoid pretending that `1/2 mod q` is a small centered error coefficient, protocol-facing experiments SHALL represent

\[
Y = 2X.
\]

Then `Y` is integral and belongs to the scaled lattice `2E8`.

The modular embedding is coefficient-wise:

\[
\iota_q(Y) = Y \bmod q \in \mathbb{Z}_q^8.
\]

This preserves E8 geometry up to the fixed public scale factor two. The scale factor must be included when comparing variance or decryption noise against non-E8 baselines.

This document does **not** claim that eight consecutive coefficients of a cyclotomic-ring Module-LWE instance may be replaced by one E8 block without additional proof. The embedding above only defines the candidate coefficient distribution to be studied.

## Multiple blocks

For `N` blocks, sample

\[
X_1,\ldots,X_N \overset{\mathrm{iid}}{\sim} P_{s,R}
\]

and concatenate them to obtain an element of `E8^N`. Equivalently, concatenate `Y_i = 2X_i` for integer arithmetic.

Therefore the full PMF factorizes across blocks:

\[
P[X_1=x_1,\ldots,X_N=x_N]
= \prod_{i=1}^N P_{s,R}[X_i=x_i].
\]

**Block independence is a design requirement.** A sampler that shares randomness across blocks does not implement this distribution.

## Mean and covariance

The support is centrally symmetric and the weight depends only on Euclidean norm. Hence

\[
\mathbb{E}[X] = 0.
\]

Because `S_R` and the radial weight are invariant under the E8 Weyl group, the covariance is isotropic:

\[
\operatorname{Cov}(X)=\sigma_{s,R}^2 I_8,
\]

where

\[
\sigma_{s,R}^2 = \frac{1}{8 Z_{s,R}}
\sum_{x\in S_R} \|x\|_2^2\,\rho_s(x).
\]

For `Y=2X`,

\[
\operatorname{Cov}(Y)=4\sigma_{s,R}^2 I_8.
\]

Zero off-diagonal covariance does **not** imply coordinate independence. Coordinates inside a block remain dependent because E8 membership and the radial cutoff constrain which coordinate tuples can occur.

Across distinct iid blocks the cross-covariance is zero and the blocks are independent by construction.

## Tails and truncation loss

The implemented distribution has a hard tail:

\[
P_{s,R}(\|X\|_2 > R)=0.
\]

To measure how much truncation changes the corresponding infinite E8 discrete Gaussian, define

\[
\delta_{s,R}
= \frac{\sum_{x\in E_8,\,\|x\|>R}\rho_s(x)}
       {\sum_{x\in E_8}\rho_s(x)}.
\]

`delta_{s,R}` is the removed probability mass. It must be computed or tightly bounded for every proposed `(s,R)` before parameters are accepted. No fixed numerical cutoff is selected in this document.

## Entropy quantities required for hardness analysis

For the finite one-block distribution define

\[
H_\infty(X) = -\log_2 \max_{x\in S_R} P[X=x].
\]

The maximum occurs at the zero vector because the weight decreases with norm, so

\[
H_\infty(X) = \log_2 Z_{s,R}.
\]

For `N` independent blocks,

\[
H_\infty(X_1,\ldots,X_N)=N\log_2 Z_{s,R}.
\]

This is one of the quantities that must be compared with any theorem requiring a bounded distribution with sufficient entropy.

## Relationship to standard LWE hardness results

Classic LWE worst-case-to-average-case reductions establish hardness for specific Gaussian-style error families. Regev's foundational reduction uses Gaussian error in the LWE problem; later classical reductions also retain tightly specified error requirements. Those results should not be cited as direct coverage for this E8-block-correlated truncated distribution merely because its PMF contains an exponential quadratic term.

For Module-LWE, Langlois and Stehle establish worst-case/average-case reductions for the standard Module-LWE setting. The standard theoretical formulation uses Gaussian error in the module/ring setting. Again, this is not by itself a proof for an E8-block replacement.

## Important 2026 result: general bounded M-LWE distributions

Boudgoust, Jeudy, Tairi, and Wen, *Hardness of M-LWE with General Distributions and Applications to Leaky Variants* (PKC 2026), prove hardness results for M-LWE where the error vector follows an **arbitrary bounded distribution with sufficient entropy**, subject to restrictions including the number of samples and the precise theorem parameters.

This result is directly relevant because `P_{s,R}` is bounded and finite.

However, this repository has **not yet established theorem coverage** for the E8 candidate. To claim coverage we still need to verify, from the full theorem statement:

1. which representation/domain the arbitrary distribution occupies;
2. the required min-entropy threshold and whether `log2(Z_{s,R})` meets it after the proposed modular/ring embedding;
3. bounds on support/norm relative to modulus and ring/module parameters;
4. restrictions on the number of M-LWE samples;
5. whether eight-coordinate E8 blocks aligned to coefficient positions satisfy the theorem's distribution model without an unproved change of basis or independence assumption;
6. whether the theorem covers the desired secret distribution as well as the error distribution used by a future construction.

Until all six are checked, the correct repository statement is:

> **Conditional opportunity, not established coverage.** A new PKC 2026 general-distribution theorem may be broad enough to cover a bounded E8 error family, but this repository has not verified its hypotheses for the proposed E8 block embedding and therefore makes no inherited Module-LWE hardness claim.

That is a more precise result than the previous blanket statement that no applicable theorem was known.

## Security consequences of block structure

Even if a general-distribution reduction eventually applies, concrete security still requires separate attack analysis. The E8 block distribution publicly reveals:

- 8-coordinate block boundaries;
- parity/coset structure inherited from E8;
- radial-shell probability structure;
- a large public automorphism/Weyl symmetry group;
- within-block dependence despite isotropic covariance.

Worst-case/average-case hardness coverage would not remove the need to test whether these properties change concrete primal, dual, hybrid, distinguishing, or decryption-failure attacks at practical parameters.

## Acceptance tests for a future sampler

A distribution-only implementation must demonstrate all of the following before it can be used by protocol code:

1. every output lies in `S_R` exactly;
2. no global RNG reseeding and no secret-derived RNG seed;
3. an explicit caller-provided CSPRNG/test RNG interface;
4. empirical shell frequencies converge to the specified PMF;
5. empirical mean converges to zero;
6. empirical covariance converges to `sigma^2 I_8`;
7. tests demonstrate that coordinates inside a block are not falsely assumed independent;
8. tests demonstrate independence between separately sampled blocks;
9. modular serialization round-trips to the intended centered `2E8` representatives when no wraparound occurs;
10. truncation loss `delta_{s,R}` or a rigorous bound is recorded for every candidate parameter set.

## Current conclusion

The exact research distribution is now defined, including its PMF, cutoff/tails, covariance, block dependence, block independence, entropy quantity, and modular embedding.

The hardness conclusion is deliberately **not** "covered" and deliberately **not** "impossible": PKC 2026 introduced a potentially relevant general-distribution M-LWE theorem. The next task is to check that theorem's quantitative hypotheses against explicit `(s,R,q,n,k,m)` candidate parameters. If the hypotheses cannot be met without destroying usefulness or correctness, that is a negative result and E8 should move outside the secrecy core.

## Primary references

- O. Regev, *On Lattices, Learning with Errors, Random Linear Codes, and Cryptography*, STOC 2005 / JACM 2009.
- A. Langlois and D. Stehle, *Worst-case to average-case reductions for module lattices*, Designs, Codes and Cryptography 75 (2015), 565-599.
- K. Boudgoust, C. Jeudy, E. Tairi, W. Wen, *Hardness of M-LWE with General Distributions and Applications to Leaky Variants*, PKC 2026, pp. 3-37, DOI 10.1007/978-3-032-26731-3_1; full version ePrint 2025/1472.
- NIST FIPS 203, *Module-Lattice-Based Key-Encapsulation Mechanism Standard* (2024).

## Handoff

Extract the exact quantitative hypotheses from the PKC 2026 general-distribution theorem and test them against concrete research parameter candidates. Do not design `KeyGen`, `Encaps`, or `Decaps` until that coverage check is complete.
