# PKC 2026 Author-Slides Audit

Status: **primary-source theorem evidence; not a security proof**

## Purpose

Record what can be established directly from Katharina Boudgoust's July 14, 2026 presentation, *Hardness of M-LWE with General Distributions and Applications to Leaky Variants*, and separate that evidence from conditions that still require the full theorem body of Boudgoust–Jeudy–Tairi–Wen (BJTW), PKC 2026 / ePrint 2025/1472.

This document does not replace `PKC2026_PARAMETER_WORKSHEET.md`. It raises the confidence of several qualitative cells and records one concrete author-provided parameter example.

## Primary-source facts established by the July 2026 slides

The author states that **search MLWE** with a general noise distribution `D` and a **uniform secret** is as hard as standard MLWE provided that:

1. `D` has sufficient min-entropy;
2. samples from `D` are short;
3. not too many samples are provided.

The slides separately state that combining the error result with Hermite Normal Form can yield a general secret-noise distribution.

The presentation also gives a concrete sanity-check application for a sparse ternary error distribution:

- ring degree `n = 256`;
- modulus `q = 2113`;
- density `rho = 0.1`;
- **minimal module rank `r = 104`** for that example.

This is not a universal lower bound for arbitrary bounded distributions. It is, however, strong evidence that the known reduction can require module ranks far larger than practical ML-KEM-style ranks for some concrete distributions.

## Proof-shape evidence

The author presentation sketches the reduction through an M-Knapsack / one-way-function route. It describes second-preimage resistance by considering whether another support element `x' != x` can satisfy the same linear image, with a union-bound style probability over the support. The slide explicitly notes that this bound is "very loose".

The same presentation states that the theoretical robustness result is primarily meaningful for **large rank**, and lists important uncovered cases including decision MLWE with general errors and RLWE-style low-rank settings.

## Implications for the E8 candidate

### What improves from UNRESOLVED to source-confirmed

The following qualitative requirements are now directly supported by an author source:

- target problem: **search MLWE**, not decision MLWE;
- initial general-error theorem uses a **uniform secret**;
- the error distribution must have **sufficient min-entropy**;
- error samples must be **short**;
- there is an upper restriction on the number of samples;
- HNF is a separate step for moving toward a general secret-error law;
- large module rank can be required in concrete applications of the reduction.

### What remains unresolved

The slides do **not** provide enough equation-level detail to mark an E8 tuple theorem-PASS. The repository still needs the full BJTW theorem statement to obtain:

1. the exact min-entropy inequality;
2. the exact shortness/norm inequality and norm convention;
3. the exact sample-count inequality;
4. the auxiliary SIS instance and quantitative hardness requirement;
5. the precise mapping of paper variables to repository `(s,R,q,n,k,m)` notation;
6. proof that public iid 8-coordinate E8 coefficient blocks are an allowed arbitrary distribution in the theorem's module domain;
7. the exact hypotheses of the HNF step if a non-uniform E8-shaped secret is ever considered.

## Current decision

**E8 remains outside any established secrecy claim.**

The author slides strengthen the plausibility that a bounded, sufficiently entropic E8 error law could fit the *shape* of the BJTW search-MLWE theorem. They simultaneously strengthen the warning that the reduction may only become useful at module ranks much larger than the repository's current illustrative `k = 2..4` tuples.

Therefore:

- do not call any existing E8 tuple theorem-covered;
- do not infer decision-MLWE or IND-CCA KEM security from the search-MLWE result;
- do not treat the sparse-ternary `r = 104` example as an E8-specific bound;
- do use it as evidence that rank inflation is a real reduction cost that must be measured before E8 is retained in the secrecy core.

## Evidence hierarchy

1. **Primary author slides, July 14, 2026** — qualitative theorem conditions and sparse-ternary parameter example.
2. **IACR ePrint 2025/1472 metadata/abstract, revised February 25, 2026** — confirms the paper/revision and the bounded-distribution / sufficient-entropy / sample-restriction claim.
3. `research/PKC2026_PARAMETER_WORKSHEET.md` — repository calculations for the E8 candidate; these remain candidate-side calculations until theorem variables are mapped exactly.

## Next handoff

Obtain equation-level text for the revised BJTW theorem and its supporting definitions. The first priority is the exact entropy, shortness, sample-count, and SIS conditions. Then re-evaluate the current E8 tuples and add at least one **large-rank comparison tuple** so the worksheet can test whether the reduction is only theoretically applicable at impractical rank.
