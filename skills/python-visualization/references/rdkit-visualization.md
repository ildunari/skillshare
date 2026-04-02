# RDKit Visualization Reference

2D molecular drawing, grid images, substructure highlighting, SVG export, and matplotlib integration.


## Contents

- [Installation](#installation)
- [SMILES to Molecule Object](#smiles-to-molecule-object)
- [Single Molecule Drawing](#single-molecule-drawing)
- [Grid Images (Multiple Molecules)](#grid-images-multiple-molecules)
- [Substructure Highlighting](#substructure-highlighting)
- [Similarity Maps](#similarity-maps)
- [Molecular Descriptors](#molecular-descriptors)
- [Drawing Options (MolDrawOptions)](#drawing-options-moldrawoptions)
- [Integration with Matplotlib](#integration-with-matplotlib)
- [Common Gotchas](#common-gotchas)

## Installation

RDKit is not pip-installable on all platforms. Use conda:

```bash
conda install -c conda-forge rdkit
```

Current stable: RDKit 2025.09.x. Always verify installation:

```python
try:
    from rdkit import Chem
    from rdkit.Chem import Draw, AllChem, Descriptors
    print(f"RDKit version: {Chem.rdBase.rdkitVersion}")
except ImportError:
    print("RDKit not installed. Use: conda install -c conda-forge rdkit")
```

## SMILES to Molecule Object

```python
from rdkit import Chem

mol = Chem.MolFromSmiles('CCO')             # ethanol
mol = Chem.MolFromSmiles('c1ccccc1')        # benzene
mol = Chem.MolFromSmiles('CC(=O)O')         # acetic acid
mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')  # aspirin

# ALWAYS check for None (invalid SMILES returns None, no error)
mol = Chem.MolFromSmiles('invalid')
if mol is None:
    print("Invalid SMILES string")
```

### Other input formats

```python
mol = Chem.MolFromMolFile('molecule.mol')
mol = Chem.MolFromMolBlock(mol_block_string)
mol = Chem.MolFromPDBFile('protein.pdb')

# From SDF file (multiple molecules)
suppl = Chem.SDMolSupplier('compounds.sdf')
mols = [mol for mol in suppl if mol is not None]
```

### Canonical SMILES (standardization)

```python
canonical = Chem.MolToSmiles(mol, canonical=True)
```

## Single Molecule Drawing

### Quick image

```python
from rdkit.Chem import Draw

mol = Chem.MolFromSmiles('c1ccc(CC(=O)O)cc1')
img = Draw.MolToImage(mol, size=(400, 300))
img.save('molecule.png')
```

### SVG output (publication quality, vector)

```python
from rdkit.Chem.Draw import rdMolDraw2D

drawer = rdMolDraw2D.MolDraw2DSVG(400, 300)
drawer.DrawMolecule(mol)
drawer.FinishDrawing()
svg = drawer.GetDrawingText()

with open('molecule.svg', 'w') as f:
    f.write(svg)
```

### PNG with MolDraw2DCairo (high-res raster)

```python
drawer = rdMolDraw2D.MolDraw2DCairo(800, 600)
drawer.DrawMolecule(mol)
drawer.FinishDrawing()
png_data = drawer.GetDrawingText()

with open('molecule.png', 'wb') as f:
    f.write(png_data)
```

## Grid Images (Multiple Molecules)

### Basic grid

```python
smiles_list = ['CCO', 'c1ccccc1', 'CC(=O)O', 'CC(=O)Oc1ccccc1C(=O)O',
               'CN1C=NC2=C1C(=O)N(C(=O)N2C)C', 'OC(=O)C(O)C(O)C(=O)O']
mols = [Chem.MolFromSmiles(s) for s in smiles_list]
# Filter None (invalid SMILES)
mols = [m for m in mols if m is not None]

img = Draw.MolsToGridImage(
    mols,
    molsPerRow=3,
    subImgSize=(300, 300),
    legends=[Chem.MolToSmiles(m) for m in mols],  # labels below each
)
img.save('grid.png')
```

### Grid with properties as legends

```python
from rdkit.Chem import Descriptors

legends = []
for mol in mols:
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    legends.append(f'MW: {mw:.1f}, LogP: {logp:.2f}')

img = Draw.MolsToGridImage(mols, molsPerRow=4, subImgSize=(350, 300),
                            legends=legends)
```

### SVG grid

```python
from rdkit.Chem.Draw import MolsToGridImage
# For SVG, use useSVG=True (returns SVG string, not PIL Image)
svg = Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(300, 250),
                            useSVG=True)
with open('grid.svg', 'w') as f:
    f.write(svg)
```

## Substructure Highlighting

### Highlight matching atoms

```python
mol = Chem.MolFromSmiles('c1ccc(CC(=O)O)cc1')
pattern = Chem.MolFromSmarts('C(=O)O')  # carboxylic acid
match = mol.GetSubstructMatch(pattern)

img = Draw.MolToImage(mol, size=(400, 300), highlightAtoms=match)
img.save('highlighted.png')
```

### Highlight with custom colors

```python
from rdkit.Chem.Draw import rdMolDraw2D

mol = Chem.MolFromSmiles('c1ccc(CC(=O)O)cc1')
pattern = Chem.MolFromSmarts('C(=O)O')
match = mol.GetSubstructMatch(pattern)

# Color atoms and bonds
atom_colors = {idx: (1, 0.4, 0.4) for idx in match}  # RGB tuples
bond_colors = {}
for bond in mol.GetBonds():
    if bond.GetBeginAtomIdx() in match and bond.GetEndAtomIdx() in match:
        bond_colors[bond.GetIdx()] = (1, 0.4, 0.4)

drawer = rdMolDraw2D.MolDraw2DSVG(400, 300)
drawer.DrawMolecule(mol, highlightAtoms=list(match),
                    highlightAtomColors=atom_colors,
                    highlightBonds=list(bond_colors.keys()),
                    highlightBondColors=bond_colors)
drawer.FinishDrawing()
svg = drawer.GetDrawingText()
```

### Multiple substructure matches

```python
matches = mol.GetSubstructMatches(pattern)
all_atoms = [atom for match in matches for atom in match]
img = Draw.MolToImage(mol, highlightAtoms=all_atoms)
```

## Similarity Maps

Visualize atomic contributions to molecular similarity or properties.

```python
from rdkit.Chem.Draw import SimilarityMaps
from rdkit.Chem import AllChem

mol = Chem.MolFromSmiles('c1ccc(CC(=O)O)cc1')
ref = Chem.MolFromSmiles('c1ccccc1')

fig, maxweight = SimilarityMaps.GetSimilarityMapFromFingerprint(
    ref, mol,
    lambda m, i: SimilarityMaps.GetMorganFingerprint(m, i, radius=2, nBits=1024),
    colorMap='RdBu_r',
    size=(400, 300),
)
fig.savefig('similarity_map.png', dpi=150, bbox_inches='tight')
```

## Molecular Descriptors

```python
from rdkit.Chem import Descriptors

mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')

mw = Descriptors.MolWt(mol)                    # molecular weight
logp = Descriptors.MolLogP(mol)                 # partition coefficient
hbd = Descriptors.NumHDonors(mol)               # H-bond donors
hba = Descriptors.NumHAcceptors(mol)            # H-bond acceptors
tpsa = Descriptors.TPSA(mol)                    # topological polar surface area
rotatable = Descriptors.NumRotatableBonds(mol)  # rotatable bonds
rings = Descriptors.RingCount(mol)              # ring count
```

### Lipinski Rule of Five filter

```python
def passes_lipinski(mol):
    return (Descriptors.MolWt(mol) <= 500 and
            Descriptors.MolLogP(mol) <= 5 and
            Descriptors.NumHDonors(mol) <= 5 and
            Descriptors.NumHAcceptors(mol) <= 10)
```

## Drawing Options (MolDrawOptions)

```python
drawer = rdMolDraw2D.MolDraw2DSVG(400, 300)
opts = drawer.drawOptions()

opts.atomLabelFontSize = 14
opts.bondLineWidth = 2.0
opts.addAtomIndices = True           # show atom numbers
opts.addStereoAnnotation = True      # show R/S, E/Z labels
opts.setBackgroundColour((1, 1, 1, 1))  # white background (RGBA)
opts.legendFontSize = 12

# Atom color palette (element -> RGB)
opts.setAtomPalette({
    6: (0.1, 0.1, 0.1),    # Carbon: dark gray
    7: (0.0, 0.0, 0.8),    # Nitrogen: blue
    8: (0.8, 0.0, 0.0),    # Oxygen: red
    16: (0.8, 0.8, 0.0),   # Sulfur: yellow
})

drawer.DrawMolecule(mol)
drawer.FinishDrawing()
```

## Integration with Matplotlib

### Embed RDKit image in matplotlib subplot

```python
import matplotlib.pyplot as plt
from rdkit.Chem import Draw
import numpy as np
from PIL import Image
import io

mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')
img = Draw.MolToImage(mol, size=(400, 300))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Left: molecule image
axes[0].imshow(np.array(img))
axes[0].axis('off')
axes[0].set_title('Aspirin')

# Right: property bar chart
props = {'MW': 180.2, 'LogP': 1.2, 'HBD': 1, 'HBA': 4, 'TPSA': 63.6}
axes[1].barh(list(props.keys()), list(props.values()), color='steelblue')
axes[1].set_title('Molecular Properties')

fig.tight_layout()
fig.savefig('mol_with_properties.png', dpi=200, bbox_inches='tight')
```

### Multi-molecule panel figure

```python
smiles_dict = {
    'Aspirin': 'CC(=O)Oc1ccccc1C(=O)O',
    'Ibuprofen': 'CC(C)Cc1ccc(cc1)C(C)C(=O)O',
    'Caffeine': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
    'Paracetamol': 'CC(=O)Nc1ccc(O)cc1',
}

fig, axes = plt.subplots(2, 2, figsize=(8, 8))
for ax, (name, smi) in zip(axes.flat, smiles_dict.items()):
    mol = Chem.MolFromSmiles(smi)
    img = Draw.MolToImage(mol, size=(400, 400))
    ax.imshow(np.array(img))
    ax.axis('off')
    mw = Descriptors.MolWt(mol)
    ax.set_title(f'{name}\nMW: {mw:.1f}', fontsize=11)

fig.suptitle('Common Analgesics', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig('analgesics.png', dpi=200, bbox_inches='tight')
```

## Common Gotchas

1. **`MolFromSmiles` returns None for invalid SMILES** — no exception raised. Always check: `if mol is None: handle_error()`.
2. **Kekulization errors** — some SMILES need sanitization. Try `Chem.MolFromSmiles(smi, sanitize=False)` then `Chem.SanitizeMol(mol)` with error handling.
3. **Hydrogen display** — by default, H atoms are implicit. Use `Chem.AddHs(mol)` to show all hydrogens (important for 3D conformer generation).
4. **2D coordinates** — `Draw.MolToImage()` auto-generates 2D coords. For explicit control: `AllChem.Compute2DCoords(mol)`.
5. **Large grids** — `MolsToGridImage` loads all molecules into memory. For >100 molecules, batch or paginate.
6. **PNG metadata** — RDKit embeds SMILES in PNG metadata. Round-trip with `Chem.MolsFromPNGString(png_bytes)`.