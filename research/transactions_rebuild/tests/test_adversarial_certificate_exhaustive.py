from itertools import combinations


def subset_weight(subset, weights):
    return sum(weights[i] for i in subset)


def has_honest_intersection(a, b, byzantine):
    return bool((set(a) & set(b)) - set(byzantine))


def conflicting_certificate_pair_exists(weights, byzantine, q):
    n = len(weights)
    valid = [
        s for r in range(1, n + 1)
        for s in combinations(range(n), r)
        if subset_weight(s, weights) + 1e-12 >= q
    ]
    for i, a in enumerate(valid):
        for b in valid[i + 1 :]:
            if not has_honest_intersection(a, b, byzantine):
                return True, a, b
    return False, None, None


def test_exhaustive_boundary_for_ten_equal_weight_validators():
    weights = [0.1] * 10
    byzantine = {0, 1}  # b = 0.2

    unsafe, _, _ = conflicting_certificate_pair_exists(weights, byzantine, 0.60)
    assert unsafe

    unsafe, a, b = conflicting_certificate_pair_exists(weights, byzantine, 0.61)
    assert not unsafe
    assert a is None and b is None


def test_exhaustive_q_strictly_above_theoretical_boundary():
    weights = [0.125] * 8
    byzantine = {0, 1}  # b = 0.25
    boundary = (1 + 0.25) / 2

    unsafe, _, _ = conflicting_certificate_pair_exists(weights, byzantine, boundary)
    assert unsafe

    unsafe, _, _ = conflicting_certificate_pair_exists(weights, byzantine, boundary + 0.001)
    assert not unsafe
