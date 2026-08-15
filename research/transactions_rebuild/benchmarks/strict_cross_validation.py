"""Independent numerical audit for the Transactions tag4 mathematical model.

This is deliberately separate from the canonical implementation: it derives the
reference formulas locally and compares them against the executable model.
"""
from __future__ import annotations

import csv
from pathlib import Path
import numpy as np

from research.transactions_rebuild.unified_state_model import (
    ReducedParams, equilibrium, full_interior_jacobian, full_interior_step,
    jury_conditions_2x2, spectral_radius, risk_containment,
)

OUT = Path("experiments/strict_cross_validation.csv")


def fd_jacobian(fun, x, h=1e-6):
    x = np.asarray(x, float)
    y = np.asarray(fun(x), float)
    J = np.empty((y.size, x.size))
    for j in range(x.size):
        xp, xm = x.copy(), x.copy(); xp[j] += h; xm[j] -= h
        J[:, j] = (fun(xp)-fun(xm))/(2*h)
    return J


def run(seed=20260814, n=1000):
    rng = np.random.default_rng(seed)
    rows = []
    max_jac_err = 0.0
    max_eq_residual = 0.0
    stability_mismatch = 0
    containment_mismatch = 0
    for case in range(n):
        p = ReducedParams(rho=rng.uniform(.02,.25), ell=rng.uniform(.03,.35),
                          a=rng.uniform(.05,.95), c=rng.uniform(.02,.20),
                          kappa=rng.uniform(.1,.8), q0=rng.uniform(.5,.8),
                          alpha_q=rng.uniform(.05,.35))
        e, d = rng.uniform(0,.85), rng.uniform(0,.85)
        contained = risk_containment(e,d,p)
        if contained:
            x2 = equilibrium(e,d,p)
            residual = np.max(np.abs(np.array([
                x2[0] + p.rho*(1-x2[0]) - p.ell*e*x2[0],
                p.a*x2[1] + (1-p.a)*e + p.c*d]) - x2))
            max_eq_residual = max(max_eq_residual, float(residual))
            x = np.r_[rng.uniform(.2,.8,4), rng.uniform(.1,.8)]
            J = full_interior_jacobian(e,p,4)
            Jfd = fd_jacobian(lambda z: full_interior_step(z,e,d,p), x)
            jac_err = np.linalg.norm(J-Jfd,'fro')/max(1.0,np.linalg.norm(J,'fro'))
            max_jac_err = max(max_jac_err,float(jac_err))
        else:
            jac_err = np.nan; residual = np.nan
        # Independent direct-vs-Jury cross-check on a general 2x2 map.
        A = rng.normal(0,.4,(2,2))
        direct = spectral_radius(A) < 1.0
        jury = jury_conditions_2x2(A)['stable']
        stability_mismatch += int(direct != jury)
        rows.append(dict(case=case, evidence=e, drift=d, contained=contained,
                         equilibrium_residual=residual, jacobian_rel_error=jac_err,
                         direct_stable=direct, jury_stable=jury))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
    assert max_eq_residual < 1e-10
    assert max_jac_err < 5e-8
    assert stability_mismatch == 0
    return dict(cases=n,max_equilibrium_residual=max_eq_residual,
                max_jacobian_relative_error=max_jac_err,
                stability_mismatches=stability_mismatch,
                output=str(OUT))


if __name__ == '__main__':
    print(run())
