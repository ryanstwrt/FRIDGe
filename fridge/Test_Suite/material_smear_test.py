from FRIDGe.fridge.utilities import material_smear as ms
import glob
import os

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../Materials")

def test_material_smear():
    atom_percent, atom_density = ms.material_smear([0], [0], ['27U'])
    print(atom_percent)
    print(atom_density)

test_material_smear()