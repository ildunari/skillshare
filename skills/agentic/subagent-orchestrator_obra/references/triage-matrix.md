# Triage Matrix

## Quick-fix eligibility (all required)

- Estimated <=12 tool calls
- Localized change (single-file or tightly local)
- No API/interface/schema contract change

If all conditions pass -> `quick_fix`.
Otherwise -> `involved_fix`.

## Routing

- `complete`: mark track done
- `quick_fix`: parent fix or small targeted fix agent, then re-review
- `involved_fix`: resume same implementer when possible, then re-review

## Escalation

- 3 failed re-validation loops on a track -> stop retries and escalate
- Repeat timeout on same track -> escalate with recovery options
