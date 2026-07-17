# E8-Lattice Cipher

A conceptual prototype for quantum-resistant encryption using the E8 root lattice.

## The Idea

E8 (the exceptional Lie group) has:
- **240 roots** in 8-dimensional space
- **696,729,600** Weyl group symmetries
- Hard "shortest vector problem" even for quantum computers

This prototype demonstrates lattice-based encryption:
- **Encryption**: Add E8 lattice "noise" to plaintext
- **Decryption**: Use private transform to find original lattice point
- **Security**: Finding short vectors without the private key is computationally hard

## Quick Start

```python
from e8_cipher import E8Cipher

# Create cipher with private key
cipher = E8Cipher(private_seed=b'my-secret-key')

# Encrypt
encrypted = cipher.encrypt(b"Hello E8")

# Decrypt
decrypted = cipher.decrypt(encrypted)
print(decrypted)  # b"Hello E8"
```

## Mathematical Foundation

The security relies on the **Learning With Errors (LWE)** problem over E8 lattice:

1. Message mapped to E8 lattice points
2. Private transform matrix applied
3. Lattice noise added (small random displacement)
4. Decryption requires knowing the private transform

Without the private key, decryption requires solving the **Shortest Vector Problem (SVP)** in 8D E8 lattice — believed to be quantum-hard.

## Why E8?

- Most symmetric object in mathematics
- Exceptional group with no classical analog
- Weyl group structure creates natural "noise" space
- 240 roots provide dense lattice for error correction

## Status

**CONCEPTUAL PROTOTYPE** — Demonstrates mathematical foundation. Not production-ready.

For production lattice cryptography, see:
- NIST Post-Quantum Cryptography standardization
- CRYSTALS-Kyber (lattice-based)
- CRYSTALS-Dilithium (lattice signatures)

## References

- Conway & Sloane, "Sphere Packings, Lattices and Groups"
- Regev, "On Lattices, Learning with Errors, and Cryptography"
- NIST PQC Standardization: https://csrc.nist.gov/projects/post-quantum-cryptography

## License

MIT — For research and educational purposes.
