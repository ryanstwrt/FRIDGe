import numpy as np
import FRIDGe.fridge.input_readers.material_reader as mat_read
import FRIDGe.fridge.utilities.material_smear as mat_smear
import FRIDGe.fridge.driver.data_maker as dm
from FRIDGe.fridge.utilities.mcnp_cell_writer import mcnp_make_concentric_cell, mcnp_make_cell, mcnp_make_cell_outside, \
    make_lattice, mcnp_make_lattice_holder, make_mcnp_assembly_void
from FRIDGe.fridge.utilities.mcnp_surface_writer import mcnp_make_macro_RCC, mcnp_make_macro_RHP, mcnp_make_z_plane


def assembly_maker(assembly):
    """
        Creates an assembly given the assembly information and pin information.

    args:
        assembly(class): contains all the information regarding the fuel assembly and fuel pin type

    returns:
        void
    """
    # Unpack the information from the assembly_data DataFrame
    full_assembly_pitch = assembly.assembly_data.ix['assembly_pitch', 'assembly']
    duct_thickness = assembly.assembly_data.ix['duct_thickness', 'assembly']
    assembly_gap = assembly.assembly_data.ix['assembly_gap', 'assembly']
    inner_flat = assembly.assembly_data.ix['inside_flat_to_flat', 'assembly']
    assembly_height = assembly.assembly_data.ix['height', 'assembly']
    fuel_reflector_height = assembly.fuel_reflector_data.ix['height', 'fuel_reflector']
    plenum_height = assembly.plenum_data.ix['height', 'plenum']
    fuel_height = assembly.pin.pin_data.ix['height', 'fuel']

    # Set the geometry for this assembly
    inner_duct_position = [0, 0, fuel_reflector_height]
    outer_duct_position = [0, 0, -1]
    universe_position = [0, 0, -0.45]
    lower_fuel_reflector_position = [0, 0, 0]
    plenum_position = [0, 0, fuel_reflector_height + fuel_height]
    upper_fuel_reflector_position = [0, 0, fuel_reflector_height + fuel_height + plenum_height]
    assembly_height_vector = [0, 0, assembly_height + 2]
    assembly_universe_height_vector = [0, 0, assembly_height + 1.6]
    fuel_reflector_height_vector = [0, 0, fuel_reflector_height]
    plenum_height_vector = [0, 0, plenum_height]
    fuel_height_vector = [0, 0, fuel_height]
    inner_assembly_pitch = [0, inner_flat/2, 0]
    outer_assembly_pitch = [0, (inner_flat + (2 * duct_thickness + assembly_gap))/2, 0]
    gap_assembly_pitch = [0, (inner_flat + 2 * duct_thickness)/2, 0]

    # Create the material data
    assembly_data_maker(assembly)

    # Create the surfaces for the assembly
    assembly.lower_reflector_surface = assembly.surface_number
    assembly.lower_reflector_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, lower_fuel_reflector_position,
                                                                         fuel_reflector_height_vector,
                                                                         inner_assembly_pitch,
                                                                         'Assembly: Lower Reflector\n')
    assembly.plenum_surface = assembly.surface_number
    assembly.plenum_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, plenum_position,
                                                                plenum_height_vector,
                                                                inner_assembly_pitch, 'Assembly: Plenum\n')
    assembly.upper_reflector_surface = assembly.surface_number
    assembly.upper_reflector_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, upper_fuel_reflector_position,
                                                                         fuel_reflector_height_vector,
                                                                         inner_assembly_pitch,
                                                                         'Assembly: Upper Reflector\n')
    assembly.inner_duct_surface = assembly.surface_number
    assembly.inner_duct_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, inner_duct_position, fuel_height_vector,
                                                                    inner_assembly_pitch,
                                                                    'Assembly: Inner Duct (fuel portion)\n')
    assembly.outer_duct_surface = assembly.surface_number
    assembly.outer_duct_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, outer_duct_position,
                                                                    assembly_height_vector,
                                                                    outer_assembly_pitch,
                                                                    'Assembly: Outerduct/Universe\n')
    assembly.universe_surface = assembly.surface_number
    assembly.universe_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, universe_position,
                                                                  assembly_universe_height_vector,
                                                                  gap_assembly_pitch,
                                                                  'Assembly: Sodium universe\n')
    assembly.universe_mcnp_surface = '*' + assembly.universe_mcnp_surface

    # Create the fuel pin to be used for this assembly.
    fuel_pin_maker(assembly)

    # Create cells for assembly
    assembly.lower_reflector_cell = assembly.cell_number
    assembly.lower_reflector_mcnp_cell, warning = mcnp_make_cell(assembly, assembly.material.fuel_reflector_num,
                                                                 assembly.material.fuel_reflector[1],
                                                                 assembly.lower_reflector_surface,
                                                                 assembly.assembly_universe, 1,
                                                                 "Assembly: Lower Reflector\n")
    assembly.plenum_cell = assembly.cell_number
    assembly.plenum_mcnp_cell, warning = mcnp_make_cell(assembly, assembly.material.plenum_num,
                                                        assembly.material.plenum[1],
                                                        assembly.plenum_surface,
                                                        assembly.assembly_universe, 1,
                                                        "Assembly: Fission Product Plenum\n")
    assembly.upper_reflector_cell = assembly.cell_number
    assembly.upper_reflector_mcnp_cell, warning = mcnp_make_cell(assembly, assembly.material.fuel_reflector_num,
                                                                 assembly.material.fuel_reflector[1],
                                                                 assembly.upper_reflector_surface,
                                                                 assembly.assembly_universe, 1,
                                                                 "Assembly: Upper Reflector\n")

    assembly.lower_plane_surface = assembly.surface_number
    assembly.lower_plane_surface_mcnp = mcnp_make_z_plane(assembly, -0.3)
    assembly.upper_plane_surface = assembly.surface_number
    assembly.upper_plane_surface_mcnp = mcnp_make_z_plane(assembly, assembly_height + 0.6)

    assembly.universe_counter += 1
    assembly.lattice_mcnp_cell = make_lattice(assembly)
    assembly.lattice_holder_mcnp_cell = mcnp_make_lattice_holder(assembly)
    assembly.void_mcnp_cell = make_mcnp_assembly_void(assembly)

    assembly.k_card = dm.make_mcnp_problem(assembly)

    return


