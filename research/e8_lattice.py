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
    }


if __name__ == "__main__":
    import json

    print(json.dumps(verify_e8(), indent=2, sort_keys=True))
