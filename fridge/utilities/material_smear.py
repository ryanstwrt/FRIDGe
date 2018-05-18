from FRIDGe.fridge.input_readers import material_reader as mr
import numpy as np
import pandas as pd
import glob
import os

AVOGADROS_NUMBER = 0.6022140857

cur_dir = os.path.dirname(__file__)
mat_dir = os.path.join(cur_dir, "../Materials")


def material_smear(material_wt_per, material_str):
    assert material_str
    for iter, name in enumerate(material_str):
        if name == 'Void' or name == 'void':
            material_str.remove('Void')
            material_wt_per.pop(iter)

    wt_per, wt_per_den = material_creator(material_wt_per, material_str)
    atom_percent, atom_density = smear_wt2at_per(wt_per)
    return atom_percent, atom_density

def material_creator(material_wt_per, material_str):
    """
        Augments the wt

    """
    smear_density = 0
    material_array = pd.DataFrame
    density_array = np.zeros(len(material_str))
    for iter, material_name in enumerate(material_str):
        wt_per, material_density = mr.get_final_wt_per([material_name])
        temp, temp1 = mr.material_reader([material_name])
        temp = pd.DataFrame(temp, columns=['element', 'zaid', 'mass_number', 'wt_per', 'density', 'linear expansion'])
        temp.wt_per = wt_per[:, 3] * material_wt_per[iter]
        temp.density = material_density
        density_array[iter] = material_density
        # create a uniform density using the law of mixtures a_12 = a_1 * wt%_1 + a2 * wt%_2 + ...
        #smear_density += material_density * material_wt_per[iter]

        if iter == 0:
            material_array = temp
        else:
            material_array = pd.concat([material_array, temp])
    print(material_array)
    #material_array.density = smear_density
    print(material_array)

    if round(material_array['wt_per'].sum(), 15) != 1.0:
        print('\033[1;37:33mWarning: Smear material with %s had a weight fraction of %f and was not normlized to 1. '
              'Check to make sure the material or element card is correct' % (material_str, material_array['wt_per'].sum()))

    material_array = material_array.as_matrix()

    return material_array, material_density


# Need to create a new wt to atom percent to maintain smearing atom densities.
def smear_wt2at_per(wt_per):
    """Converts the array of wt % to atom % and returns the atom density for use
       in the cell cards.

    The fifth step in getting a material.

    args:
        wt_per (double array): array with all isotopes present in
        the material in weight percent
        attr (double array): Array with the known attributes for a material

    returns:
        at_per (double array): array with all isotopes present in
        the material in atom percent
        atom_density (double): the total atom density for the material
    """
    at_den = np.zeros(len(wt_per))
    at_per = np.copy(wt_per)
    at_den_sum = 0
    at_per_sum = 0
    # Get the total atom density (to be used in the cell card and for the
    # atom percent)
    for i, isotope in enumerate(wt_per):
        at_den[i] = isotope[3] * wt_per[i, 4] * AVOGADROS_NUMBER / isotope[2]
        at_den_sum += at_den[i]
    for i, isotope in enumerate(wt_per):
        at_per[i][3] = at_den[i] / at_den_sum
        at_per_sum += at_per[i][3]
    if round(at_per_sum, 15) != 1:
        print('\033[1;37;33mWARNING: The atom percent of %s was %f and not normalized to 1. '
              'Check element to determine error' % (at_per[:, 1], at_per_sum))
    return at_per, at_den_sum