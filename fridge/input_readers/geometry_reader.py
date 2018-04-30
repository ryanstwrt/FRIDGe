import numpy as np
import pandas as pd
import glob
import os

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../Geometry")


def fuel_assembly_geometry_reader(assembly_type):
    """This function reads in the geometry/material contributions for a single
    fuel assembly.

    This includes fuel pin height/pitch/fuel type, etc. It
    returns a Data Structure with all the relevant geometry/material
    information to then start creating MCNP geometries and materials.

    args:
        assembly_type (str array): Name of the assembly type that will be used

    return:
        fuel_assembly (Data Frame): Contains all the geometric components
        and the materials for each component.
    """
    assembly_file = glob.glob(os.path.join(geo_dir, assembly_type[0] + '.*'))

    fuel_data = np.zeros(6)
    fuel_materials = []
    assembly_data = np.zeros(6)
    assembly_materials = []
    plenum_data = np.zeros(1)
    plenum_materials = []
    plenum_material_smears = np.zeros(3)
    fuel_reflector_data = np.zeros(1)
    fuel_reflector_materials = []
    fuel_reflector_materials_smears = np.zeros(2)

    with open(assembly_file[0], "r") as mat_file:
        for i, line in enumerate(mat_file):
            line = line.strip()
            holder = [x for x in line.split(' ')]
            if 0 < i < 10:
                if i > 6:
                    fuel_materials.append(holder[1])
                else:
                    fuel_data[i - 1] = holder[1]
            elif 11 < i < 20:
                if i > 17:
                    assembly_materials.append(holder[1])
                else:
                    assembly_data[i - 12] = holder[1]
            elif 21 < i < 25:
                if i == 23:
                    plenum_material_smears[0:] = holder[1:]
                elif i == 24:
                    plenum_materials = holder[1:]
                elif i == 22:
                    plenum_data[0] = holder[1]
            elif 26 < i < 30:
                if i == 29:
                    fuel_reflector_materials = holder[1:]
                elif i == 28:
                    fuel_reflector_materials_smears[0:] = holder[1:]
                else:
                    fuel_reflector_data[0] = holder[1]

    # Accumulate and organize the fuel data/materials
    fuel_data = pd.DataFrame(fuel_data, columns=['fuel'],
                             index=['pin_diameter', 'clad_thickness', 'fuel_smear', 'pitch',
                                    'wire_wrap_diameter', 'height'])
    fuel_materials = pd.DataFrame(fuel_materials, columns=['fuel'],
                                  index=['fuel', 'clad', 'bond'])
    fuel_data = pd.concat([fuel_data, fuel_materials])

    # Accumulate and organize the assembly data/materials
    assembly_data = pd.DataFrame(assembly_data,
                                 columns=['assembly'],
                                 index=['pins_per_assembly', 'assembly_pitch', 'duct_thickness',
                                        'assembly_gap', 'inside_flat_to_flat', 'height'])
    assembly_materials = pd.DataFrame(assembly_materials,
                                      columns=['assembly'],
                                      index=['coolant', 'assembly'])
    assembly_data = pd.concat([assembly_data, assembly_materials])

    # Accumulate and organize the plenum data/materials
    plenum_data = np.append(plenum_data, plenum_material_smears)

    plenum_data = pd.DataFrame(plenum_data,
                               columns=['plenum'],
                               index=['height', 'coolant_per', 'void_per', 'cladding_per'])
    plenum_materials = pd.DataFrame(plenum_materials,
                                    columns=['plenum'],
                                    index=['coolant', 'void', 'cladding'])
    plenum_data = pd.concat([plenum_data, plenum_materials])

    # Accumulate and organize the fuel reflector data/materials
    fuel_reflector_data = np.append(fuel_reflector_data, fuel_reflector_materials_smears)

    fuel_reflector_data = pd.DataFrame(fuel_reflector_data,
                                       columns=['fuel_reflector'],
                                       index=['height', 'coolant_per', 'cladding_per'])
    fuel_reflector_materials = pd.DataFrame(fuel_reflector_materials,
                                            columns=['fuel_reflector'],
                                            index=['coolant', 'cladding'])
    fuel_reflector_data = pd.concat([fuel_reflector_data, fuel_reflector_materials])


    return fuel_data, assembly_data, plenum_data, fuel_reflector_data
