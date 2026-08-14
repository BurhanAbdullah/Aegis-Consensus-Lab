"""Cross-validation of the closed-form scalar boundary against the kernel."""
from __future__ import annotations

from itertools import product

from ..analytical_reference import feasible, quorum, trust_equilibrium
from ..kernel.tag4_kernel import AegisKernel, Params, ValidatorState

EVIDENCE_GRID = tuple(i / 20 for i in range(21))
B_GRID = tuple(i / 20 for i in range(7))
Q0_GRID = tuple(0.45 + i * 0.025 for i in range(13))
BOUNDARY_TOL = 1e-9
MAX_STEPS = 300


def run_sweep() -> list[dict]:
    rows = []
    for evidence, b, q0 in product(EVIDENCE_GRID, B_GRID, Q0_GRID):
        params = Params(q0=q0)
        tau_star = trust_equilibrium(params.rho, params.ell, evidence)
        q_star = quorum(q0, params.alpha_q, tau_star, params.q_min, params.q_max)
        kernel = AegisKernel([ValidatorState("A", [0.37] * 4)], params=params)
        trace = None
        for _ in range(MAX_STEPS):
            trace = kernel.step({"A": evidence}, {"A": 0.0}, {"A": True}, {"A": True})
        assert trace is not None
        analytical_safe = feasible(q_star, b)
        empirical_safe = feasible(trace.quorum_fraction, b)
        away_from_boundary = (
            abs(q_star - (1.0 + b) / 2.0) > BOUNDARY_TOL
            and abs(q_star - (1.0 - b)) > BOUNDARY_TOL
        )
        rows.append({
            "evidence": evidence,
            "byzantine_weight": b,
            "q0": q0,
            "analytical_tau": tau_star,
            "empirical_tau": trace.tau["A"],
            "analytical_q": q_star,
            "empirical_q": trace.quorum_fraction,
            "analytical_feasible": int(analytical_safe),
            "empirical_feasible": int(empirical_safe),
            "away_from_boundary": int(away_from_boundary),
        })
    return rows


def max_errors(rows: list[dict]) -> tuple[float, float, int, int]:
    tau_error = max(abs(r["analytical_tau"] - r["empirical_tau"]) for r in rows)
    q_error = max(abs(r["analytical_q"] - r["empirical_q"]) for r in rows)
    checked = [r for r in rows if r["away_from_boundary"]]
    classification_mismatches = sum(r["analytical_feasible"] != r["empirical_feasible"] for r in checked)
    near_boundary = len(rows) - len(checked)
    return tau_error, q_error, classification_mismatches, near_boundary


if __name__ == "__main__":
    rows = run_sweep()
    print("cases", len(rows))
    print("max_errors", max_errors(rows))
