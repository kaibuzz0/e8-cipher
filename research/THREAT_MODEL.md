# E8 Successor Research Threat Model

Status: **research specification, not a security claim**

This document defines what a successor to the archived v2 experiment would
have to protect. It deliberately separates a security target from the open
question of whether E8 contributes anything useful to meeting that target.

## 1. Intended primitive

The primary target is a **key-encapsulation mechanism (KEM)**, not direct bulk
message encryption. A successful KEM establishes a shared secret over a public
channel; a standard authenticated-encryption scheme can then protect application
data. This matches the modern separation used by NIST SP 800-227 and FIPS 203.

The research name `E8-KEM` is only a placeholder. No algorithm in this
repository currently satisfies this specification.

## 2. Security target

A candidate must ultimately target **IND-CCA security** for encapsulation: an
attacker that can obtain a public key, request chosen encapsulations, and query
a decapsulation oracle on arbitrary ciphertexts other than the challenge must
not distinguish the challenge shared secret from random with non-negligible
advantage.

Earlier experimental stages may measure IND-CPA-style properties, but passing
those experiments is not sufficient for a candidate KEM.

The design must also provide:

- **cross-key isolation**: compromise or possession of one key pair must not
  enable decapsulation under an unrelated key pair;
- **fresh encapsulation randomness** from an OS-backed CSPRNG in production;
- **implicit rejection / robust invalid-ciphertext handling** appropriate to a
  CCA-secure KEM construction;
- **domain separation** for every hash/KDF role;
- **strict, versioned serialization** with rejection of malformed encodings;
- **no secret-derived public nonce or randomness seed**;
- **no global mutable PRNG state** in cryptographic operations;
- a documented plan for side-channel-resistant implementation if the research
  reaches implementation maturity.

## 3. Adversary capabilities

Assume the attacker can:

1. read all source code, specifications, parameters, public matrices, and test
   vectors;
2. obtain arbitrarily many public keys and ciphertexts;
3. choose plaintext/application inputs around the KEM and compare repeated
   executions;
4. perform known-plaintext, chosen-ciphertext, multi-target, and cross-key
   experiments;
5. run lattice reduction and decoding attacks, including LLL/BKZ-class tools;
6. exploit all algebraic structure intentionally introduced by E8, direct sums,
   automorphisms, module structure, or correlated sampling;
7. use large classical compute and, for the intended post-quantum claim,
   polynomial-time quantum algorithms where applicable;
8. observe public timing, ciphertext lengths, rejection behavior, and other
   externally visible metadata.

The attacker does **not** get to read secret memory directly in the abstract
cryptographic model. Memory disclosure, fault attacks, and invasive physical
attacks belong to later implementation-security analysis.

## 4. Explicitly rejected legacy assumptions

The successor must not inherit any of the following v2 ideas as security
arguments:

- a fixed or reconstructable "good basis" shared across keys;
- security merely because a public basis has a high condition number;
- deterministic reseeding of encryption randomness from the private key;
- a private-seed-derived value presented as a nonce;
- successful round-trip encryption as evidence of security;
- calling a simplified orthogonal sublattice "E8";
- assuming larger dimension alone creates a concrete security level.

These failures are preserved in `tests/test_legacy_failures.py`.

## 5. Baseline for comparison

FIPS 203 specifies ML-KEM and relates its security to the Module Learning With
Errors problem. The E8 research must therefore compare any candidate against a
well-understood Module-LWE baseline rather than against the archived GGH
prototype.

References:

- NIST FIPS 203, *Module-Lattice-Based Key-Encapsulation Mechanism Standard*,
  2024: https://doi.org/10.6028/NIST.FIPS.203
- NIST SP 800-227, *Recommendations for Key-Encapsulation Mechanisms*, final
  2025: https://doi.org/10.6028/NIST.SP.800-227
- O. Regev, *On Lattices, Learning with Errors, Random Linear Codes, and
  Cryptography*, JACM 2009 / STOC 2005.

The existence of ML-KEM does not imply that an E8-modified distribution or
module automatically inherits ML-KEM security.

## 6. Candidate E8 roles to evaluate

### A. GGH-style E8 trapdoor

**Current disposition: reject as the successor direction.**

The repository already demonstrates catastrophic key-separation and randomness
failures in its particular legacy implementation, and generic GGH-style public
basis hiding is historically vulnerable to lattice reduction. Genuine E8 math
fixes the mislabeled geometry but does not repair the missing modern security
reduction.

### B. E8-shaped LWE / Module-LWE error geometry

**Disposition: research hypothesis, not yet accepted.**

The idea is to sample short error vectors using genuine E8 geometry while the
public equations follow an LWE/Module-LWE-style construction. This is the most
direct way E8 might affect the hardness/performance tradeoff.

Major unresolved question: a correlated or nonstandard E8 error distribution
must be tied to an appropriate hardness theorem. It cannot simply be called
"Module-LWE" because it visually resembles an LWE construction. Before code is
written, the project must determine whether the proposed distribution satisfies
known reduction requirements or whether a new proof would be required.

### C. E8 quantization/coding outside the hardness core

**Disposition: safe experimental fallback.**

E8 can be tested as a quantizer, reconciliation code, or error-correction layer
around a standard KEM. In this role, the cryptographic security claim remains
with the standardized KEM; E8 is evaluated for bandwidth, decoding, or noise
handling rather than claimed as the source of secrecy.

This path can produce useful engineering even if E8 fails to improve the
underlying hardness assumption.

### D. Ring/Module-E8 algebraic construction

**Disposition: long-term speculative research.**

Embedding E8 coefficients into a polynomial/module construction may offer fast
algebra, but added structure can also create attacks. No implementation should
be described as secure until the exact algebra, distributions, and reduction are
specified independently of code.

## 7. Decision rule for the next construction step

The next research pass should investigate candidate **B** first because it is
the clearest route by which E8 could contribute to a post-quantum hardness
construction rather than merely sit beside one.

Before implementing a KEM, it must answer:

1. What exact probability distribution is used for an E8-shaped error sample?
2. Are coordinates independent, block-correlated, or sampled from a discrete
   Gaussian over E8?
3. Which published LWE/Module-LWE hardness result, if any, covers that
   distribution and parameter regime?
4. What information about E8 block boundaries or automorphisms becomes visible
   to the attacker?
5. Does E8 shaping improve decoding failure probability, key/ciphertext size,
   or performance enough to justify extra structure?
6. Can the same benefit be obtained with a standard distribution without the
   additional attack surface?

If no credible hardness connection can be established, candidate B must be
recorded as a negative result and the project should move to candidate C or
conclude that E8 does not improve encryption security.

## 8. Success and failure criteria

A successful Gate 2 design is not "code that encrypts." It is a specification
with KeyGen, Encaps, and Decaps algorithms, exact distributions and parameters,
a named hardness assumption, and a falsifiable security argument.

Gate 2 fails constructively if the E8-specific component cannot be tied to a
credible hardness assumption or only adds exploitable structure. That result
must be documented rather than hidden by increasing dimensions or adding more
mixing layers.