def fuel_pin_maker(fuel_assembly):
    """
        Creates the MCNP surfaces and cells for a pin and assigns them to the
        pin class.

    args:
        fuel_assembly (class): contains all the information regarding the fuel assembly and fuel pin type
    returns:
        void
    """
    # Unpack the information from the pin_data DataFrame
    fuel_pin_or = fuel_assembly.pin.pin_data.ix['pin_diameter', 'fuel'] / 2
    fuel_pin_thickness = fuel_assembly.pin.pin_data.ix['clad_thickness', 'fuel']
    fuel_pin_ir = fuel_pin_or - fuel_pin_thickness
    fuel_pellet_or = fuel_pin_ir * np.sqrt(fuel_assembly.pin.pin_data.ix['fuel_smear', 'fuel'])
    wire_wrap_radius = fuel_assembly.pin.pin_data.ix['wire_wrap_diameter', 'fuel'] / 2
    fuel_pin_height = fuel_assembly.pin.pin_data.ix['height', 'fuel']
    fuel_pin_pitch = fuel_assembly.pin.pin_data.ix['pitch', 'fuel']
    pin_pos = [0, 0, 50]
    fuel_assembly.universe_counter += 1
    fuel_assembly.pin.fuel_pin_universe = fuel_assembly.universe_counter

    # Create the surface for each section of a pin.
    fuel_assembly.pin.fuel_pellet_surface = fuel_assembly.surface_number
    fuel_assembly.pin.fuel_pellet_mcnp_surface, warning = mcnp_make_macro_RCC(fuel_assembly, pin_pos,
                                                                              [0, 0, fuel_pin_height], fuel_pellet_or,
                                                                              "Pin: Fuel pellet outer radius\n")

    fuel_assembly.pin.fuel_bond_surface = fuel_assembly.surface_number
    fuel_assembly.pin.fuel_bond_mcnp_surface, warning = mcnp_make_macro_RCC(fuel_assembly, pin_pos,
                                                                            [0, 0, fuel_pin_height], fuel_pin_ir,
                                                                            "Pin: Na bond outer radius\n")

    fuel_assembly.pin.fuel_clad_surface = fuel_assembly.surface_number
    fuel_assembly.pin.fuel_clad_mcnp_surface, warning = mcnp_make_macro_RCC(fuel_assembly, pin_pos,
                                                                            [0, 0, fuel_pin_height], fuel_pin_or,
                                                                            "Pin: Cladding outer radius\n")

    fuel_assembly.pin.fuel_pin_universe_surface = fuel_assembly.surface_number
    fuel_assembly.pin.fuel_pin_universe_mcnp_surface, warning = mcnp_make_macro_RHP(fuel_assembly, pin_pos,
                                                                                    [0, 0, fuel_pin_height],
                                                                                    [fuel_pin_pitch, 0, 0],
                                                                                    "$ Pin: Na universe for fuel pin\n")

    fuel_assembly.pin.na_cell_surface = fuel_assembly.surface_number
    fuel_assembly.pin.na_cell_mcnp_surface, warning = mcnp_make_macro_RHP(fuel_assembly, pin_pos,
                                                                          [0, 0, fuel_pin_height],
                                                                          [fuel_pin_pitch * 2, 0, 0],
                                                                          "$ Pin: Blank sodium pin for lattice\n")

    # Create the cell for each section of a pin
    fuel_assembly.pin.fuel_pellet_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_pellet_mcnp_cell, warning = mcnp_make_cell(fuel_assembly, fuel_assembly.material.fuel_num,
                                                                      fuel_assembly.pin.fuel_material[1],
                                                                      fuel_assembly.pin.fuel_pellet_surface,
                                                                      fuel_assembly.universe_counter, 1,
                                                                      "Pin: Fuel Pellet\n")

    fuel_assembly.pin.fuel_bond_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_bond_mcnp_cell, warning = mcnp_make_concentric_cell(fuel_assembly,
                                                                               fuel_assembly.material.bond_num,
                                                                               fuel_assembly.pin.fuel_bond[1],
                                                                               fuel_assembly.pin.fuel_pellet_surface,
                                                                               fuel_assembly.pin.fuel_bond_surface,
                                                                               fuel_assembly.universe_counter, 1,
                                                                               "Pin: Na Bond\n")

    fuel_assembly.pin.fuel_clad_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_clad_mcnp_cell, warning = mcnp_make_concentric_cell(fuel_assembly, fuel_assembly.material.clad_num,
                                                                               fuel_assembly.pin.fuel_clad[1],
                                                                               fuel_assembly.pin.fuel_bond_surface,
                                                                               fuel_assembly.pin.fuel_clad_surface,
                                                                               fuel_assembly.universe_counter, 1,
                                                                          "Pin: Pin Cladding\n")

    fuel_assembly.pin.fuel_universe_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_universe_mcnp_cell, warning = mcnp_make_cell_outside(fuel_assembly, fuel_assembly.material.coolant_num,
                                                                                0.94,
                                                                                fuel_assembly.pin.fuel_clad_surface,
                                                                                fuel_assembly.universe_counter, 1,
                                                                              "Pin: Wirewrap + Na coolant\n")

    fuel_assembly.universe_counter += 1
    fuel_assembly.pin.na_cell_universe = fuel_assembly.universe_counter
    fuel_assembly.pin.na_cell = fuel_assembly.cell_number
    fuel_assembly.pin.na_mcnp_cell, warning = mcnp_make_cell(fuel_assembly, fuel_assembly.material.coolant_num, 0.94,
                                                             fuel_assembly.pin.na_cell_surface,
                                                             fuel_assembly.universe_counter, 1,
                                                             "Pin: Na Pin\n")
    return


