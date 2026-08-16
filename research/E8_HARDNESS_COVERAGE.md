# E8 Error Distribution — Hardness Coverage Review

Status: **conditional research result; no inherited security claim**

## Question

Does an existing LWE or Module-LWE worst-case/average-case hardness theorem directly cover the candidate truncated E8 block distribution defined in `E8_ERROR_DISTRIBUTION.md`?

## Candidate summarized

One block is sampled from

\[
P_{s,R}[X=x] \propto \exp(-\pi\|x\|^2/s^2)
\]

on the finite set `E8 ∩ B_R(0)`. Blocks are iid. For modular arithmetic the proposed research representation is the integral scaled vector `Y=2X`.

The distribution is therefore:

- finite and bounded;
- centrally symmetric;
- radially weighted;
- isotropic in covariance by E8 Weyl symmetry;
- correlated within each 8-coordinate block;
- independent across blocks by definition.

## Classic LWE result

Regev's foundational LWE reduction and later standard LWE reductions use specific Gaussian error formulations. They establish the importance of Gaussian-type error but do not provide a direct theorem saying that an arbitrary block-correlated finite distribution may replace the specified error law.

**Result:** classic LWE Gaussian reductions are **not direct coverage** for the proposed truncated E8 block distribution.

## Standard Module-LWE result

Langlois and Stehle's Module-LWE worst-case/average-case framework gives hardness for Module-LWE under its stated module/ring and error-distribution conditions. The standard theoretical formulation is Gaussian in the appropriate module/ring embedding. The fact that E8 is a lattice and the PMF is radially exponential does not make the proposed coefficient-block distribution identical to that Gaussian formulation.

**Result:** the standard Module-LWE reduction is **not yet direct coverage** for the E8 coefficient-block substitution.

## PKC 2026 general-distribution result

A materially relevant new result exists:

Katharina Boudgoust, Corentin Jeudy, Erkan Tairi, and Weiqiang Wen, *Hardness of M-LWE with General Distributions and Applications to Leaky Variants*, PKC 2026, pp. 3–37, DOI `10.1007/978-3-032-26731-3_1` (full version ePrint 2025/1472).

The authors state that M-LWE remains hard when the error vector follows an **arbitrary bounded distribution with sufficient entropy**, with restrictions including the number of samples. This is substantially more general than the older Gaussian-only theoretical baseline and is potentially relevant to a truncated E8 distribution.

Our candidate is bounded, so it passes the first qualitative filter. Its min-entropy is explicitly computable from its normalization constant:

\[
H_\infty(X)=\log_2 Z_{s,R}.
\]

For iid blocks, min-entropy adds.

However, qualitative similarity is not theorem verification.

## Conditions still requiring exact verification

Before claiming the PKC 2026 theorem covers this E8 candidate, the repository must extract and check the paper's exact hypotheses for a proposed parameter tuple. At minimum:

1. **Domain:** verify that the arbitrary distribution may live in exactly the module/ring representation where the E8-derived coefficient vector is placed.
2. **Entropy:** evaluate the theorem's required entropy lower bound and compare it with the candidate distribution's min-entropy after embedding.
3. **Bound:** compare the theorem's required norm/support bound with the scaled E8 cutoff `2R` and modulus.
4. **Samples:** satisfy the theorem's stated sample-count restriction.
5. **Dimensions:** satisfy its number-field degree/module-rank conditions.
6. **Embedding:** prove that grouping coefficients into public 8-coordinate E8 blocks is still an instance of the theorem's allowed arbitrary distribution rather than an unproved structural transformation.
7. **Secret law:** verify the future secret distribution separately; coverage of an error law does not automatically justify whatever secret law a future KEM chooses.
8. **Concrete security:** even theorem coverage would not provide a concrete attack estimate for a new structured distribution and parameter set.

No `(s,R,q,n,k,m)` parameter tuple has yet been checked against all of those conditions.

## Current verdict

**Not proven covered; not proven impossible.**

The earlier research note said no published reduction had been established for the E8-block idea. That remains true as a repository security claim, but the literature search has found a stronger opportunity than previously recorded: the PKC 2026 general-distribution theorem may cover bounded E8 errors if its quantitative hypotheses and representation model are satisfied.

Therefore this project SHALL NOT:

- claim E8 errors inherit ML-KEM security;
- cite E8 density or Weyl symmetry as a hardness proof;
- implement a successor KEM before the theorem conditions are checked;
- silently replace the theorem's ring/module distribution with an 8-coordinate coefficient construction.

## Fallback decision

If no useful E8 parameter tuple satisfies the theorem's hypotheses, or if the necessary embedding changes the problem outside the theorem, record that as a negative result. In that case E8 should move outside the secrecy assumption and be evaluated only as a reconciliation, coding, or quantization layer around a standard KEM.

## Sources checked

- O. Regev, *On Lattices, Learning with Errors, Random Linear Codes, and Cryptography*.
- A. Langlois, D. Stehle, *Worst-case to average-case reductions for module lattices*, Designs, Codes and Cryptography 75 (2015), 565–599.
- K. Boudgoust, C. Jeudy, E. Tairi, W. Wen, *Hardness of M-LWE with General Distributions and Applications to Leaky Variants*, PKC 2026, 3–37.
- NIST FIPS 203, *Module-Lattice-Based Key-Encapsulation Mechanism Standard*.

## Handoff

The next pass should obtain the full PKC 2026 theorem statement and turn its hypotheses into a parameter-check worksheet. Then choose small research candidates `(s,R,q,n,k,m)`, compute support/min-entropy and scaled norm bounds, and mark each theorem hypothesis PASS/FAIL/UNRESOLVED. A KEM specification remains blocked until at least one useful tuple passes without an unproved embedding step.
