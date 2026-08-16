#!/usr/bin/env python3
"""Legacy high-level API for the archived v2 E8 cipher experiment.

SECURITY STATUS
===============
This module is retained only as a broken-design research specimen. It is not a
secure encryption protocol and must not be used to protect secrets. Verified
failures include cross-key decryption, reconstruction of the effective decoding
basis, deterministic encryption RNG reuse, ciphertext-difference leakage, and a
private-seed-derived pseudo-nonce.

The active research track lives under ``research/`` and intentionally does not
claim a secure successor protocol yet.
"""

import warnings

from e8_core import E8Cipher as _E8CipherCore, DEFAULT_N, DEFAULT_SCALE


class LegacyCipherSecurityWarning(UserWarning):
    """Warning emitted when the archived insecure cipher is instantiated."""


LEGACY_SECURITY_NOTICE = (
    "e8_cipher.E8Cipher is the archived insecure v2 research specimen; "
    "it has verified cross-key, deterministic-RNG, and key-structure failures "
    "and must not be used to protect secrets."
)


class E8Cipher:
    """Compatibility wrapper around the archived insecure v2 cipher.

    This class remains importable so historical experiments and regression tests
    are reproducible. Construction emits :class:`LegacyCipherSecurityWarning`.
    """

    def __init__(self, private_seed: bytes = None, N: int = None, scale: float = None):
        """Create the legacy cipher specimen and emit a visible security warning."""
        warnings.warn(LEGACY_SECURITY_NOTICE, LegacyCipherSecurityWarning, stacklevel=2)
        self._cipher = _E8CipherCore(
            private_seed=private_seed,
            N=N if N is not None else DEFAULT_N,
            scale=scale if scale is not None else DEFAULT_SCALE,
        )

    def encrypt(self, plaintext: bytes) -> dict:
        """Run legacy encryption for compatibility/research only."""
        return self._cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: dict) -> bytes:
        """Run legacy decryption for compatibility/research only."""
        return self._cipher.decrypt(ciphertext)

    def get_public_key(self) -> dict:
        """Export the legacy public-key representation for research."""
        return self._cipher.get_public_key()

    def get_private_key(self) -> dict:
        """Export legacy private material for reproducibility; keep it secret."""
        return self._cipher.get_private_key()


if __name__ == "__main__":
    print("E8-Cipher v2.x — ARCHIVED INSECURE RESEARCH SPECIMEN")
    print("=" * 64)
    print(LEGACY_SECURITY_NOTICE)
    print("\nUse research/e8_lattice.py for the verified mathematical substrate.")
