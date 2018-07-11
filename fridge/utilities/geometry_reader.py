import numpy as np
import pandas as pd
import glob
import os
import yaml

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/assembly")


def fuel_assembly_geometry_reader(assembly_type):
    """This function reads in the geometry/material contributions for a single
    fuel assembly.

    This includes fuel pin height/pitch/fuel type, etc. It
    returns a Data Structure with all the relevant geometry/material
    information to then start creating MCNP geometries and materials.

    args:
        assembly_type (str array): Name of the assembly type that will be used

    return:
        fuel_data (Data Frame): Contains all the geometric and material components for the fuel
        assembly_data (Data Frame): Contains all the geometric and material components for the assembly
        plenum_data (Data Frame): Contains all the geometric and material components for the plenum
        fuel_reflector_data (Data Frame): Contains all the geometric and material components for the fuel reflector

    """
    assembly_file = glob.glob(os.path.join(geo_dir, assembly_type + '.*'))
    assembly_yaml_file = glob.glob(os.path.join(geo_dir, 'A271.yaml'))


    if assembly_file == []:
        print('\n\033[1;37;31mFatal Error: No assembly type named %s. \nChange your assembly type to a previously created assembly, '
              'or create a new assembly using the utilities.' % assembly_type)
        quit()

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

    with open(assembly_yaml_file[0], "r") as mat_file:

        inputs = yaml.load(mat_file)
        fuel_diameter = float(inputs["Pin_Diameter"])
        plenum_height = float(inputs['Plenum Height'])
        plenum_smear = [float(i) for i in inputs['Plenum Smear']]
        plenum_material = inputs["Plenum Material"]
        plenum_Data = [plenum_height, plenum_smear[0], plenum_smear[1], plenum_smear[2], plenum_material[0], plenum_material[1], plenum_material[2]]
        plenum_Data = pd.DataFrame(plenum_Data,
                               columns=['plenum'],
                               index=['height', 'coolant_per', 'void_per', 'clad_per', 'coolant', 'void', 'clad'])


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
                               index=['height', 'coolant_per', 'void_per', 'clad_per'])
    plenum_materials = pd.DataFrame(plenum_materials,
                                    columns=['plenum'],
                                    index=['coolant', 'void', 'clad'])
    plenum_data = pd.concat([plenum_data, plenum_materials])

    # Accumulate and organize the fuel reflector data/materials
    fuel_reflector_data = np.append(fuel_reflector_data, fuel_reflector_materials_smears)

    fuel_reflector_data = pd.DataFrame(fuel_reflector_data,
                                       columns=['fuel_reflector'],
                                       index=['height', 'coolant_per', 'clad_per'])
    fuel_reflector_materials = pd.DataFrame(fuel_reflector_materials,
                                            columns=['fuel_reflector'],
                                            index=['coolant', 'clad'])
    fuel_reflector_data = pd.concat([fuel_reflector_data, fuel_reflector_materials])


    return fuel_data, assembly_data, plenum_data, fuel_reflector_data
