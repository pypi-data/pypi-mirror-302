import pandas as pd
from rdkit import Chem, Geometry
from rdkit.Chem import rdFMCS
from autoqchem.db_functions import db_select_molecules, descriptors_from_mol_df

mol_df = db_select_molecules(tags=['ArBr_lit_SJ'])
descs_df = descriptors_from_mol_df(mol_df, conf_option='boltzmann')
data = {}
df = pd.read_csv('list.csv')
cans = df['can'].tolist()
rd_mols = {can: Chem.MolFromSmiles(can) for can in cans}
sub = Chem.MolFromSmarts('c-Br')
matches = {can: rd_mols[can].GetSubstructMatches(sub)[0] for can in cans}
matches = pd.Series(matches).map(list)

tmp_df = descs_df.to_frame('descs')
tmp_df['matches'] = matches

sub_labels = [f"atom{i + 1}" for i in range(len(matches[0]))]
for i, label in enumerate(sub_labels):
    to_concat = []
    for c, row in tmp_df.iterrows():
        atom_descs = row['descs']['atom_descriptors']
        atom_descs['labels'] = row['descs']['labels']
        print(atom_descs['labels'].to_list())
        to_concat.append(atom_descs.iloc[row['matches'][i]])
    data[label] = pd.concat(to_concat, axis=1, sort=True)
    data[label].columns = descs_df.index
    data[label] = data[label].T

    to_concat = []
    for c, row in tmp_df.iterrows():
        atom_descs = row['descs']['atom_descriptors']
        atom_descs['labels'] = row['descs']['labels']
        atom_descs = atom_descs[~atom_descs['labels'].str.startswith("H")]  # need to remove hydrogens
        to_concat.append(atom_descs.iloc[row['matches'][i]])
    data[label] = pd.concat(to_concat, axis=1, sort=True)
    data[label].columns = descs_df.index
    data[label] = data[label].T