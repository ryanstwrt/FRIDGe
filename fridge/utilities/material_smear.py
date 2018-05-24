from FRIDGe.fridge.utilities import material_reader as mr
import numpy as np
import pandas as pd

AVOGADROS_NUMBER = 0.6022140857


def material_smear(material_wt_per, material_str):
    """
        Calculates the atom percent of a material given multiuple materials.

        args:
            material_wt_per (double array): array with all isotopes present in
            the material in weight percent
            material_str (str array): array with the name of each material

        returns:
            atom_percent (double array): array with all isotopes present in
                the material in smeared at%
            atom_density (double): the total atom density of the smeared material
    """
    assert material_str
    for iter, name in enumerate(material_str):
        if name == 'Void' or name == 'void':
            material_str.remove('Void')
            material_wt_per.pop(iter)

    wt_per = material_creator(material_wt_per, material_str)
    atom_percent, atom_density = smear_wt2at_per(wt_per)
    return atom_percent, atom_density


def material_creator(material_wt_per, material_str):
    """
        Calculates the weight percent of a material given multiuple materials.

        args:
            material_wt_per (double array): array with all isotopes present in
            the material in weight percent
            material_str (str array): array with the name of each material

        returns:
            material_array (double array): array with all isotopes present in
                the material in smeared wt %
    """
    material_array = pd.DataFrame
    density_array = np.zeros(len(material_str))
    for iter, material_name in enumerate(material_str):
        wt_per, material_density = mr.get_final_wt_per([material_name])
        temp, temp1 = mr.material_reader([material_name])
        temp = pd.DataFrame(temp, columns=['element', 'zaid', 'mass_number', 'wt_per', 'density', 'linear expansion'])
        temp.wt_per = wt_per[:, 3] * material_wt_per[iter]
        temp.density = material_density
        density_array[iter] = material_density

        if iter == 0:
            material_array = temp
        else:
            material_array = pd.concat([material_array, temp])

    if round(material_array['wt_per'].sum(), 15) != 1.0:
        print('\033[1;37:33mWarning: Smear material with %s had a weight fraction of %f and was not normlized to 1. '
              'Check to make sure the material or element card is correct'
              % (material_str, material_array['wt_per'].sum()))

    material_array = material_array.as_matrix()

    return material_array


# Need to create a new wt to atom percent to maintain smearing atom densities.
def smear_wt2at_per(wt_per):
    """Converts the array of wt % to atom % and returns the atom density for use
       in the cell cards.

    The fifth step in getting a material.

    args:
        wt_per (double array): array with all isotopes present in
        the material in weight percent

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

def wire_wrap_smear(assembly):
    wire_wrap_radius = assembly.pin.pin_data.ix['wire_wrap_diameter', 'fuel'] / 2
    fuel_pin_height = assembly.pin.pin_data.ix['height', 'fuel']
    fuel_pin_pitch = assembly.pin.pin_data.ix['pitch', 'fuel']
    fuel_pin_or = assembly.pin.pin_data.ix['pin_diameter', 'fuel'] / 2

    wire_wrap_vol = np.power(wire_wrap_radius,2) * np.pi * fuel_pin_height
    fuel_pin_vol = np.power(fuel_pin_or,2) * np.pi * fuel_pin_height
    coolant_vol = (3/2) * np.sqrt(3) * fuel_pin_height * np.power(fuel_pin_pitch,2) - fuel_pin_vol - wire_wrap_vol
    total_volume = wire_wrap_vol + coolant_vol
    wire_wrap_per = wire_wrap_vol / total_volume
    coolant_vol_per = coolant_vol / total_volume
    return wire_wrap_per, coolant_vol_per