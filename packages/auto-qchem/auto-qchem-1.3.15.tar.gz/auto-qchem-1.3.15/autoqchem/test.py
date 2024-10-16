# reproduce error

def reproduce(smiles, num_conf=3, rdkit_ff='MMFF94'):

    import os
    from rdkit import Chem, Geometry
    from rdkit.Chem import AllChem

    # get threads
    n_threads = os.cpu_count() - 1

    # initialize rdmol
    rdmol = Chem.AddHs(Chem.MolFromSmiles(smiles))

    params = AllChem.EmbedParameters()
    params.useSymmetryForPruning = True
    params.useSmallRingTorsions = True
    params.useMacrocycleTorsions = True
    params.ETversion = 2
    params.pruneRmsThresh = 0.35
    params.numThreads = n_threads
    params.useRandomCoords = True

    # embed and optimized conformers
    AllChem.EmbedMultipleConfs(rdmol, num_conf, params)
    if rdkit_ff == "MMFF94":
        AllChem.MMFFOptimizeMoleculeConfs(rdmol, mmffVariant="MMFF94", numThreads=n_threads)
    elif rdkit_ff == "MMFF94s":
        AllChem.MMFFOptimizeMoleculeConfs(rdmol, mmffVariant="MMFF94s", numThreads=n_threads)
    elif rdkit_ff == "UFF":
        AllChem.UFFOptimizeMoleculeConfs(rdmol, numThreads=n_threads)


    # elements, conformer_coordinates, connectivity_matrix, charges = extract_from_rdmol(rdmol)
    #
    # return elements, conformer_coordinates, connectivity_matrix, charges

if __name__ == '__main__':
    from db_functions import get_all_conformer_data
    get_all_conformer_data(tags=['ArBr_lit_SJ'])