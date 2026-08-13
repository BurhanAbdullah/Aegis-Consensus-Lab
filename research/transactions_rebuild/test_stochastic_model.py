import numpy as np
from stochastic_model import StochasticParams, trust_step, risk_step, monte_carlo_mean_trajectory


def test_deterministic_stochastic_wrapper_matches_reference():
    p = StochasticParams(rho=.2, ell=.3, evidence_noise_std=0.0)
    tau, e = trust_step(.7, .5, p, np.random.default_rng(1))
    assert np.isclose(tau, .7 + .2*.3 - .3*.5*.7)
    assert e == .5


def test_noise_is_seed_reproducible():
    p = StochasticParams(evidence_noise_std=.05)
    a = trust_step(.7, .5, p, np.random.default_rng(42))
    b = trust_step(.7, .5, p, np.random.default_rng(42))
    assert np.allclose(a[0], b[0])
    assert np.allclose(a[1], b[1])


def test_risk_bounds():
    p = StochasticParams()
    r = risk_step(.8, 1.0, 1.0, p)
    assert 0.0 <= r <= 1.0


def test_mc_reproducibility():
    p = StochasticParams(evidence_noise_std=.02)
    a = monte_carlo_mean_trajectory(.8, .5, p, 20, 30, 123)
    b = monte_carlo_mean_trajectory(.8, .5, p, 20, 30, 123)
    assert all(np.allclose(x, y) for x, y in zip(a, b))
