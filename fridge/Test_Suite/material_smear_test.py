from FRIDGe.fridge.utilities import material_smear as ms


def test_material_smear():
    atom_percent, atom_density = ms.material_smear([1, 2], [1, 2], ['27U'])
    print(atom_percent)
    print(atom_density)

test_material_smear()