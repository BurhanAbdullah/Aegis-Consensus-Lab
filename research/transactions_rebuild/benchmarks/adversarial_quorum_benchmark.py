"""Adversarial weighted-quorum benchmark at and above the safety boundary.

Ten equal-weight validators are used so the construction is transparent:
validators 0 and 1 are Byzantine (b=0.2). At q=0.60, two conflicting
certificates can each contain both Byzantine validators plus four disjoint
honest validators. At q>0.60 this construction is impossible.
"""
from __future__ import annotations

from itertools import combinations

WEIGHTS = (0.1,) * 10
BYZANTINE = frozenset((0, 1))
BOUNDARY_Q = 0.60
ADAPTIVE_Q = 0.61


def certificate_sets(q: float):
    return [
        s
        for r in range(1, len(WEIGHTS) + 1)
        for s in combinations(range(len(WEIGHTS)), r)
        if sum(WEIGHTS[i] for i in s) + 1e-12 >= q
    ]


def conflicting_pair(q: float):
    valid = certificate_sets(q)
    for i, a in enumerate(valid):
        for b in valid[i + 1 :]:
            if not ((set(a) & set(b)) - set(BYZANTINE)):
                return a, b
    return None


def benchmark() -> dict[str, object]:
    boundary_pair = conflicting_pair(BOUNDARY_Q)
    adaptive_pair = conflicting_pair(ADAPTIVE_Q)
    return {
        "boundary_q": BOUNDARY_Q,
        "adaptive_q": ADAPTIVE_Q,
        "boundary_conflict_exists": boundary_pair is not None,
        "adaptive_conflict_exists": adaptive_pair is not None,
        "boundary_pair": boundary_pair,
        "adaptive_pair": adaptive_pair,
    }


if __name__ == "__main__":
    print(benchmark())
