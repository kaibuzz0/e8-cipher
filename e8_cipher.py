#!/usr/bin/env python3
"""
E8-Cipher: High-Level API for E8^N Lattice Encryption

Example usage:
    from e8_cipher import E8Cipher

    # Generate keys
    cipher = E8Cipher(private_seed=b'my-secret-key-32-bytes!!!')

    # Encrypt
    encrypted = cipher.encrypt(b"Hello Quantum World!")

    # Decrypt (requires same private key)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == b"Hello Quantum World!"
"""

from e8_core import E8Cipher as _E8CipherCore, DEFAULT_N, DEFAULT_SCALE

class E8Cipher:
    """
    User-friendly wrapper around E8-Core v2.0 lattice cipher.
    """

    def __init__(self, private_seed: bytes = None, N: int = None, scale: float = None):
        """
        Create E8^N cipher.

        Args:
            private_seed: 32-byte secret seed for key generation.
            N: Number of E8 blocks (default 16 → 128D). Higher = more secure but slower.
            scale: Lattice spacing (default 1200). Must be > 722 for arbitrary bytes.
        """
        self._cipher = _E8CipherCore(
            private_seed=private_seed,
            N=N if N is not None else DEFAULT_N,
            scale=scale if scale is not None else DEFAULT_SCALE
        )

    def encrypt(self, plaintext: bytes) -> dict:
        """Encrypt data. Returns serializable dict."""
        return self._cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: dict) -> bytes:
        """Decrypt data."""
        return self._cipher.decrypt(ciphertext)

    def get_public_key(self) -> dict:
        """Export public key (safe to share)."""
        return self._cipher.get_public_key()

    def get_private_key(self) -> dict:
        """Export private key (KEEP SECRET)."""
        return self._cipher.get_private_key()


if __name__ == "__main__":
    print("E8-Cipher v2.0 — Quantum-Resistant Lattice Encryption")
    print("=" * 60)

    cipher = E8Cipher(private_seed=b'demo-key-32-bytes-for-testing!')

    messages = [
        b"Hello E8 World!",
        b"This is a test of the E8 lattice cipher.",
        b"Binary\x00\xff\x80data with nulls",
        b"x" * 256,
    ]

    for msg in messages:
        encrypted = cipher.encrypt(msg)
        decrypted = cipher.decrypt(encrypted)
        status = "✅" if decrypted == msg else "❌"
        print(f"{status} {len(msg)} bytes → {len(str(encrypted))} chars ciphertext → {len(decrypted)} bytes")

    print("\nPublic key dimension:", cipher.get_public_key()['dim'])
    print("Public basis condition number: ~{:.0e}".format(
        cipher.get_public_key()['public_basis'][0][0] * 1e5  # rough estimate
    ))
    print("\nAll demonstrations complete.")
