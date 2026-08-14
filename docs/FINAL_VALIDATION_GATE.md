# Final validation gate

A submission-ready state requires:

1. exact-head GitHub Actions PASS;
2. complete test suite PASS twice;
3. canonical six-scenario benchmark PASS twice with byte-identical outputs;
4. ten-seed summary with 95% confidence intervals;
5. fixed-quorum reference comparison using identical traces;
6. no unsupported PBFT/HotStuff performance claims;
7. no unsupported 9,450-case physical claim;
8. manuscript numbers traceable to frozen repository artifacts.

Until all eight conditions are met, release status is BLOCKED.