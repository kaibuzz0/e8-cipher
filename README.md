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
