"""Verified mathematical primitives for E8 research.

This module intentionally contains no encryption protocol.  Its job is to make
claims about E8 mechanically testable before cryptographic constructions are
built on top of them.
"""

from __future__ import annotations

from itertools import combinations, product

import numpy as np


# One standard simple-root basis for the E8 root lattice.  Rows are basis
# vectors.  Every row has squared norm 2 and |det(B)| = 1.
E8_SIMPLE_ROOT_BASIS = np.array(
    [
        [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5],
        [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0],
    ],
    dtype=np.float64,
)


def e8_roots() -> np.ndarray:
    """Return all 240 roots of E8 as a (240, 8) float64 array.

    The roots are the union of:
      * 112 integer roots: permutations of (±1, ±1, 0, ..., 0)
      * 128 half-integer roots: (±1/2)^8 with an even number of minus signs
    """

    roots: list[np.ndarray] = []

    for i, j in combinations(range(8), 2):
        for si, sj in product((-1.0, 1.0), repeat=2):
            v = np.zeros(8, dtype=np.float64)
            v[i] = si
            v[j] = sj
            roots.append(v)

    for signs in product((-0.5, 0.5), repeat=8):
        minus_count = sum(1 for x in signs if x < 0)
        if minus_count % 2 == 0:
            roots.append(np.asarray(signs, dtype=np.float64))

    out = np.asarray(roots, dtype=np.float64)
    if out.shape != (240, 8):
        raise AssertionError(f"internal E8 root construction error: {out.shape}")
    return out


def gram_matrix(basis: np.ndarray = E8_SIMPLE_ROOT_BASIS) -> np.ndarray:
    """Return the Gram matrix B B^T for a row-vector basis."""

    b = np.asarray(basis, dtype=np.float64)
    return b @ b.T


def lattice_covolume(basis: np.ndarray = E8_SIMPLE_ROOT_BASIS) -> float:
    """Return |det(B)| for a full-rank row-vector basis."""

    return float(abs(np.linalg.det(np.asarray(basis, dtype=np.float64))))


def is_e8_lattice_vector(vector: np.ndarray, atol: float = 1e-9) -> bool:
    """Test membership in the conventional coordinate description of E8.

    E8 consists of vectors whose coordinates are either all integers or all
    half-integers and whose coordinate sum is even.
    """

    v = np.asarray(vector, dtype=np.float64)
    if v.shape != (8,):
        return False

    integer_coords = np.allclose(v, np.rint(v), atol=atol)
    half_coords = np.allclose(v - 0.5, np.rint(v - 0.5), atol=atol)
    if not (integer_coords or half_coords):
        return False

    s = float(np.sum(v))
    return abs(s - 2.0 * round(s / 2.0)) <= atol


def verify_e8() -> dict[str, object]:
    """Run inexpensive invariants and return a machine-readable report."""

    roots = e8_roots()
    norms_sq = np.einsum("ij,ij->i", roots, roots)
    basis = E8_SIMPLE_ROOT_BASIS
    det = float(np.linalg.det(basis))
    gram = gram_matrix(basis)

    unique_roots = len({tuple(row.tolist()) for row in roots})
    basis_are_roots = all(
        any(np.allclose(b, root) for root in roots)
        for b in basis
    )

    return {
        "dimension": 8,
        "root_count": int(len(roots)),
        "unique_root_count": int(unique_roots),
        "all_roots_norm_squared_2": bool(np.allclose(norms_sq, 2.0)),
        "basis_vectors_are_roots": bool(basis_are_roots),
        "basis_abs_determinant": abs(det),
        "unimodular_covolume_1": bool(np.isclose(abs(det), 1.0)),
        "gram_determinant": float(np.linalg.det(gram)),
        "all_roots_are_lattice_vectors": bool(
            all(is_e8_lattice_vector(root) for root in roots)
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(verify_e8(), indent=2, sort_keys=True))
