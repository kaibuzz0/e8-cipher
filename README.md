# E8-Cipher v2.0: Lattice-Based Encryption using E8^N

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **E8^N Direct-Sum Lattice Encryption — A Correct Implementation of the GGH Framework**

## 🔬 Mathematical Foundation

The E8 exceptional Lie group provides:
- **240 root vectors** in 8-dimensional space
- **696,729,600 Weyl group symmetries**
- **Densest sphere packing** in 8D (optimal lattice structure)

This implementation extends E8 to **E8^N** (direct sum of N copies), creating a lattice in **8N dimensions** where:
- The **Closest Vector Problem (CVP)** with a bad basis is believed to be hard
- **Babai's nearest plane algorithm** with a good basis enables efficient decryption
- A **unimodular transformation** hides the good basis, creating a public/private key pair

## 🚀 Quick Start

```bash
pip install numpy
python e8_cipher.py
```

```python
from e8_cipher import E8Cipher

# Create cipher with 32-byte private seed
cipher = E8Cipher(private_seed=b'secret-key-32-bytes-long!!!')

# Encrypt
encrypted = cipher.encrypt(b"Hello Quantum World!")

# Decrypt (requires same private key)
decrypted = cipher.decrypt(encrypted)
```

## 📐 Architecture

```
Private Key:  good_basis (short, orthogonal E8^N vectors)
Public Key:   public_basis = U @ good_basis (bad, long, unimodular-transformed)

Encryption:   c = r @ public_basis + m + e
  - r: random integer coefficients
  - m: message encoded as lattice perturbation
  - e: small Gaussian noise (σ = 0.05)

Decryption:   nearest_lattice = Babai(good_basis, c)
              recovered = c - nearest_lattice
              round to nearest byte
```

### Why This Works

1. **With the good basis:** Babai nearest-plane efficiently finds the closest lattice point because the basis is nearly orthogonal.

2. **With only the public basis:** The unimodular transformation `U` creates highly non-orthogonal vectors. Finding the nearest lattice point becomes the CVP, which is believed to be hard in high dimensions.

## ⚙️ Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `N` | 16 | E8 blocks (total dimension = 8N) |
| `scale` | 1200 | Lattice spacing (must be > 722 for arbitrary bytes) |
| `noise_sigma` | 0.05 | Gaussian noise standard deviation |

**Security vs Performance:**
- `N=16` (128D): Fast, educational
- `N=64` (512D): Approaches practical hardness
- `N=128` (1024D): Comparable to Kyber-1024 dimensionality

## 🧪 Testing

```bash
python e8_core.py
```

Runs 8 comprehensive tests:
1. Unimodular matrix generation (det = ±1)
2. E8^N lattice initialization
3. Babai nearest plane correctness
4. Encrypt/decrypt round-trip (multiple messages)
5. Larger dimension (N=8, 64D)
6. Deterministic key generation
7. E8 Weyl transform for hashing
8. Public/private key export

## ⚠️ Security Disclaimer

**This is a demonstration and research implementation.**

- Uses the **GGH framework**, which has known weaknesses against lattice-reduction attacks
- **NOT NIST-approved** — for production use, choose CRYSTALS-Kyber or Dilithium
- The E8^N structure may have algebraic weaknesses not yet analyzed
- No formal security proof is provided

**Use for:**
- ✅ Educational purposes
- ✅ Research into lattice cryptography
- ✅ Prototyping E8-based primitives
- ✅ Blockchain commitment schemes (Weyl transform hashing)

**Do NOT use for:**
- ❌ Protecting real secrets in production
- ❌ Replacing standard post-quantum algorithms
- ❌ Anything requiring formal security guarantees

## 📊 Performance Benchmarks

All benchmarks run on Termux/Android (ARM64), Python 3.11, NumPy 2.4.6:

### Key Generation

| N | Dimension | Time | Public Key Size |
|---|-----------|------|-----------------|
| 4 | 32D | ~140 ms | 8 KB |
| 16 | 128D | ~24 ms | 128 KB |
| 64 | 512D | ~171 ms | 2.0 MB |

### Encryption / Decryption Throughput

| N | Dimension | Encrypt 1 KB | Decrypt 1 KB | Ciphertext Expansion |
|---|-----------|-------------|-------------|---------------------|
| 4 | 32D | ~4 ms | ~4 ms | ~20× |
| 16 | 128D | ~3 ms | ~2 ms | ~20× |
| 64 | 512D | ~4 ms | ~5 ms | ~20× |

