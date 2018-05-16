from FRIDGe.fridge.utilities import material_smear as ms
from FRIDGe.fridge.input_readers import material_reader as mr
import numpy as np


def test_material_smear():

    #test a material smear where there is only one material
    atom_percent, atom_density = ms.material_smear([1.0], ['27U'])
    true_atom_percent, true_atom_density = mr.material_reader(['27U'])
    assert atom_percent.all() == true_atom_percent.all()
    assert atom_density == true_atom_density

    atom_percent1, atom_density1 = ms.material_smear([0.3, 0.7], ['Liquid_Na', 'HT9'])
    atom_percent2, atom_density2 = ms.material_smear([0.7, 0.3], ['HT9', 'Liquid_Na'])

    assert np.allclose(atom_density1, atom_density2)
    assert atom_percent1.all() == atom_percent2.all()

test_material_smear()