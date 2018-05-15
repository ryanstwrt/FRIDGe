from FRIDGe.fridge.input_readers import material_reader as mr
import glob
import os

cur_dir = os.path.dirname(__file__)
mat_dir = os.path.join(cur_dir, "../Materials")

def material_smear(materials, material_wt_per, material_str):
    material_name = ''
    for iter, name in enumerate(material_str):
        if iter+1 == len(material_str):
            material_name += str(name)
        else:
            material_name += str(name) + '_'

    # Check to see if the material smear already exists
    material_dir = '../Materials/' + material_name + '.txt'
    material_exist = os.path.isfile(material_dir)
    if material_exist:
        atom_percent, atom_density = mr.material_reader([material_name])
        return atom_percent, atom_density

