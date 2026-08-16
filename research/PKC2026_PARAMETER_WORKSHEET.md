# PKC 2026 General-Distribution M-LWE — E8 Parameter Worksheet

Status: **theorem audit in progress; no inherited security claim**

## Purpose

Turn the Boudgoust–Jeudy–Tairi–Wen PKC 2026 general-distribution M-LWE result into a falsifiable checklist for the candidate E8 error law.

The candidate one-block law is the truncated discrete Gaussian already fixed in `E8_ERROR_DISTRIBUTION.md`:

\[
P_{s,R}[X=x] = \frac{\exp(-\pi\|x\|_2^2/s^2)}{Z_{s,R}},\qquad
x\in E_8,\ \|x\|_2\le R,
\]

with protocol-facing integer representative `Y=2X` and coefficient-wise reduction modulo `q`.

This worksheet deliberately distinguishes three statuses:

- **PASS** — the condition can be checked from an exact published statement or from the candidate's exact mathematics;
- **FAIL** — a checked condition is violated;
- **UNRESOLVED** — the necessary theorem statement, notation mapping, proof obligation, or quantitative bound has not yet been established.

`UNRESOLVED` is not a soft pass.

## Source-access result

The official Springer PKC 2026 page confirms the published result and states that search M-LWE remains hard when the error vector follows an **arbitrary bounded distribution with sufficient entropy**, with a restriction on the number of samples. The same page also exposes technical notes about norm balls and truncation, but the theorem body containing the quantitative hypotheses is subscription-gated in the accessible HTML. The open HAL record `lirmm-05396885v2` is protected by an anti-bot gate in this execution environment. The IACR full version is ePrint 2025/1472, but its PDF body was likewise not retrievable by the available web/PDF path during this pass.

A later primary research paper comparing its own leakage reduction with BJTW explicitly states that `[BJTW25, Theorem 4.1]` additionally requires a rank-`(m-n)` SIS problem to be sufficiently hard and therefore imposes a lower bound on the number of samples `m`. This is useful structural evidence, but it is **not a substitute for the BJTW theorem body** and does not justify inventing the omitted SIS norm parameter, entropy threshold, or constants.

Therefore this document records the exact equations we can derive for the E8 candidate and the exact qualitative hypotheses visible from the publication, while marking the unavailable quantitative BJTW inequalities as `UNRESOLVED`.

## Candidate-side equations that are exact now

For an E8 shell with squared norm `2j`, the number of vectors is

\[
a_j = 240\,\sigma_3(j).
\]

For the cutoffs used below,

- `||x||^2 = 2`: 240 vectors;
- `||x||^2 = 4`: 2,160 vectors;
- `||x||^2 = 6`: 6,720 vectors;
- `||x||^2 = 8`: 17,520 vectors.

Hence for `J=floor(R^2/2)`,

\[
|S_R| = 1 + \sum_{j=1}^{J} a_j,
\]

\[
Z_{s,R}=1+\sum_{j=1}^{J}a_j\exp(-2\pi j/s^2),
\]

and because zero has maximum probability,

\[
H_\infty(X)=\log_2 Z_{s,R}.
\]

If an M-LWE error vector contains `m*n` coefficient positions and `n` is divisible by eight, grouping them into iid E8 blocks gives

\[
N_{blocks}=\frac{mn}{8},\qquad
H_\infty(E)=\frac{mn}{8}\log_2 Z_{s,R}.
\]

This last equation is valid **only for the proposed coefficient-block interpretation**; whether BJTW permits that interpretation is a separate theorem-domain question.

For `Y=2X`, `||Y||_2 <= 2R`. A sufficient condition for every coordinate to retain its centered integer representative without modular wraparound is

\[
2R < q/2\quad\Longleftrightarrow\quad 4R<q.
\]

This is a serialization/embedding sanity check, not a hardness condition from BJTW.

## BJTW hypothesis ledger

| ID | Hypothesis / proof obligation | Equation or condition currently justified | Status |
|---|---|---|---|
| H1 | Error distribution is bounded | `||X||_2 <= R`; equivalently `||Y||_2 <= 2R` | **PASS** for every finite `R` candidate |
| H2 | Error distribution has sufficient entropy | Candidate value is `H_inf(E)=(mn/8) log2 Z_{s,R}` under iid coefficient blocks; BJTW's required lower bound is not available in the accessible theorem body | **UNRESOLVED** |
| H3 | Number-of-samples restriction | Published abstract confirms a restriction on sample count; a later primary paper states BJTW Thm. 4.1 also requires hardness of rank-`(m-n)` SIS in its LWE notation | **UNRESOLVED** until BJTW notation is mapped exactly to module rank `k`, field degree `n`, and sample count `m` |
| H4 | Auxiliary SIS hardness | Need exact BJTW SIS instance, rank/dimension, norm bound `beta`, modulus and advantage relation | **UNRESOLVED** |
| H5 | Ring/number-field/module domain | Need exact theorem domain and whether an arbitrary distribution over coefficient embeddings is allowed | **UNRESOLVED** |
| H6 | Public E8 block grouping is covered | Must prove that grouping eight coefficients into correlated E8 blocks is merely choosing an allowed arbitrary bounded distribution, not changing the M-LWE algebraic problem | **UNRESOLVED** |
| H7 | Secret-law requirements | Error-only coverage does not automatically justify a future E8 secret; HNF/general secret-error theorem has separate conditions | **UNRESOLVED** |
| H8 | Efficient sampling | The PMF is finite and explicit, but a verified sampler is not yet merged | **UNRESOLVED** operationally |
| H9 | Centered modular embedding does not wrap | Sufficient check `4R < q` | evaluated per tuple below |
| H10 | `n` aligns with 8-coordinate blocks | `8 | n` for simple coefficient-block partitioning | evaluated per tuple below |

