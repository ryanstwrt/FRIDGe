from FRIDGe.fridge.utilities import material_smear as ms, material_reader as mr
import numpy as np


def test_material_smear():
    """
    Tests the material smear function.
    """
    # Test a material smear where there is only one material
    atom_percent, atom_density = ms.material_smear([1.0], ['27U'])
    true_atom_percent, true_atom_density = mr.material_reader(['27U'])
    assert atom_percent.all() == true_atom_percent.all()
    assert atom_density == true_atom_density

    # Test a material smear with two materials and ensure they give the same answer when swapped
    atom_percent1, atom_density1 = ms.material_smear([0.3, 0.7], ['Liquid_Na', 'HT9'])
    atom_percent2, atom_density2 = ms.material_smear([0.7, 0.3], ['HT9', 'Liquid_Na'])

    assert np.allclose(atom_density1, atom_density2)
    assert atom_percent1.all() == atom_percent2.all()

    # Test a material smear with a void in it
    atom_percent, atom_density = ms.material_smear([0.3, 0.7], ['Liquid_Na', 'Void'])
    true_atom_percent, true_atom_density = mr.material_reader(['Liquid_Na'])
    true_atom_percent = true_atom_percent * 0.3
    assert np.allclose(atom_density, true_atom_density * 0.3)
    assert np.allclose(atom_percent.all(), true_atom_percent.all())


test_material_smear()