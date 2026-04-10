# 3D Molecular Visualization

Interactive 3D molecular viewing with py3Dmol, conformer generation with RDKit, and protein visualization.

## py3Dmol Setup

```bash
pip install py3Dmol
```

```python
import py3Dmol

# Basic viewer
view = py3Dmol.view(width=600, height=400)
view.addModel(mol_block, 'mol')       # MOL format
view.addModel(pdb_string, 'pdb')      # PDB format
view.addModel(sdf_string, 'sdf')      # SDF format
view.addModel(xyz_string, 'xyz')      # XYZ format
view.setStyle({'stick': {}})
view.zoomTo()
view.show()  # renders in Jupyter
```

## RDKit to py3Dmol Pipeline

### Generate 3D conformer from SMILES

```python
from rdkit import Chem
from rdkit.Chem import AllChem

def smiles_to_3d(smiles):
    """Convert SMILES to 3D mol block for py3Dmol."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    mol = Chem.AddHs(mol)
    # Generate 3D coordinates
    result = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    if result == -1:
        raise RuntimeError("3D embedding failed")
    # Optimize geometry with MMFF force field
    AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
    return Chem.MolToMolBlock(mol)

mol_block = smiles_to_3d('CC(=O)Oc1ccccc1C(=O)O')  # aspirin
```

### Display in py3Dmol

```python
import py3Dmol

mol_block = smiles_to_3d('CC(=O)Oc1ccccc1C(=O)O')
view = py3Dmol.view(width=600, height=400)
view.addModel(mol_block, 'mol')
view.setStyle({'stick': {'radius': 0.15}, 'sphere': {'scale': 0.25}})
view.setBackgroundColor('white')
view.zoomTo()
view.show()
```

### Multiple conformers

```python
def generate_conformers(smiles, n_conf=10):
    """Generate multiple 3D conformers."""
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.numThreads = 0   # use all cores
    params.pruneRmsThresh = 0.5  # prune similar conformers
    AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params)
    # Optimize each conformer
    results = AllChem.MMFFOptimizeMoleculeConfs(mol, maxIters=500)
    return mol

mol = generate_conformers('c1ccc(CC(=O)O)cc1', n_conf=5)
# Get lowest energy conformer
energies = [(i, AllChem.MMFFGetMoleculeForceField(mol, AllChem.MMFFGetMoleculeProperties(mol), confId=i).CalcEnergy())
            for i in range(mol.GetNumConformers())]
best_conf = min(energies, key=lambda x: x[1])[0]
mol_block = Chem.MolToMolBlock(mol, confId=best_conf)
```

## Visualization Styles

### Available styles

| Style | Use | Example |
|---|---|---|
| `stick` | Default for small molecules | `{'stick': {'radius': 0.15}}` |
| `sphere` | Space-filling model | `{'sphere': {'scale': 1.0}}` |
| `line` | Wireframe (fast for large) | `{'line': {'linewidth': 1}}` |
| `cartoon` | Protein secondary structure | `{'cartoon': {'color': 'spectrum'}}` |
| `surface` | Molecular surface | Added separately |
| `cross` | Crosshair at atom positions | `{'cross': {'linewidth': 1}}` |

### Combined styles

```python
# Ball-and-stick
view.setStyle({'stick': {'radius': 0.12}, 'sphere': {'scale': 0.25}})

# Stick with element coloring (default)
view.setStyle({'stick': {'colorscheme': 'default'}})

# Custom coloring
view.setStyle({'stick': {'color': '0x3498db'}})           # single color
view.setStyle({'stick': {'colorscheme': 'Jmol'}})         # Jmol colors
view.setStyle({'stick': {'colorscheme': 'greenCarbon'}})   # green carbons
```

### Color schemes

`default`, `Jmol`, `rasmol`, `greenCarbon`, `cyanCarbon`, `magentaCarbon`, `yellowCarbon`, `whiteCarbon`, `orangeCarbon`, `purpleCarbon`

