# Routing Collision Guide

Routing collisions happen when two skills can plausibly trigger on the same request.

## Detect using
- overlapping trigger phrases
- overlapping domain language
- same runtime or same canonical role
- lack of clear "use when" / "do not use when" boundaries

## Preferred fixes
1. tighten descriptions
2. add explicit boundaries
3. add supersedes declarations
4. rename if conceptual separation is weak
5. merge only if the skills truly do the same job
