import numpy as np
import pandas as pd
import glob
import os

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "Geometry")


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

    pin_data = np.zeros(6)
    pin_materials = []
    assembly_data = np.zeros(6)
    assembly_materials = []
    plenum_data = np.zeros(1)
    plenum_materials = []
    fuel_reflector_data = np.zeros(1)
    fuel_reflector_materials = []
    with open(assembly_file[0], "r") as mat_file:
        for i, line in enumerate(mat_file):
            line = line.strip()
            holder = [x for x in line.split(' ')]
            if 0 < i < 10:
                if i > 6:
                    pin_materials.append(holder[1])
                else:
                    pin_data[i-1] = holder[1]
            elif 11 < i < 20:
                if i > 17:
                    assembly_materials.append(holder[1])
                else:
                    assembly_data[i-12] = holder[1]
            elif 21 < i < 25:
                if i == 23:
                    plenum_material_smears = holder[1:]
                elif i == 24:
                    plenum_materials = holder[1:]
                elif i == 22:
                    plenum_data[0] = holder[1]
            elif 26 < i < 30:
                if i == 28:
                    fuel_reflector_materials = holder[1:]
                elif i == 29:
                    fuel_reflector_material_smears = holder[1:]
                else:
                    fuel_reflector_data[0] = holder[1]

    fuel_data = np.concatenate([pin_data,pin_materials])
    fuel_data = pd.DataFrame(fuel_data,
                             columns=['fuel'],
                             index=['pin_diameter', 'clad_thickness', 'fuel_smear', 'pitch', 'wire_wrap_diameter',
                                    'height', 'fuel', 'clad', 'bond'])
    assembly_data = np.concatenate([assembly_data,assembly_materials])
    assembly_data = pd.DataFrame(assembly_data,
                                 columns=['assembly'],
                                 index=['pins_per_assembly', 'assembly pitch', 'duct_thickness',
                                        'assembly_gap', 'inside_flat_to_flat', 'height', 'coolant', 'assembly'])
    plenum_data = np.concatenate([plenum_data, plenum_material_smears])
    plenum_data = pd.DataFrame(plenum_data,
                               columns=['plenum'],
                               index=['height', plenum_materials[0], plenum_materials[1], plenum_materials[2]])
    fuel_reflector_data = np.concatenate([fuel_reflector_data, fuel_reflector_materials])
    fuel_reflector_data = pd.DataFrame(fuel_reflector_data,
                                       columns=['fuel_reflector'],
                                       index=['height', fuel_reflector_material_smears[0], fuel_reflector_material_smears[1]])
    return


fuel_assembly_geometry_reader(['A271'])
