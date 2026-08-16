"""Regression evidence for known failures in the archived v2 cipher.

These tests intentionally demonstrate insecure behavior. They are not tests of
properties a secure successor should preserve. Their purpose is containment:
future research must not mistake successful legacy round trips for security.
"""

import unittest

import numpy as np

from e8_core import E8Cipher


class TestLegacyCipherFailures(unittest.TestCase):
    def test_private_decoding_basis_is_identical_across_unrelated_keys(self):
        alice = E8Cipher(private_seed=b"alice-independent-key-material-000", N=4)
        bob = E8Cipher(private_seed=b"bob-independent-key-material---000", N=4)

        self.assertFalse(np.array_equal(alice.lattice.public_basis, bob.lattice.public_basis))
        self.assertTrue(np.array_equal(alice.lattice.perturbed_good, bob.lattice.perturbed_good))
        self.assertTrue(np.array_equal(alice.lattice.perturbation, bob.lattice.perturbation))

    def test_unrelated_private_key_can_cross_decrypt_ciphertext(self):
        alice = E8Cipher(private_seed=b"alice-independent-key-material-000", N=4)
        bob = E8Cipher(private_seed=b"bob-independent-key-material---000", N=4)
        message = b"cross-key isolation must fail in this legacy specimen"

        ciphertext = alice.encrypt(message)
        recovered_by_bob = bob.decrypt(ciphertext)

        self.assertEqual(recovered_by_bob, message)

    def test_repeated_encryption_reuses_entire_rng_stream(self):
        cipher = E8Cipher(private_seed=b"rng-reuse-regression-key-material!!", N=4)
        message = b"same plaintext, same deterministic legacy ciphertext"

        first = cipher.encrypt(message)
        second = cipher.encrypt(message)

        self.assertEqual(first["ciphertext"], second["ciphertext"])

    def test_ciphertext_difference_cancels_reused_lattice_mask_and_noise(self):
        cipher = E8Cipher(private_seed=b"difference-attack-regression-key!!", N=4)
        left = b"A" * cipher.block_size
        right = b"B" * cipher.block_size

        left_ct = np.asarray(cipher.encrypt(left)["ciphertext"][0], dtype=np.float64)
        right_ct = np.asarray(cipher.encrypt(right)["ciphertext"][0], dtype=np.float64)

        # Because encrypt() restarts the PRNG from the same secret-derived seed,
        # r and Gaussian noise are identical in both calls. Subtraction therefore
        # exposes the exact encoded plaintext difference: 65 - 66 = -1.
        self.assertTrue(np.allclose(left_ct - right_ct, -np.ones(cipher.block_size)))

    def test_legacy_nonce_is_constant_private_seed_prefix(self):
        seed = b"nonce-leak-regression-key-material!!"
        cipher = E8Cipher(private_seed=seed, N=4)

        first = cipher.encrypt(b"first")
        second = cipher.encrypt(b"second")

        expected = seed.hex()[:16]
        self.assertEqual(first["nonce"], expected)
        self.assertEqual(second["nonce"], expected)


if __name__ == "__main__":
    unittest.main()