**Notes:**
- Ciphertext expansion is fixed at ~20× due to JSON float64 serialization overhead.
- Keygen variance is high for small N because unimodular matrix generation is randomized.
- At N=64 (512D), operations are fast enough for real-time messaging on mobile hardware.
- Higher N = exponentially larger public keys but similar per-byte encrypt/decrypt cost due to block-diagonal structure.

## 📖 API Documentation

### `E8Cipher`

```python
from e8_cipher import E8Cipher
```

#### Constructor

```python
cipher = E8Cipher(
    private_seed: bytes = None,  # 32-byte seed; random if omitted
    N: int = 16,                # E8 blocks (dimension = 8*N)
    scale: float = 1200.0,      # Lattice spacing
    perturbation: np.ndarray = None  # Optional custom perturbation matrix
)
```

**Parameters:**
- `private_seed` — 32-byte secret seed. Same seed always produces the same key pair.
- `N` — Number of E8 copies. Default 16 (128 dimensions). Higher = more secure, slower.
- `scale` — Lattice cell spacing. Must be > 722 to avoid Babai decoding failure on arbitrary bytes.
- `perturbation` — Optional dense perturbation matrix added to `good_basis` before unimodular transform.
  Prevents secret basis vectors from appearing verbatim in the public basis.
  If omitted, a deterministic ~1%-scale perturbation is auto-generated.

#### Methods

**`encrypt(plaintext: bytes) → dict`**

Encrypt arbitrary bytes. Returns a JSON-serializable dict:

```python
{
    "ciphertext": [[float, ...], ...],   # List of float64 arrays
    "nonce": "hex_nonce",
    "pad_len": 0,
    "params": {
        "N": 16,
        "scale": 1200.0,
        "dim": 128,
        "version": "2.0.0"
    }
}
```

**`decrypt(encrypted_data: dict) → bytes`**

Decrypt ciphertext dict back to original plaintext.

**`get_public_key() → dict`**

Export public key (safe to share):

```python
{
    "public_basis": [[...], ...],  # 8N × 8N matrix
    "N": 16,
    "scale": 1200.0,
    "dim": 128
}
```

**`get_private_key() → dict`**

Export private key (**keep secret**):

```python
{
    "private_seed": "hex_seed",
    "good_basis": [[...], ...],     # Short orthogonal basis
    "unimodular": [[...], ...],     # U matrix
    "N": 16,
    "scale": 1200.0
}
```

### `E8Core` Classes (Advanced)

```python
from e8_core import E8Lattice, E8Cipher, E8WeylTransform, generate_unimodular
```

#### `generate_unimodular(n, operations=200, max_multiplier=5, seed=None)`

Generate a random n×n unimodular integer matrix (det = ±1) via elementary row operations.

#### `E8Lattice(N=16, scale=1200.0, public_basis=None, unimodular=None)`

Core lattice object. Manages good basis, public basis, and Babai nearest-plane decoding.

**Key Methods:**
- `babai_nearest_plane(target)` → `(lattice_point, coefficients)`
- `encode_bytes(data)` → perturbation vector
- `decode_bytes(vector, original_len)` → recovered bytes
- `hash_to_point(data)` → deterministic E8^N point
- `weyl_reflection(point, root_idx)` → reflected point

#### `E8WeylTransform(N=16)`

Deterministic hash primitive using E8 symmetries.

- `transform(data, seed)` → 32-byte SHA256 hash

Useful for blockchain commitments and checksums where E8 structure provides mixing.

#### `E8MerkleHasher(N=16)`

Full **Merkle-Damgård hash function** using E8 Weyl symmetries as the compression core.

- `hash(message)` → 32-byte hash digest
- `hash_hex(message)` → hex string

```python
from e8_core import E8MerkleHasher

hasher = E8MerkleHasher(N=4)
digest = hasher.hash(b"Hello E8")
```

Architecture:
- Block size: 32 bytes (SHA256 output size)
- IV: Deterministic E8-derived seed
- Compression: `state = SHA256(WeylTransform(state ⊕ block, seed=block_hash) + state + block)`
- Passes avalanche test (~50% bit flip on single-byte change)

**Note:** This is a custom hash primitive, not a NIST-approved hash function.
Use for research, blockchain commitments, or as a mixing layer — not for
applications requiring SHA-3/BLAKE3 guarantees.

### `run_lattice_security_analysis(N_values)`

Run automated LLL reduction and vulnerability assessment:

```python
from e8_core import run_lattice_security_analysis

results = run_lattice_security_analysis(N_values=[4, 8, 16])
# Prints per-dimension metrics: RHF, LLL time, security estimate
```

Outputs:
- Pre/post-LLL shortest vector lengths
- Hermite factor and root Hermite factor
- Estimated security interpretation (VULNERABLE / MODERATE / STRONG)

## 🗺️ Roadmap

