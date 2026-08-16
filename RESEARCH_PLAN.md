# E8 Cipher Research Program

## Mission

Determine whether genuine E8 lattice structure can contribute useful, defensible cryptographic properties to an encryption or key-encapsulation design. The project succeeds only if the claims are supported by mathematics, adversarial testing, reproducible code, and external-review-ready documentation.

This repository is **research software, not production cryptography** until a construction has a credible reduction to a well-studied hardness assumption and survives independent cryptanalysis.

## Non-negotiable research rules

1. Separate mathematical facts from security hypotheses.
2. Never infer security from encrypt/decrypt round trips.
3. Never use deterministic or secret-derived randomness as encryption randomness.
4. Every private key must create genuinely independent secret material.
5. Do not call a structure E8 unless invariants for the E8 lattice/root system are verified.
6. Prefer standard primitives for components that are not the object of the research (CSPRNG, SHA-2/SHA-3, HKDF, AEAD).
7. Publish negative results. A disproved design is a useful research result.

## Research gates

### Gate 0 — Correct mathematical substrate

- [x] Construct all 240 E8 roots explicitly.
- [x] Add a full-rank determinant-1 E8 basis.
- [x] Verify every root has squared norm 2.
- [x] Verify all generated roots satisfy E8 lattice membership rules.
- [x] Verify lattice covolume / Gram determinant is 1.
- [ ] Add exact/rational verification to remove dependence on float tolerances.
- [ ] Add E8 Weyl reflections over the full 240-root system.
- [ ] Verify reflections preserve root membership and norms.
- [ ] Add E8^N direct-sum construction with explicit invariants.

**Exit criterion:** mathematical tests demonstrate that all objects labeled E8 are actually E8-derived.

### Gate 1 — Legacy cipher containment

- [ ] Add regression test proving the old fixed decoding basis can be reconstructed.
- [ ] Add regression test proving the old encrypt() reuses its RNG stream.
- [ ] Mark legacy cipher API as insecure/deprecated in runtime and docs.
- [ ] Remove private-seed-derived pseudo-nonce from any successor design.
- [ ] Decide whether legacy code remains only as a documented broken-design specimen.

**Exit criterion:** known catastrophic failures are captured as tests and cannot silently re-enter a successor design.

### Gate 2 — Threat model and construction choice

- [ ] Define attacker capabilities and target security properties (IND-CPA / IND-CCA / KEM security).
- [ ] Decide whether the E8 contribution belongs in a GGH-like trapdoor, LWE/Module-LWE error geometry, coding layer, or another primitive.
- [ ] Reject any design whose secret is reconstructable from public parameters.
- [ ] Write the exact algorithms for KeyGen, Encaps/Encrypt, Decaps/Decrypt before implementation.
- [ ] Identify the standard hardness assumption to which security should reduce.

**Exit criterion:** a written construction exists that can be attacked and reviewed independently of code.

### Gate 3 — Reference implementation

- [ ] Implement the candidate construction separately from legacy v2 code.
- [ ] Use OS/CSPRNG randomness and domain-separated KDF inputs.
- [ ] Add serialization with versioning and strict validation.
- [ ] Add malformed-ciphertext handling and constant-time design notes.
- [ ] Add known-answer vectors and deterministic test-only RNG injection.

**Exit criterion:** reference code is reproducible, testable, and does not depend on global RNG state.

### Gate 4 — Adversarial verification

- [ ] Differential/known-plaintext tests.
- [ ] Cross-key isolation tests.
- [ ] Nonce/randomness reuse tests.
- [ ] LLL/BKZ experiments using a mature lattice library where practical.
- [ ] Parameter sweeps with reproducible seeds.
- [ ] Mutation/fuzz tests for parsers and ciphertext handling.
- [ ] Statistical tests for error/sampling distributions.
- [ ] Compare attack cost against contemporary standardized PQC baselines.

**Exit criterion:** no known trivial break; concrete attack estimates are documented. This does not by itself prove security.

### Gate 5 — Cryptographic review readiness

- [ ] Formal specification with notation and pseudocode.
- [ ] Security argument/reduction reviewed for unstated assumptions.
- [ ] Reproducible benchmark suite.
- [ ] Side-channel assessment.
- [ ] Independent implementation or external review.
- [ ] Publish negative and positive results.

**Success criterion:** a defensible construction with working code and evidence strong enough to justify external cryptographic review.

**Failure criterion:** evidence shows E8 adds no useful security, creates exploitable structure, or cannot be tied to a credible hardness assumption. If so, document that result rather than forcing a protocol.

## Five-hour pass handoff

Each research pass should:

1. Read this file and inspect current open PRs/issues.
2. Select the highest-priority unchecked item whose prerequisites are complete.
3. Make one coherent, reviewable change.
4. Run the relevant tests/analysis.
5. Record evidence in code, tests, or `docs/` rather than only in prose comments.
6. Update checkboxes only when the claimed verification actually exists.
7. Leave the next highest-priority item obvious to the following pass.

## Website

The static research site lives under `docs/`. It should present:

- current research gate and status;
- verified mathematical invariants;
- known breaks and negative results;
- candidate protocol architecture when one exists;
- test/benchmark evidence;
- explicit distinction between verified facts and hypotheses.
