import unittest

import numpy as np

from research.e8_lattice import (
    E8_SIMPLE_ROOT_BASIS,
    E8_SIMPLE_ROOT_BASIS_SCALED2,
    e8_roots_scaled2,
    exact_basis_determinant_scaled2,
    exact_gram_determinant_scaled2,
    gram_matrix,
    is_e8_lattice_vector,
    is_e8_lattice_vector_scaled2,
    lattice_covolume,
    verify_e8,
    verify_weyl_root_closure,
    weyl_reflect_scaled2,
)


class TestE8Mathematics(unittest.TestCase):
    def test_root_system_has_240_unique_roots(self):
        roots = e8_roots_scaled2()
        self.assertEqual(roots.shape, (240, 8))
        self.assertEqual(len({tuple(row) for row in roots}), 240)

    def test_every_root_has_squared_norm_two_exactly(self):
        roots = e8_roots_scaled2()
        norms_sq_scaled2 = np.einsum("ij,ij->i", roots, roots)
        self.assertTrue(np.all(norms_sq_scaled2 == 8))

    def test_every_generated_root_is_in_e8_exactly(self):
        self.assertTrue(
            all(is_e8_lattice_vector_scaled2(r) for r in e8_roots_scaled2())
        )

    def test_exact_reference_basis_covolume(self):
        self.assertEqual(exact_basis_determinant_scaled2(), -256)
        self.assertEqual(abs(exact_basis_determinant_scaled2()), 2**8)
        self.assertEqual(exact_gram_determinant_scaled2(), 4**8)

    def test_float_compatibility_view_matches_exact_basis(self):
        self.assertTrue(
            np.array_equal(
                E8_SIMPLE_ROOT_BASIS_SCALED2,
                np.rint(2.0 * E8_SIMPLE_ROOT_BASIS).astype(np.int64),
            )
        )
        self.assertTrue(np.isclose(lattice_covolume(), 1.0))
        self.assertTrue(np.isclose(np.linalg.det(gram_matrix()), 1.0))

    def test_basis_vectors_are_roots(self):
        roots = {tuple(row) for row in e8_roots_scaled2()}
        for basis_vector in E8_SIMPLE_ROOT_BASIS_SCALED2:
            self.assertIn(tuple(basis_vector), roots)

    def test_membership_rejects_non_lattice_vectors(self):
        self.assertFalse(is_e8_lattice_vector(np.array([0.25] * 8)))
        self.assertFalse(
            is_e8_lattice_vector(np.array([1.0, 0, 0, 0, 0, 0, 0, 0]))
        )
        self.assertFalse(
            is_e8_lattice_vector_scaled2(np.array([1, 1, 1, 1, 1, 1, 1, 0]))
        )

    def test_weyl_reflection_maps_known_root_to_root(self):
        roots = e8_roots_scaled2()
        reflected = weyl_reflect_scaled2(roots[0], roots[1])
        self.assertIn(tuple(reflected), {tuple(row) for row in roots})
        self.assertEqual(int(reflected @ reflected), 8)

    def test_all_57600_root_reflections_close_exactly(self):
        self.assertTrue(verify_weyl_root_closure())

    def test_machine_report_passes_all_exact_invariants(self):
        report = verify_e8()
        self.assertEqual(report["root_count"], 240)
        self.assertEqual(report["unique_root_count"], 240)
        self.assertTrue(report["all_roots_norm_squared_2_exact"])
        self.assertTrue(report["basis_vectors_are_roots_exact"])
        self.assertTrue(report["unimodular_covolume_1_exact"])
        self.assertTrue(report["gram_determinant_1_exact"])
        self.assertTrue(report["all_roots_are_lattice_vectors_exact"])
        self.assertTrue(report["weyl_root_closure_240x240"])


if __name__ == "__main__":
    unittest.main()