## Explicit research tuples

Notation in this repository's worksheet:

- `s`: E8 discrete-Gaussian scale;
- `R`: E8 Euclidean cutoff;
- `q`: modulus;
- `n`: ring/number-field coefficient degree used by the candidate experiment;
- `k`: secret module rank;
- `m`: number of M-LWE sample rows/module elements.

This mapping is **provisional** until matched line-by-line to BJTW's notation.

### Computed candidate quantities

| Candidate | `(s,R,q,n,k,m)` | `|S_R|` | `H_inf(block)` | iid blocks `mn/8` | candidate `H_inf(E)` | `4R<q` | `8|n` |
|---|---|---:|---:|---:|---:|---|---|
| A — small/square | `(1.0, 2, 3329, 256, 2, 2)` | 2,401 | 0.541732 bits | 64 | 34.670836 bits | PASS | PASS |
| B — medium/square | `(1.5, sqrt(6), 3329, 256, 3, 3)` | 9,121 | 4.664308 bits | 96 | 447.773557 bits | PASS | PASS |
| C — medium/+1 sample | `(1.5, sqrt(6), 3329, 256, 3, 4)` | 9,121 | 4.664308 bits | 128 | 597.031410 bits | PASS | PASS |
| D — wide/+1 sample | `(2.0, sqrt(8), 3329, 256, 4, 5)` | 26,641 | 7.890681 bits | 160 | 1,262.508896 bits | PASS | PASS |
| E — wide/512 | `(2.0, sqrt(8), 7681, 512, 4, 5)` | 26,641 | 7.890681 bits | 320 | 2,525.017792 bits | PASS | PASS |

The entropy values above are **candidate min-entropies**, not statements that a BJTW threshold is met.

## PASS / FAIL / UNRESOLVED worksheet

| Candidate | Bounded law | Centered embed | 8-block alignment | BJTW entropy inequality | BJTW sample inequality | BJTW SIS condition | BJTW module/domain match | E8 grouping covered | Overall theorem coverage |
|---|---|---|---|---|---|---|---|---|---|
| A | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | **UNRESOLVED** |
| B | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | **UNRESOLVED** |
| C | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | **UNRESOLVED** |
| D | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | **UNRESOLVED** |
| E | PASS | PASS | PASS | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | **UNRESOLVED** |

### What we can already reject

A tuple **fails this research path** immediately if any of the following hold:

1. `R` is not finite — it no longer satisfies the bounded-distribution premise being investigated;
2. `n` is not divisible by eight while using the current simple coefficient-block embedding and no alternative mapping is specified;
3. the modular representation cannot be decoded as intended because the chosen parameterization permits wraparound in the range claimed by the design;
4. once the exact BJTW entropy lower bound is obtained, `H_inf(E)` falls below it;
5. once the exact BJTW sample/SIS condition is obtained, the tuple does not satisfy it;
6. the theorem domain does not permit the proposed correlated eight-coordinate coefficient distribution without a new reduction.

Items 4–6 are the decisive security-assumption tests and remain unresolved today.

## Why no candidate is marked theorem-PASS yet

The project now knows substantially more than “bounded + entropy might work,” but the exact theorem constants/inequalities needed to turn that into a security reduction were not available through the accessible full-text path in this pass. Marking any tuple PASS would therefore manufacture a theorem statement.

This is itself a useful checkpoint: **E8 has not yet earned a place inside the secrecy assumption.** It remains a candidate only while the BJTW proof obligations are open.

## Decision rule for the next pass

Keep E8 inside the secrecy-core research track only if all of the following become PASS for at least one useful tuple:

1. exact BJTW entropy inequality;
2. exact sample-count restriction;
3. exact auxiliary SIS hardness condition with plausible concrete parameters;
4. exact module/ring-domain compatibility;
5. a written reduction argument showing that iid E8 coefficient blocks are an allowed error distribution under the theorem rather than a changed problem.

If any indispensable condition is proven FAIL for all useful tuples, move E8 out of the secrecy assumption and evaluate it only for reconciliation, coding, or quantization around a standard KEM.

## Next retrieval target

Obtain the full text of ePrint 2025/1472 or the HAL manuscript through a source that exposes the theorem body. Transcribe the relevant theorem(s) **verbatim at the equation level but paraphrased in prose**, preserving variable definitions, then replace every `UNRESOLVED` quantitative cell above with a reproducible calculation.

Do not design successor `KeyGen`, `Encaps`, or `Decaps` while the overall theorem-coverage column is unresolved.
