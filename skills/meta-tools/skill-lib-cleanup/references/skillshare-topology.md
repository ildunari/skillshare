# Skillshare Topology

The cleanup skill should treat skillshare as a distribution system, not just another folder tree.

## Inputs
Read:
- `source`
- `mode`
- `targets`
- ignore rules

from `~/.config/skillshare/config.yaml`.

## Questions to answer
- Which skills exist in canonical source?
- Which target runtimes should receive them?
- Which targets are missing installs?
- Which installs are exact matches, drifted, or extra?
- Which installs exist without any canonical source skill?

## Drift statuses
- `in-sync`
- `out-of-sync`
- `install-only`
- `undistributed-source`
- `missing`

## Action defaults
- `out-of-sync` → usually **SYNC FROM SOURCE** or manual divergence review
- `install-only` → **PROMOTE TO SOURCE** or archive/remove
- `undistributed-source` → **PUSH TO TARGETS** if intended to distribute