## Protein Visualization

### Load from PDB

```python
view = py3Dmol.view(query='pdb:1crn')  # fetch from RCSB PDB
view.setStyle({'cartoon': {'color': 'spectrum'}})
view.zoomTo()
view.show()
```

### Chain selection and styling

```python
view = py3Dmol.view(query='pdb:4HHB')  # hemoglobin

# Style different chains
view.setStyle({'chain': 'A'}, {'cartoon': {'color': 'blue'}})
view.setStyle({'chain': 'B'}, {'cartoon': {'color': 'red'}})
view.setStyle({'chain': 'C'}, {'cartoon': {'color': 'green'}})
view.setStyle({'chain': 'D'}, {'cartoon': {'color': 'orange'}})

# Show heme groups as sticks
view.setStyle({'resn': 'HEM'}, {'stick': {'colorscheme': 'greenCarbon'}})
view.zoomTo()
```

### Binding site highlighting

```python
view = py3Dmol.view(query='pdb:1ncr')

# Protein as transparent cartoon
view.setStyle({}, {'cartoon': {'color': 'white', 'opacity': 0.7}})

# Ligand as colored sticks
view.setStyle({'hetflag': True}, {'stick': {'colorscheme': 'greenCarbon',
                                             'radius': 0.2}})

# Binding site residues (within 5A of ligand)
view.addStyle({'within': {'distance': 5, 'sel': {'hetflag': True}}},
              {'stick': {'colorscheme': 'cyanCarbon', 'radius': 0.12}})
view.zoomTo({'hetflag': True})
```

### Surface

```python
# Transparent surface over cartoon
view.addSurface(py3Dmol.SAS,
    {'opacity': 0.5, 'color': 'white'},
    {'chain': 'A'})

# Electrostatic-like coloring
view.addSurface(py3Dmol.SAS,
    {'opacity': 0.7, 'colorscheme': {'prop': 'b', 'gradient': 'rwb',
                                      'min': 0, 'max': 100}})
```

## Saving and Export

### Static image from py3Dmol

```python
# In Jupyter, capture as PNG
png = view.png()  # returns base64 PNG data

# Save to file
import base64
with open('molecule_3d.png', 'wb') as f:
    f.write(base64.b64decode(png))
```

### HTML export

```python
html = view._make_html()
with open('molecule_viewer.html', 'w') as f:
    f.write(html)
```

### Embedding in presentations

For static images in slides/papers, py3Dmol's PNG output works. For interactive viewers, export as HTML and embed or share the HTML file.

## Alternative: NGLView

For heavier protein visualization (trajectories, large complexes):

```bash
pip install nglview
```

```python
import nglview as nv

view = nv.show_pdbid('1crn')
view.add_cartoon(selection='protein', color='sstruc')
view.add_ball_and_stick(selection='ligand')
view
```

NGLView supports MD trajectory playback, volume rendering, and more complex molecular scenes, but is heavier than py3Dmol.

## Common Patterns for Drug Discovery

### Compound library overview

```python
# RDKit grid for 2D overview + py3Dmol for selected compound drill-down
# Step 1: Generate grid image (see rdkit-visualization.md)
img = Draw.MolsToGridImage(mols, molsPerRow=5, legends=names)
img.save('library_overview.png')

# Step 2: 3D view of selected compound
mol_block = smiles_to_3d(selected_smiles)
view = py3Dmol.view(width=600, height=400)
view.addModel(mol_block, 'mol')
view.setStyle({'stick': {}, 'sphere': {'scale': 0.3}})
view.zoomTo()
```

### Ligand overlay

```python
view = py3Dmol.view(width=600, height=400)
colors = ['0x3498db', '0xe74c3c', '0x2ecc71']

for i, smi in enumerate(smiles_list):
    mol_block = smiles_to_3d(smi)
    view.addModel(mol_block, 'mol')
    view.setStyle({'model': i}, {'stick': {'color': colors[i % len(colors)]}})

view.zoomTo()
```
