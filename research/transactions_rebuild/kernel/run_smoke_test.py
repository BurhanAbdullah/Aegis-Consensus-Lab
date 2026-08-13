from tag4_kernel import AegisKernel, ValidatorState


if __name__ == "__main__":
    k = AegisKernel([
        ValidatorState("v1", [1, 1, 1, 1]),
        ValidatorState("v2", [.9, .8, .9, .8]),
        ValidatorState("v3", [.7, .7, .8, .7]),
        ValidatorState("v4", [.6, .7, .6, .8]),
    ])
    for r in range(10):
        e = {"v1": 0.05, "v2": 0.05, "v3": 0.05, "v4": 0.05}
        d = {v: 0.0 for v in e}
        if 4 <= r <= 6:
            e["v3"] = 0.8
            d["v3"] = 0.5
        t = k.step(e, d)
        print(t.round, round(t.quorum_fraction, 6), round(t.total_weight, 6), round(t.quorum_weight, 6))
