import unittest

import numpy as np

from research.e8_lattice import (
    E8_SIMPLE_ROOT_BASIS,
    e8_roots,
    gram_matrix,
    is_e8_lattice_vector,
    lattice_covolume,
    verify_e8,
)


class TestE8Mathematics(unittest.TestCase):
    def test_root_system_has_240_unique_roots(self):
        roots = e8_roots()
        self.assertEqual(roots.shape, (240, 8))
        self.assertEqual(len({tuple(row) for row in roots}), 240)

    def test_every_root_has_squared_norm_two(self):
        roots = e8_roots()
        norms_sq = np.einsum("ij,ij->i", roots, roots)
        self.assertTrue(np.allclose(norms_sq, 2.0))

    def test_every_generated_root_is_in_e8(self):
        self.assertTrue(all(is_e8_lattice_vector(r) for r in e8_roots()))

    def test_basis_is_full_rank_and_unimodular(self):
        self.assertEqual(np.linalg.matrix_rank(E8_SIMPLE_ROOT_BASIS), 8)
        self.assertTrue(np.isclose(lattice_covolume(), 1.0))
        self.assertTrue(np.isclose(abs(np.linalg.det(E8_SIMPLE_ROOT_BASIS)), 1.0))

    def test_gram_determinant_is_one(self):
        self.assertTrue(np.isclose(np.linalg.det(gram_matrix()), 1.0))

    def test_basis_vectors_are_roots(self):
        roots = e8_roots()
        for basis_vector in E8_SIMPLE_ROOT_BASIS:
            self.assertTrue(any(np.allclose(basis_vector, r) for r in roots))

    def test_membership_rejects_non_lattice_vector(self):
        self.assertFalse(is_e8_lattice_vector(np.array([0.25] * 8)))
        self.assertFalse(is_e8_lattice_vector(np.array([1.0, 0, 0, 0, 0, 0, 0, 0])))

    def test_machine_report_passes_all_invariants(self):
        report = verify_e8()
        self.assertEqual(report["root_count"], 240)
        self.assertEqual(report["unique_root_count"], 240)
        self.assertTrue(report["all_roots_norm_squared_2"])
        self.assertTrue(report["basis_vectors_are_roots"])
        self.assertTrue(report["unimodular_covolume_1"])
        self.assertTrue(report["all_roots_are_lattice_vectors"])


if __name__ == "__main__":
    unittest.main()
