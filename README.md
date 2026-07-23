# E8-Cipher: Quantum-Resistant Lattice Cryptography

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **E8 Lattice-Based Encryption for the Post-Quantum Era**

A pure Python implementation of quantum-resistant cryptography using the E8 root lattice.

## 🔬 Mathematical Foundation

The E8 exceptional Lie group provides:
- **240 root vectors** in 8-dimensional space
- **696,729,600 Weyl group symmetries**
- **NP-hard Shortest Vector Problem** (quantum-resistant)

## 🚀 Quick Start

```bash
pip install numpy
python e8_core.py
```

```python
from e8_core import E8Cipher

# Create cipher
cipher = E8Cipher(private_seed=b'secret-key-32-bytes!')

# Encrypt
encrypted = cipher.encrypt(b"Hello Quantum World!")

# Decrypt
decrypted = cipher.decrypt(encrypted)
```

## 📖 Documentation

See inline docstrings and test suite in `e8_core.py`.

## 📝 License

MIT License
