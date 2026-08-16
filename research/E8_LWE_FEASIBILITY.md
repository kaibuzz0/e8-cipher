# E8-Shaped LWE / Module-LWE Feasibility Note

Status: **candidate-selection research, not a security proof**

## Decision

For the successor research track, the primary E8-specific hypothesis will be:

> **Use genuine E8 geometry in the error/reconciliation side of an
> LWE/Module-LWE-style construction, while treating the hardness claim as open
> until the exact distribution is covered by a credible reduction.**

The project will **not** return to a GGH-style hidden-basis trapdoor as its
primary successor direction. If E8-shaped error geometry cannot be tied to a
credible hardness assumption, E8 will be moved outside the secrecy core and
studied only as a quantization/reconciliation/coding layer around a standard
KEM.

This decision chooses what to investigate. It does not establish that the
resulting construction is secure.

## Why this is the most plausible E8 role

The active research substrate now provides genuine E8 roots, exact membership,
Weyl reflections, and explicit E8^N direct sums. Those objects naturally define
short vectors, Voronoi geometry, and quantization/reconciliation experiments.
They do **not** by themselves provide a modern public-key hardness reduction.

NIST FIPS 203 specifies ML-KEM and states that its security is related to the
Module Learning With Errors problem. Therefore any E8 modification should be
measured against a Module-LWE baseline rather than against the archived v2 GGH
prototype.

Changing LWE secret/error distributions is security-sensitive: published
analysis of Kyber-family variants shows distribution choices can change both
estimated LWE hardness and decryption-failure attack behavior. That is exactly
why an E8-shaped distribution must be analyzed as a new assumption/parameter
choice rather than treated as cosmetic geometry.

## Candidate distribution model

The first mathematical object to study is a block distribution over E8:

1. choose a scale parameter `s`;
2. sample an 8-dimensional short vector from a discrete-Gaussian-like
   distribution over the genuine E8 lattice;
3. repeat independently across `N` blocks to form an E8^N error vector;
4. embed/map the result into the modulus domain used by an LWE/Module-LWE-style
   public equation.

The exact sampler is intentionally **not specified yet**. "Gaussian-like" is
not acceptable in the final construction. The next pass must write the exact
probability mass function and normalization/truncation rules before code.

## Security questions that must be answered first

### 1. Reduction coverage

Determine whether an existing LWE/Module-LWE worst-case/average-case reduction
covers the exact E8-block distribution. If only spherical/independent Gaussian
or other specific error families are covered, E8 block correlation must not be
silently substituted.

Current result: this repository has **not established** a published reduction
covering the proposed E8^N block-correlated distribution.

### 2. Correlation leakage

Within an E8 block, coordinates are constrained by lattice geometry. Attackers
know block boundaries and all public parameters. Tests must measure whether
those correlations improve distinguishing, primal/dual, decoding, or hybrid
attacks compared with a standard baseline.

### 3. Automorphism/structure attacks

E8 has a large automorphism/Weyl group. Symmetry may improve implementation or
sampling, but it is also public algebraic structure. The project must test
whether it reduces effective entropy or creates equivalent targets that help an
attacker.

### 4. Decryption failure

A denser short-vector geometry could improve quantization/reconciliation, but
changing tails and correlation can also worsen decryption-failure behavior.
Failure probability must be computed/estimated from the actual distribution,
not inferred from E8's sphere-packing reputation.

### 5. Net benefit

E8-specific structure is justified only if it produces a measurable benefit
such as lower reconciliation failure, smaller ciphertexts, faster decoding, or
another concrete engineering advantage **without weakening the security
assumption**. If the same benefit is available from a standard distribution,
extra E8 structure is unnecessary attack surface.

## Required experiment sequence

Before successor KEM code:

1. define the exact E8 discrete distribution mathematically;
2. implement a test-only sampler isolated from any protocol;
3. verify empirical moments, covariance, symmetry, tails, and block
   independence against the mathematical definition;
4. compare it with a standard centered-binomial/discrete-Gaussian baseline;
5. estimate decryption/reconciliation failure under candidate modulus/noise
   parameters;
6. run known lattice-estimator / primal / dual attack models where the chosen
   distribution can be represented honestly;
7. identify a published hardness theorem that actually matches the distribution
   or document that a new proof would be required.

Only after these steps should `KeyGen`, `Encaps`, and `Decaps` be specified.

## Fallback path

If the E8 error distribution cannot be connected to a credible hardness result,
retain a standard KEM for secrecy and evaluate E8 only as a post-KEM
reconciliation, coding, or quantization component. In that architecture, the
security claim remains with the standard KEM and E8 is judged on engineering
metrics only.

## References

- NIST FIPS 203, *Module-Lattice-Based Key-Encapsulation Mechanism Standard*,
  2024: https://doi.org/10.6028/NIST.FIPS.203
- NIST SP 800-227, *Recommendations for Key-Encapsulation Mechanisms*, final
  2025: https://doi.org/10.6028/NIST.SP.800-227
- O. Regev, *On Lattices, Learning with Errors, Random Linear Codes, and
  Cryptography*, JACM 56(6), 2009 / STOC 2005.
- M. Shao, Y. Liu, Y. Zhou, Y. Shao, *On the Security of LWE-based KEMs under
  Various Distributions: A Case Study of Kyber*, Cryptology ePrint 2024/1979.

## Handoff

The next highest-priority task is to define the exact E8 block error probability
distribution and build distribution-only tests. Do not integrate it into a KEM
until reduction coverage and attack modeling are understood.