### v2.1 — Lattice Hardening (Complete)
- [x] Implement **perturbation matrix** to prevent verbatim secret basis vectors in public basis
- [x] Add **LLL lattice reduction self-test** to measure public-basis vulnerability
- [x] Add **E8 Merkle-Damgård hash function** for blockchain commitments
- [ ] Add **BKZ approximation** test to quantify higher-block-size attack cost
- [ ] Measure **Hermite factor** of public basis vs dimension with perturbation
- [ ] Add **parameter recommendations** based on measured attack thresholds

### v2.2 — Performance & Compression (Short Term)
- [ ] Optimize Babai nearest-plane with **block-parallel NumPy** operations
- [ ] Add **ciphertext compression** to reduce the 20× expansion penalty (raw bytes instead of JSON)
- [ ] Add **streaming encryption** for large files (process block by block)
- [ ] Benchmark memory usage for N=64 and N=128

### v2.5 — Algebraic Structure (Medium Term)
- [ ] Replace D8 sublattice with **full E8 root lattice** (include half-integer Type 2 roots)
- [ ] Explore **E8 module structure** over polynomial rings (Ring-E8 analog of Ring-LWE)
- [ ] Implement **Gaussian sampling** over E8 cells using discrete Gaussian distributions
- [ ] Add **rejection sampling** for constant-time operations
- [ ] Investigate **E8 automorphism group** for additional public-key hardening

### v2.6 — Hybrid Modes (Medium Term)
- [ ] Build **E8 + AES hybrid mode**: Use E8 for key encapsulation, AES-256-GCM for bulk data
- [ ] Implement **E8-based digital signatures** via hash-and-sign or Fiat-Shamir
- [ ] Add **threshold decryption**: split private key among N parties via lattice secret sharing
- [ ] Create **E8 error-correcting code** layer for noisy-channel robustness

### v3.0 — Production Path (Long Term)
- [ ] Formal security analysis with **reduction proof** to known lattice problems
- [ ] Side-channel resistant implementation (constant-time, no branching on secrets)
- [ ] WASM compilation for browser/edge deployment
- [ ] Python bindings to C implementation for 10×+ speedup
- [ ] Comparison benchmarking against **CRYSTALS-Kyber** and **NTRU**
- [ ] Publish in **IACR ePrint** or similar venue for peer review

### 🔬 Option D: Ring-E8 Module-LWE (Back Burner / Research)
This is the long-term path to genuine post-quantum security using E8 structure.
Replace the direct-sum E8^N with a **module lattice over a polynomial ring**:

```
R = Z[x] / (x^n + 1)          # Polynomial ring
M = R^8                          # Module of rank 8 over R
Lattice = φ(M) ⊂ R^(8n)          # Embedding into real space
```

Each coefficient is an E8 lattice point, but the global structure is a **polynomial module**
rather than a block-diagonal direct sum. This provides:
- **Ring-LWE hardness** (NIST-vetted security foundation)
- **Fast polynomial arithmetic** (NTT for O(n log n) multiplication)
- **E8 structure** at the coefficient level (densest packing in each module component)

Challenges:
- Requires **algebraic number theory** (E8 as a module over a ring of integers)
- **Discrete Gaussian sampling** with covariance matching E8 geometry
- **Rejection sampling** for constant-time key generation
- **Security proof** reducing to Module-LWE + E8 automorphism hardness

This is 6–12 months of full-time research. The current E8^N direct sum is the
proof-of-concept; Ring-E8 is the destination.

### Research Open Questions
- [ ] Does E8^N have **structured attacks** that generic lattices avoid?
- [ ] Can the Weyl group symmetries be exploited for **faster decryption** without leaking the key?
- [ ] Is E8 the optimal lattice cell, or would **Leech lattice** (24D) or **Barnes-Wall** be superior?
- [ ] What is the **concrete security** at N=64 vs N=128 under known lattice attacks?
- [ ] Does the **perturbation matrix** provide meaningful security gain, or just slow LLL slightly?
- [ ] Can **E8 automorphisms** be used to randomize the public basis without a trapdoor?

## 📝 References

- Goldreich, Goldwasser, Halevi. "Public-key cryptosystems from lattice reduction problems." CRYPTO 1997.
- Babai, L. "On Lovász' lattice reduction and the nearest lattice point problem." 1986.
- Conway, Sloane. "Sphere Packings, Lattices and Groups." Springer.
- NIST Post-Quantum Cryptography Standardization (CRYSTALS-Kyber, Dilithium)

## 📝 License

MIT License

---

**Version:** 2.0.0  
**Author:** Chain-Breaker Team / Hive Reconstruction  
**Last Updated:** 2026-08-01