def assembly_data_maker(assembly):
    assembly.material.fuel = mat_read.material_reader([assembly.pin.pin_data.ix['fuel', 'fuel']])
    assembly.material.bond = mat_read.material_reader([assembly.pin.pin_data.ix['bond', 'fuel']])
    assembly.material.clad = mat_read.material_reader([assembly.pin.pin_data.ix['clad', 'fuel']])
    assembly.material.fuel_reflector = mat_smear.material_smear(assembly.fuel_reflector_smear_per, assembly.fuel_reflector_smear_zaids)
    assembly.material.plenum = mat_smear.material_smear(assembly.plenum_smear_per, assembly.plenum_smear_zaids)
    assembly.material.assembly = mat_read.material_reader([assembly.assembly_data.ix['assembly', 'assembly']])
    assembly.material.assembly_coolant = mat_read.material_reader([assembly.assembly_data.ix['coolant', 'assembly']])

    assembly.material.fuel_num = assembly.material_number
    assembly.material.fuel_mcnp_data = make_mcnp_material_data(
        assembly, assembly.pin.pin_data.ix['fuel', 'fuel'], assembly.material.fuel[0],
        assembly.material.fuel[1], assembly.material.fuel_xc_set)

    assembly.material.bond_num = assembly.material_number
    assembly.material.coolant_num = assembly.material_number
    assembly.material.bond_mcnp_data = make_mcnp_material_data(
        assembly, assembly.pin.pin_data.ix['bond', 'fuel'], assembly.material.bond[0],
        assembly.material.bond[1], assembly.material.bond_xc_set)

    assembly.material.clad_num = assembly.material_number
    assembly.material.assembly_num = assembly.material_number
    assembly.material.clad_mcnp_data = make_mcnp_material_data(
        assembly, assembly.pin.pin_data.ix['clad', 'fuel'], assembly.material.clad[0],
        assembly.material.clad[1], assembly.material.clad_xc_set)

    assembly.material.fuel_reflector_num = assembly.material_number
    assembly.material.fuel_reflector_mcnp_data = make_mcnp_material_data(
        assembly, 'Fuel Reflector Smear', assembly.material.fuel_reflector[0],
        assembly.material.fuel_reflector[1], assembly.material.fuel_reflector_xc_set)

    assembly.material.plenum_num = assembly.material_number
    assembly.material.plenum_mcnp_data = make_mcnp_material_data(
        assembly, 'Plenum Smear', assembly.material.plenum[0],
        assembly.material.plenum[1], assembly.material.plenum_xc_set)

    return


def make_mcnp_material_data(assembly, material_name, material_zaids, material_density, material_xc_set):
    material_header = 'c  Material: ' + str(material_name) + '  ; Density: ' + str(material_density) + '  a/(bn*cm)\n'
    material_data = 'm' + str(assembly.material_number) + '\n' + '     '
    for iter, material in enumerate(material_zaids):
        if (iter + 1) == len(material_zaids):
            material_data += str(int(material[1])) + material_xc_set + ' -' + '{:0.6e}'.format(material[3]) + '\n'
        elif (iter + 1) % 3 == 0:
            material_data += str(int(material[1])) + material_xc_set + ' -' + '{:0.6e}'.format(material[3]) + '\n' + '     '

        else:
            material_data += str(int(material[1])) + material_xc_set + ' -' + '{:0.6e}'.format(material[3]) + ' '
    assembly.material_number += 1
    mcnp_output = material_header + material_data
    return mcnp_output