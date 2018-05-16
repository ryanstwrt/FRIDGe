from FRIDGe.fridge.input_readers import material_reader as mr
import numpy as np
import pandas as pd
import glob
import os

cur_dir = os.path.dirname(__file__)
mat_dir = os.path.join(cur_dir, "../Materials")


def material_smear(material_wt_per, material_str):
    assert material_str
    material_name = ''
    for iter, name in enumerate(material_str):
        if iter+1 == len(material_str):
            material_name += str(name)
        else:
            material_name += str(name) + '_'
    material_dir = '../Materials/' + material_name + '.txt'
    material_exist = os.path.isfile(material_dir)
    #if material_exist:
    #    atom_percent, atom_density = mr.material_reader([material_name])
    #    return atom_percent, atom_density

    wt_per = material_creator(material_wt_per, material_str)
    atom_percent, atom_density = mr.wt2at_per(wt_per, [wt_per[0, 4]])
    return atom_percent, atom_density

def material_creator(material_wt_per, material_str):
    """
        Augments the wt

    """
    smear_density = 0
    for iter, material_name in enumerate(material_str):
        wt_per, material_density = mr.get_final_wt_per([material_name])
        temp, temp1 = mr.material_reader([material_name])
        temp = pd.DataFrame(temp, columns=['element', 'zaid', 'mass_number', 'wt_per', 'density', 'linear expansion'])
        temp.wt_per = wt_per[:, 3] * material_wt_per[iter]
        temp.density = material_density

        # create a uniform density using the law of mixtures a_12 = a_1 * wt%_1 + a2 * wt%_2 + ...
        smear_density += material_density * material_wt_per[iter]

        if iter == 0:
            material_array = temp
        else:
            material_array = pd.concat([material_array, temp])

    material_array.density = smear_density

    if round(material_array['wt_per'].sum(), 15) != 1.0:
        print('\033[1;37:33mWarning: Smear material with %s had a weight fraction of %f and was not normlized to 1. '
              'Check to make sure the material or element card is correct' % (material_str, material_array['wt_per'].sum()))

    material_array = material_array.as_matrix()

    return material_array
