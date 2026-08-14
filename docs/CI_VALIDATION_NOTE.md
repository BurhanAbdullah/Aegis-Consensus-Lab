# CI validation gate

The validation branch must not be merged into `tag4` or `main` until a GitHub Actions run is green for the exact branch head.

The required run executes the complete pytest suite twice and executes the six-scenario benchmark twice, requiring byte-identical repeated output.

A missing workflow run is treated as `NOT VERIFIED`, never as success.
