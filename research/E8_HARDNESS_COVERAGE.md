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

The distribution is therefore finite, bounded, centrally symmetric, radially weighted, isotropic in covariance by E8 Weyl symmetry, correlated within each 8-coordinate block, and independent across blocks by definition.

## Classic LWE result

Regev's foundational LWE reduction and later standard LWE reductions use specific Gaussian error formulations. They do not provide a direct theorem saying that an arbitrary block-correlated finite distribution may replace the specified error law.

**Result:** classic LWE Gaussian reductions are **not direct coverage** for the proposed truncated E8 block distribution.

## Standard Module-LWE result

Langlois and Stehle's Module-LWE worst-case/average-case framework gives hardness under its stated module/ring and error-distribution conditions. The fact that E8 is a lattice and the PMF is radially exponential does not make the proposed coefficient-block distribution identical to the theorem's standard Gaussian formulation.

**Result:** the standard Module-LWE reduction is **not direct coverage** for the E8 coefficient-block substitution.

## PKC 2026 general-distribution result

Katharina Boudgoust, Corentin Jeudy, Erkan Tairi, and Weiqiang Wen, *Hardness of M-LWE with General Distributions and Applications to Leaky Variants*, PKC 2026, pp. 3–37, DOI `10.1007/978-3-032-26731-3_1` (full version ePrint 2025/1472), state that search M-LWE remains hard when the error vector follows an **arbitrary bounded distribution with sufficient entropy**, with a restriction on the number of samples.

The candidate is bounded and has explicitly computable min-entropy, so this theorem family is materially relevant. But qualitative similarity is not theorem verification.

## Parameter worksheet

`research/PKC2026_PARAMETER_WORKSHEET.md` is now the authoritative Gate-2 theorem audit. It contains five explicit `(s,R,q,n,k,m)` candidates and marks every condition **PASS**, **FAIL**, or **UNRESOLVED**.

Candidate-side quantities currently checked include:

- exact E8 shell/support sizes for the selected cutoffs;
- `Z_{s,R}` and `H_inf(block)=log2 Z_{s,R}`;
- total candidate min-entropy under the proposed iid coefficient-block interpretation;
- block alignment `8 | n`;
- the sufficient centered no-wrap check `4R < q` for `Y=2X`.

All five candidates pass those candidate-side sanity checks. **None is marked theorem-PASS.**

## Theorem retrieval limitation recorded, not hidden

The official Springer page exposes the publication abstract and technical notes but gates the theorem body in this environment. The HAL manuscript `lirmm-05396885v2` is also blocked here by its anti-bot access layer. A later primary research paper explicitly reports that `[BJTW25, Theorem 4.1]` requires an auxiliary rank-`(m-n)` SIS problem to remain hard, confirming that sample count is coupled to an additional hardness obligation, but that secondary statement is not enough to reconstruct BJTW's omitted norm bound, entropy threshold, constants, or exact module notation.

The repository therefore refuses to fabricate those inequalities. They remain `UNRESOLVED` until the full theorem body is obtained.

## Conditions still requiring exact verification

1. **Entropy:** the exact BJTW min-entropy lower bound.
2. **Samples:** the exact sample-count interval/restriction and notation mapping.
3. **Auxiliary SIS:** the exact SIS rank/dimension, norm bound, modulus, and hardness requirement.
4. **Domain:** the theorem's ring/number-field/module representation.
5. **Embedding:** whether public 8-coordinate coefficient grouping is an allowed arbitrary distribution rather than an unproved problem transformation.
6. **Secret law:** separate conditions if a future construction also changes the secret distribution.
7. **Concrete security:** attack estimates remain necessary even if asymptotic theorem coverage succeeds.

## Current verdict

**Not proven covered; not proven impossible.**

E8 has not yet earned a place inside the secrecy assumption. The project now has enough candidate-side mathematics to evaluate the theorem immediately once its exact quantitative statement is available, but it will not treat the word “arbitrary” in the abstract as permission to skip the theorem's entropy, sample, SIS, or algebraic-domain hypotheses.

## Fallback decision

If no useful E8 parameter tuple satisfies every indispensable theorem hypothesis, or if the E8 coefficient-block embedding changes the problem outside the theorem, record that as a negative result. In that case E8 moves outside the secrecy assumption and is evaluated only as a reconciliation, coding, or quantization layer around a standard KEM.

## Sources checked

- O. Regev, *On Lattices, Learning with Errors, Random Linear Codes, and Cryptography*.
- A. Langlois, D. Stehle, *Worst-case to average-case reductions for module lattices*, Designs, Codes and Cryptography 75 (2015), 565–599.
- K. Boudgoust, C. Jeudy, E. Tairi, W. Wen, *Hardness of M-LWE with General Distributions and Applications to Leaky Variants*, PKC 2026, 3–37 / ePrint 2025/1472.
- NIST FIPS 203, *Module-Lattice-Based Key-Encapsulation Mechanism Standard*.

## Handoff

Obtain the full BJTW theorem body through ePrint, HAL, or an author-provided full-text path. Preserve its exact variable definitions and quantitative inequalities in `PKC2026_PARAMETER_WORKSHEET.md`, then evaluate each candidate cell reproducibly. If every useful tuple fails an indispensable condition, formally close the secrecy-core E8 track and begin reconciliation/coding experiments.
