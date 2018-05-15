from FRIDGe.fridge.utilities import material_smear as ms


def test_material_smear():
#    atom_percent, atom_density = ms.material_smear([1, 2], [1, 2], ['27U'])

    atom_percent, atom_density = ms.material_smear([1, 2], [0.3, 0.7], ['Liquid_Na', 'HT9'])
    print(atom_percent)
    print(atom_density)


test_material_smear()