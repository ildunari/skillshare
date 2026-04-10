"""RDKit molecular visualization helpers.

Usage:
    from rdkit_helpers import (mol_grid, validate_smiles, mol_with_properties,
                                highlight_substructure, similarity_map)
"""

from typing import Optional


def _check_rdkit():
    """Check RDKit availability and return imports."""
    try:
        from rdkit import Chem
        from rdkit.Chem import Draw, AllChem, Descriptors
        from rdkit.Chem.Draw import rdMolDraw2D
        return Chem, Draw, AllChem, Descriptors, rdMolDraw2D
    except ImportError:
        raise ImportError(
            "RDKit is not installed. Install via conda:\n"
            "  conda install -c conda-forge rdkit\n"
            "RDKit is not pip-installable on all platforms."
        )


def validate_smiles(smiles_list):
    """Validate a list of SMILES strings.

    Parameters
    ----------
    smiles_list : list of str

    Returns
    -------
    dict with keys:
        'valid': list of (smiles, mol) tuples
        'invalid': list of smiles strings that failed
    """
    Chem, *_ = _check_rdkit()
    valid = []
    invalid = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            valid.append((smi, mol))
        else:
            invalid.append(smi)
    if invalid:
        print(f"Warning: {len(invalid)} invalid SMILES: {invalid}")
    return {'valid': valid, 'invalid': invalid}


def mol_grid(smiles_list, labels=None, mols_per_row=4, img_size=(350, 300),
             show_properties=False, output=None):
    """Generate a molecular grid image from SMILES.

    Parameters
    ----------
    smiles_list : list of str
        SMILES strings.
    labels : list of str, optional
        Labels below each molecule. If None and show_properties is True,
        shows MW and LogP.
    mols_per_row : int
    img_size : tuple of (width, height)
    show_properties : bool
        If True and labels is None, auto-generate MW/LogP labels.
    output : str, optional
        Save path (.png or .svg). If None, returns image object.

    Returns
    -------
    PIL.Image or str (SVG) or None (if saved to file)
    """
    Chem, Draw, _, Descriptors, _ = _check_rdkit()

    mols = []
    valid_labels = []
    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            mols.append(mol)
            if labels is not None:
                valid_labels.append(labels[i] if i < len(labels) else '')
            elif show_properties:
                mw = Descriptors.MolWt(mol)
                logp = Descriptors.MolLogP(mol)
                valid_labels.append(f'MW: {mw:.1f}, LogP: {logp:.2f}')
        else:
            print(f"Skipping invalid SMILES: {smi}")

    if not mols:
        raise ValueError("No valid molecules to draw")

    use_svg = output and output.endswith('.svg')

    if use_svg:
        svg = Draw.MolsToGridImage(mols, molsPerRow=mols_per_row,
                                    subImgSize=img_size,
                                    legends=valid_labels or None,
                                    useSVG=True)
        if output:
            with open(output, 'w') as f:
                f.write(svg)
            print(f'Saved: {output}')
            return None
        return svg

    img = Draw.MolsToGridImage(mols, molsPerRow=mols_per_row,
                                subImgSize=img_size,
                                legends=valid_labels or None)
    if output:
        img.save(output)
        print(f'Saved: {output}')
        return None
    return img


def mol_with_properties(smiles, output=None, size=(500, 400)):
    """Draw a single molecule with property annotations.

    Parameters
    ----------
    smiles : str
    output : str, optional
    size : tuple

    Returns
    -------
    dict with 'image' (PIL.Image) and 'properties' (dict)
    """
    Chem, Draw, _, Descriptors, _ = _check_rdkit()

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    props = {
        'SMILES': Chem.MolToSmiles(mol, canonical=True),
        'Molecular Weight': round(Descriptors.MolWt(mol), 2),
        'LogP': round(Descriptors.MolLogP(mol), 2),
        'H-Bond Donors': Descriptors.NumHDonors(mol),
        'H-Bond Acceptors': Descriptors.NumHAcceptors(mol),
        'TPSA': round(Descriptors.TPSA(mol), 2),
        'Rotatable Bonds': Descriptors.NumRotatableBonds(mol),
        'Rings': Descriptors.RingCount(mol),
        'Lipinski Passes': (Descriptors.MolWt(mol) <= 500 and
                            Descriptors.MolLogP(mol) <= 5 and
                            Descriptors.NumHDonors(mol) <= 5 and
                            Descriptors.NumHAcceptors(mol) <= 10),
    }

    img = Draw.MolToImage(mol, size=size)
    if output:
        img.save(output)
        print(f'Saved: {output}')

    return {'image': img, 'properties': props}


def highlight_substructure(smiles, smarts_pattern, output=None,
                           size=(400, 300), color=(1, 0.4, 0.4)):
    """Draw a molecule with substructure highlighted.

    Parameters
    ----------
    smiles : str
        Target molecule SMILES.
    smarts_pattern : str
        SMARTS pattern to highlight.
    output : str, optional
    size : tuple
    color : tuple of (R, G, B) floats 0-1

    Returns
    -------
    SVG string
    """
    Chem, _, _, _, rdMolDraw2D = _check_rdkit()

    mol = Chem.MolFromSmiles(smiles)
    pattern = Chem.MolFromSmarts(smarts_pattern)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    if pattern is None:
        raise ValueError(f"Invalid SMARTS: {smarts_pattern}")

    matches = mol.GetSubstructMatches(pattern)
    if not matches:
        print(f"No match found for pattern {smarts_pattern}")
        all_atoms = []
    else:
        all_atoms = list(set(atom for match in matches for atom in match))

    atom_colors = {idx: color for idx in all_atoms}

    bond_list = []
    bond_colors = {}
    for bond in mol.GetBonds():
        a1, a2 = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        if a1 in all_atoms and a2 in all_atoms:
            bond_list.append(bond.GetIdx())
            bond_colors[bond.GetIdx()] = color

    drawer = rdMolDraw2D.MolDraw2DSVG(*size)
    drawer.DrawMolecule(mol, highlightAtoms=all_atoms,
                        highlightAtomColors=atom_colors,
                        highlightBonds=bond_list,
                        highlightBondColors=bond_colors)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()

    if output:
        with open(output, 'w') as f:
            f.write(svg)
        print(f'Saved: {output}')

    return svg


def smiles_to_3d_molblock(smiles, optimize=True):
    """Convert SMILES to 3D mol block for py3Dmol.

    Parameters
    ----------
    smiles : str
    optimize : bool
        If True, optimize geometry with MMFF.

    Returns
    -------
    str : MOL block with 3D coordinates
    """
    Chem, _, AllChem, _, _ = _check_rdkit()

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")

    mol = Chem.AddHs(mol)
    result = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    if result == -1:
        raise RuntimeError(f"3D embedding failed for: {smiles}")

    if optimize:
        AllChem.MMFFOptimizeMolecule(mol, maxIters=500)

    return Chem.MolToMolBlock(mol)
