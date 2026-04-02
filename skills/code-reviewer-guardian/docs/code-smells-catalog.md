
# Code Smells Catalog (Swift)

## Long Method (P2)
- **Look for**: functions > 60 lines; deeply nested conditionals.
- **Why**: impedes comprehension and reuse.
- **Fix**: Extract Method; early returns; strategy pattern.

## God Object (P2)
- **Look for**: types > 600 lines; 25+ methods; touches many modules.
- **Why**: high coupling, low cohesion.
- **Fix**: Extract Type; split responsibilities; define small protocols.

## Feature Envy (P2)
- **Look for**: method manipulates other objects more than self.
- **Why**: misplaced behavior and tight coupling.
- **Fix**: Move Method; push behavior to data or service.

## Data Clumps (P3)
- **Look for**: repeated parameter tuples.
- **Fix**: Introduce Parameter Object.

## Duplicate Code (P3)
- **Look for**: similar blocks across files.
- **Fix**: DRY: extract common functions or types.

## Massive View Controller (P2)
- **Look for**: networking/persistence/formatting in VC.
- **Fix**: MVVM/Clean: ViewModel + Interactor + Services.
