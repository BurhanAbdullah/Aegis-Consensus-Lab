"""Weighted certificate semantics for the tag4 consensus model.

A certificate is bound to (height, view, phase, proposal_id) and contains
at most one vote per validator. Safety is conditional on honest validators
not signing conflicting proposals in the same context.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple


@dataclass(frozen=True)
class Vote:
    validator_id: str
    height: int
    view: int
    phase: str
    proposal_id: str
    weight: float


@dataclass(frozen=True)
class Certificate:
    height: int
    view: int
    phase: str
    proposal_id: str
    weight: float
    voters: Tuple[str, ...]


def certificate(votes: Iterable[Vote], quorum_weight: float) -> Certificate | None:
    votes = list(votes)
    if not votes:
        return None
    first = votes[0]
    seen = set()
    total = 0.0
    for vote in votes:
        context = (vote.height, vote.view, vote.phase, vote.proposal_id)
        expected = (first.height, first.view, first.phase, first.proposal_id)
        if context != expected or vote.validator_id in seen or vote.weight < 0:
            return None
        seen.add(vote.validator_id)
        total += vote.weight
    if total + 1e-12 < quorum_weight:
        return None
    return Certificate(first.height, first.view, first.phase, first.proposal_id, total, tuple(sorted(seen)))


def conflicting_certificates(a: Certificate, b: Certificate) -> bool:
    return (
        a.height == b.height
        and a.view == b.view
        and a.phase == b.phase
        and a.proposal_id != b.proposal_id
    )


def weighted_intersection_lower_bound(q: float) -> float:
    """Minimum intersection weight of two subsets of normalized total weight 1."""
    return max(0.0, 2.0 * q - 1.0)


def safety_margin(q: float, byzantine_weight: float) -> float:
    """Safety margin with a numerical guard at the exact theoretical boundary.

    The mathematical condition is 2q - 1 > b.  The tolerance only prevents
    binary floating-point roundoff from turning an exact boundary into a
    false positive; it does not relax the mathematical inequality.
    """
    return weighted_intersection_lower_bound(q) - float(byzantine_weight)


def safety_condition(q: float, byzantine_weight: float) -> bool:
    return safety_margin(q, byzantine_weight) > 1e-12


def availability_condition(q: float, honest_participating_weight: float) -> bool:
    return float(q) <= float(honest_participating_weight) + 1e-12


def feasible_interval(byzantine_weight: float) -> Tuple[float, float]:
    b = float(byzantine_weight)
    return ((1.0 + b) / 2.0, 1.0 - b)
