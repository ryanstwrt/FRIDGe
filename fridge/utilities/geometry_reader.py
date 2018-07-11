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
    assembly_yaml_file = glob.glob(os.path.join(geo_dir, assembly_type + '.yaml'))
    #assembly_yaml_file = glob.glob(os.path.join(geo_dir, 'A271.yaml'))


    if assembly_yaml_file == []:
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
        fuel_diameter = float(inputs["Pin Diameter"])
        clad_thickness = float(inputs['Clad Thickness'])
        fuel_smear = float(inputs['Fuel Smear'])
        fuel_pitch = float(inputs['Pitch'])
        wire_wrap_diameter = float(inputs['Wire Wrap Diameter'])
        height = float(inputs['Fuel Height'])
        fuel = inputs['Fuel']
        clad = inputs['Clad']
        bond = inputs['Bond']
        fuel_data = [fuel_diameter, clad_thickness, fuel_smear, fuel_pitch, wire_wrap_diameter, height, fuel, clad, bond]
        fuel_data = pd.DataFrame(fuel_data, columns=['fuel'], index = ['pin_diameter', 'clad_thickness', 'fuel_smear', 'pitch',
                                    'wire_wrap_diameter', 'height', 'fuel', 'clad', 'bond'])

        plenum_height = float(inputs['Plenum Height'])
        plenum_smear = [float(i) for i in inputs['Plenum Smear']]
        plenum_material = inputs["Plenum Material"]
        plenum_data = [plenum_height, plenum_smear[0], plenum_smear[1], plenum_smear[2], plenum_material[0], plenum_material[1], plenum_material[2]]
        plenum_data = pd.DataFrame(plenum_data,
                               columns=['plenum'],
                               index=['height', 'coolant_per', 'void_per', 'clad_per', 'coolant', 'void', 'clad'])

        fuel_reflector_height = float(inputs['Fuel Reflector Height'])
        fuel_reflector_smear = [float(i) for i in inputs['Smear']]
        fuel_reflector_material = inputs['Material']
        fuel_reflector_data = [fuel_reflector_height, fuel_reflector_smear[0], fuel_reflector_smear[1], fuel_reflector_material[0], fuel_reflector_material[1]]
        fuel_reflector_data = pd.DataFrame(fuel_reflector_data, columns=['fuel_reflector'],
                                           index=['height', 'coolant_per', 'clad_per', 'coolant', 'clad'])

        pins_per_assembly = float(inputs['Pins Per Assembly'])
        assembly_pitch = float(inputs['Assembly Pitch'])
        duct_thickness = float(inputs['Duct Thickness'])
        assembly_gap = float(inputs['Assembly Gap'])
        duct_inner_flat_to_flat = float(inputs['Duct Inside Flat to Flat'])
        assembly_height = float(inputs['Assembly Height'])
        coolant = inputs['Coolant']
        assembly_material = inputs['Assembly Material']
        assembly_data = [pins_per_assembly, assembly_pitch, duct_thickness, assembly_gap, duct_inner_flat_to_flat,
                         assembly_height, coolant, assembly_material]
        assembly_data = pd.DataFrame(assembly_data, columns=['assembly'], index=['pins_per_assembly', 'assembly_pitch', 'duct_thickness',
                                        'assembly_gap', 'inside_flat_to_flat', 'height', 'coolant', 'assembly'])

        return fuel_data, assembly_data, plenum_data, fuel_reflector_data