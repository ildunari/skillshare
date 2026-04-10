# Distribution Drift

Distribution drift is not the same as duplication.

## Drift categories

### In sync
Canonical source and all expected installs match.

### Out of sync
Canonical source exists and install exists, but hashes differ.

### Install only
Runtime install exists, but no canonical source skill exists.

### Undistributed source
Canonical source exists, but one or more configured targets are missing installs.

## Reporting rule
Treat drift as a **sync / propagation** problem first. Only consider merge/archive/delete after the canonical/source relationship is understood.
