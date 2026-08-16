"""Verified mathematical primitives for E8 research.

This module intentionally contains no encryption protocol. Its job is to make
claims about E8 mechanically testable before cryptographic constructions are
built on top of them.

For exact checks, vectors are represented in ``scaled2`` coordinates: every
coordinate is multiplied by two. E8 roots then have integer coordinates and
squared norm 8, so determinant, membership, and Weyl-reflection closure can be
verified without floating-point tolerances.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product

import numpy as np


# One standard simple-root basis for the E8 root lattice. Rows are basis
# vectors. Every row has squared norm 2 and |det(B)| = 1.
E8_SIMPLE_ROOT_BASIS_SCALED2 = np.array(
    [
        [1, -1, -1, -1, -1, -1, -1, 1],
        [2, 2, 0, 0, 0, 0, 0, 0],
        [-2, 2, 0, 0, 0, 0, 0, 0],
        [0, -2, 2, 0, 0, 0, 0, 0],
        [0, 0, -2, 2, 0, 0, 0, 0],
        [0, 0, 0, -2, 2, 0, 0, 0],
        [0, 0, 0, 0, -2, 2, 0, 0],
        [0, 0, 0, 0, 0, -2, 2, 0],
    ],
    dtype=np.int64,
)
E8_SIMPLE_ROOT_BASIS = E8_SIMPLE_ROOT_BASIS_SCALED2.astype(np.float64) / 2.0


def _det_bareiss(matrix: np.ndarray) -> int:
    """Return an exact integer determinant using the Bareiss algorithm."""

    a = [[int(x) for x in row] for row in np.asarray(matrix).tolist()]
    if not a or any(len(row) != len(a) for row in a):
        raise ValueError("matrix must be non-empty and square")

    n = len(a)
    if n == 1:
        return a[0][0]

    sign = 1
    previous_pivot = 1

    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign *= -1

        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                if numerator % previous_pivot != 0:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = numerator // previous_pivot
            a[i][k] = 0
        previous_pivot = pivot

    return sign * a[-1][-1]


def e8_roots_scaled2() -> np.ndarray:
    """Return all 240 E8 roots with every coordinate multiplied by two."""

    roots: list[list[int]] = []

    # 112 roots: permutations of (±1, ±1, 0, ..., 0), scaled by two.
    for i, j in combinations(range(8), 2):
        for si, sj in product((-2, 2), repeat=2):
            v = [0] * 8
            v[i] = si
            v[j] = sj
            roots.append(v)

    # 128 roots: (±1/2)^8 with an even number of minus signs, scaled by two.
    for signs in product((-1, 1), repeat=8):
        if sum(1 for x in signs if x < 0) % 2 == 0:
            roots.append(list(signs))

    out = np.asarray(roots, dtype=np.int64)
    if out.shape != (240, 8):
        raise AssertionError(f"internal E8 root construction error: {out.shape}")
    return out


def e8_roots() -> np.ndarray:
    """Return all 240 roots of E8 as a (240, 8) float64 array."""

    return e8_roots_scaled2().astype(np.float64) / 2.0


def is_e8_lattice_vector_scaled2(vector: np.ndarray) -> bool:
    """Exact E8 membership test for integer ``scaled2`` coordinates.

    In scaled-by-two coordinates, an E8 vector has either all-even or all-odd
    coordinates, and its coordinate sum is divisible by four.
    """

    v = np.asarray(vector)
    if v.shape != (8,) or not np.issubdtype(v.dtype, np.integer):
        return False
    values = [int(x) for x in v.tolist()]
    parity = values[0] & 1
    if any((x & 1) != parity for x in values):
        return False
    return sum(values) % 4 == 0


def is_e8_lattice_vector(vector: np.ndarray, atol: float = 1e-9) -> bool:
    """Floating-point compatibility wrapper for the conventional E8 model."""

    v = np.asarray(vector, dtype=np.float64)
    if v.shape != (8,):
        return False

    scaled = 2.0 * v
    rounded = np.rint(scaled)
    if not np.allclose(scaled, rounded, atol=atol):
        return False
    return is_e8_lattice_vector_scaled2(rounded.astype(np.int64))


def gram_matrix(basis: np.ndarray = E8_SIMPLE_ROOT_BASIS) -> np.ndarray:
    """Return the Gram matrix B B^T for a row-vector basis."""

    b = np.asarray(basis, dtype=np.float64)
    return b @ b.T


def lattice_covolume(basis: np.ndarray = E8_SIMPLE_ROOT_BASIS) -> float:
    """Return |det(B)| for a full-rank row-vector basis."""

    return float(abs(np.linalg.det(np.asarray(basis, dtype=np.float64))))


def exact_basis_determinant_scaled2() -> int:
    """Exact determinant of the scaled-by-two E8 reference basis."""

    return _det_bareiss(E8_SIMPLE_ROOT_BASIS_SCALED2)


def exact_gram_determinant_scaled2() -> int:
    """Exact determinant of B2 B2^T for the scaled-by-two basis B2."""

    b = E8_SIMPLE_ROOT_BASIS_SCALED2
    return _det_bareiss(b @ b.T)


def weyl_reflect_scaled2(vector: np.ndarray, root: np.ndarray) -> np.ndarray:
    """Apply an exact Weyl reflection using scaled-by-two coordinates.

    For an E8 root ``r`` with ||r||² = 2, s_r(x) = x - (x·r)r.
    After multiplying both x and r by two this becomes

        x2' = x2 - ((x2·r2) / 4) r2.

    E8 integrality guarantees the dot product is divisible by four.
    """

    x = np.asarray(vector, dtype=np.int64)
    r = np.asarray(root, dtype=np.int64)
    if x.shape != (8,) or r.shape != (8,):
        raise ValueError("vector and root must each have shape (8,)")
    if int(r @ r) != 8:
        raise ValueError("reflection root must have exact squared norm 2")

    dot = int(x @ r)
    if dot % 4 != 0:
        raise ValueError("vector/root inner product is not integral in E8 coordinates")
    return x - (dot // 4) * r


def verify_weyl_root_closure() -> bool:
    """Exhaustively verify all 240×240 root reflections remain E8 roots."""

    roots = e8_roots_scaled2()
    root_set = {tuple(int(x) for x in row) for row in roots}
    for vector in roots:
        for root in roots:
            reflected = weyl_reflect_scaled2(vector, root)
            if tuple(int(x) for x in reflected) not in root_set:
                return False
    return True


@dataclass(frozen=True)
class E8DirectSum:
    """Exact mathematical model of the orthogonal direct sum E8^N.

    This class is deliberately limited to lattice structure. It does not claim
    that E8^N is cryptographically hard, nor does it implement encryption.
    """

    copies: int

    def __post_init__(self) -> None:
        if not isinstance(self.copies, int) or self.copies < 1:
            raise ValueError("copies must be a positive integer")

    @property
    def dimension(self) -> int:
        return 8 * self.copies

    def basis_scaled2(self) -> np.ndarray:
        """Return the exact block-diagonal scaled-by-two basis for E8^N."""

        dim = self.dimension
        out = np.zeros((dim, dim), dtype=np.int64)
        for block in range(self.copies):
            start = 8 * block
            out[start : start + 8, start : start + 8] = E8_SIMPLE_ROOT_BASIS_SCALED2
        return out

    def basis(self) -> np.ndarray:
        """Return the conventional floating-point block-diagonal E8^N basis."""

        return self.basis_scaled2().astype(np.float64) / 2.0

    def is_lattice_vector_scaled2(self, vector: np.ndarray) -> bool:
        """Test exact E8^N membership by checking every E8 block."""

        v = np.asarray(vector)
        if v.shape != (self.dimension,) or not np.issubdtype(v.dtype, np.integer):
            return False
        return all(
            is_e8_lattice_vector_scaled2(v[start : start + 8])
            for start in range(0, self.dimension, 8)
        )

    def embed_root(self, block: int, root_index: int) -> np.ndarray:
        """Embed one of the 240 E8 roots into a selected direct-sum block."""

        if block < 0 or block >= self.copies:
            raise IndexError("block outside E8 direct sum")
        roots = e8_roots_scaled2()
        if root_index < 0 or root_index >= len(roots):
            raise IndexError("root_index outside E8 root system")
        out = np.zeros(self.dimension, dtype=np.int64)
        start = 8 * block
        out[start : start + 8] = roots[root_index]
        return out

    def reflect_scaled2(self, vector: np.ndarray, block: int, root_index: int) -> np.ndarray:
        """Apply an exact E8 Weyl reflection to one block of E8^N."""

        v = np.asarray(vector, dtype=np.int64)
        if v.shape != (self.dimension,):
            raise ValueError(f"vector must have shape ({self.dimension},)")
        if block < 0 or block >= self.copies:
            raise IndexError("block outside E8 direct sum")
        roots = e8_roots_scaled2()
        if root_index < 0 or root_index >= len(roots):
            raise IndexError("root_index outside E8 root system")

        out = v.copy()
        start = 8 * block
        out[start : start + 8] = weyl_reflect_scaled2(
            out[start : start + 8], roots[root_index]
        )
        return out

    def exact_scaled2_determinant(self) -> int:
        """Return det(2B) exactly for the block-diagonal E8^N basis."""

        single = exact_basis_determinant_scaled2()
        return single**self.copies

    def exact_scaled2_gram_determinant(self) -> int:
        """Return det((2B)(2B)^T) exactly for E8^N."""

        single = exact_gram_determinant_scaled2()
        return single**self.copies

    def verify(self) -> dict[str, object]:
        """Return explicit direct-sum invariants for this value of N."""

        basis2 = self.basis_scaled2()
        expected_abs_det2 = 2 ** self.dimension
        expected_gram_det2 = 4 ** self.dimension
        embedded_roots_valid = all(
            self.is_lattice_vector_scaled2(self.embed_root(block, root_idx))
            for block in range(self.copies)
            for root_idx in range(240)
        )

        # Check that reflections are block-local and preserve membership/norm
        # for every embedded root against every root in the same block.
        reflection_closure = True
        for block in range(self.copies):
            for root_idx in range(240):
                vector = self.embed_root(block, root_idx)
                norm_before = int(vector @ vector)
                for mirror_idx in range(240):
                    reflected = self.reflect_scaled2(vector, block, mirror_idx)
                    if (
                        not self.is_lattice_vector_scaled2(reflected)
                        or int(reflected @ reflected) != norm_before
                    ):
                        reflection_closure = False
                        break
                if not reflection_closure:
                    break
            if not reflection_closure:
                break

        return {
            "copies": self.copies,
            "dimension": self.dimension,
            "basis_shape": tuple(int(x) for x in basis2.shape),
            "block_diagonal_basis_exact": bool(
                all(
                    np.array_equal(
                        basis2[8*i:8*i+8, 8*j:8*j+8],
                        E8_SIMPLE_ROOT_BASIS_SCALED2 if i == j else np.zeros((8, 8), dtype=np.int64),
                    )
                    for i in range(self.copies)
                    for j in range(self.copies)
                )
            ),
            "scaled2_abs_determinant_exact": abs(self.exact_scaled2_determinant()),
            "expected_scaled2_abs_determinant": expected_abs_det2,
            "covolume_1_exact": abs(self.exact_scaled2_determinant()) == expected_abs_det2,
            "scaled2_gram_determinant_exact": self.exact_scaled2_gram_determinant(),
            "expected_scaled2_gram_determinant": expected_gram_det2,
            "gram_determinant_1_exact": self.exact_scaled2_gram_determinant() == expected_gram_det2,
            "embedded_root_count": 240 * self.copies,
            "all_embedded_roots_are_lattice_vectors_exact": embedded_roots_valid,
            "weyl_reflections_preserve_direct_sum_exact": reflection_closure,
        }


def verify_e8() -> dict[str, object]:
    """Run inexpensive and exact invariants and return a machine-readable report."""

    roots2 = e8_roots_scaled2()
    roots = roots2.astype(np.float64) / 2.0
    norms_sq_scaled2 = np.einsum("ij,ij->i", roots2, roots2)
    basis2 = E8_SIMPLE_ROOT_BASIS_SCALED2
    root_set = {tuple(int(x) for x in row) for row in roots2}

    unique_roots = len(root_set)
    basis_are_roots = all(tuple(int(x) for x in b) in root_set for b in basis2)
    exact_det2 = exact_basis_determinant_scaled2()
    exact_gram_det2 = exact_gram_determinant_scaled2()

    return {
        "dimension": 8,
        "root_count": int(len(roots)),
        "unique_root_count": int(unique_roots),
        "all_roots_norm_squared_2_exact": bool(np.all(norms_sq_scaled2 == 8)),
        "basis_vectors_are_roots_exact": bool(basis_are_roots),
        "basis_scaled2_determinant_exact": exact_det2,
        "basis_abs_determinant_exact": f"{abs(exact_det2)}/2^8 = 1",
        "unimodular_covolume_1_exact": abs(exact_det2) == 2**8,
        "gram_scaled2_determinant_exact": exact_gram_det2,
        "gram_determinant_1_exact": exact_gram_det2 == 4**8,
        "all_roots_are_lattice_vectors_exact": bool(
            all(is_e8_lattice_vector_scaled2(root) for root in roots2)
        ),
        "weyl_root_closure_240x240": verify_weyl_root_closure(),
        "direct_sum_examples": {
            f"E8^{copies}": E8DirectSum(copies).verify() for copies in (1, 2, 4)
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(verify_e8(), indent=2, sort_keys=True))
