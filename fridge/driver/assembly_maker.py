import numpy as np

def assembly_maker(assembly):
    """
        Creates an assembly given the assembly information and pin information.

    args:
        assembly(class): contains all the information regarding the fuel assembly and fuel pin type

    returns:
        void
    """
    # Unpack the information from the assembly_data DataFrame
    number_pins = assembly.assembly_data.ix['pins_per_assembly', 'assembly']
    full_assembly_pitch = assembly.assembly_data.ix['assembly_pitch', 'assembly']
    duct_thickness = assembly.assembly_data.ix['duct_thickness', 'assembly']
    assembly_gap = assembly.assembly_data.ix['assembly_gap', 'assembly']
    inner_flat = assembly.assembly_data.ix['inside_flat_to_flat', 'assembly']
    assembly_height = assembly.assembly_data.ix['height', 'assembly']
    fuel_reflector_height = assembly.fuel_reflector_data.ix['height', 'fuel_reflector']
    plenum_height = assembly.plenum_data.ix['height', 'plenum']
    fuel_height = assembly.pin.pin_data.ix['height', 'fuel']
    inner_duct_position = [0, 0, fuel_reflector_height]
    outer_duct_position = [0, 0, -1]
    universe_position = [0, 0, -0.45]
    lower_fuel_reflector_position = [0, 0, 0]
    plenum_position = [0, 0, fuel_reflector_height + fuel_height]
    upper_fuel_reflector_position = [0, 0, fuel_reflector_height + fuel_height + plenum_height]
    assembly_height_vector = [0, 0, assembly_height+2]
    assembly_universe_height_vector = [0, 0, assembly_height + 0.6]
    fuel_reflector_height_vector = [0, 0, fuel_reflector_height]
    plenum_height_vector = [0, 0, plenum_height]
    fuel_height_vector = [0, 0, fuel_height]
    assembly_pitch = [0, inner_flat/2, 0]

    #Create the surfaces for the assembly
    assembly.lower_reflector_surface = assembly.surface_number
    assembly.lower_reflector_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, lower_fuel_reflector_position, fuel_reflector_height_vector,
                                                                         assembly_pitch, 'Assembly: Lower Reflector')
    assembly.plenum_surface = assembly.surface_number
    assembly.plenum_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, plenum_position,
                                                                         plenum_height_vector,
                                                                         assembly_pitch, 'Assembly: Plenum')
    assembly.upper_reflector_surface = assembly.surface_number
    assembly.upper_reflector_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, upper_fuel_reflector_position, fuel_reflector_height_vector,
                                                                         assembly_pitch, 'Assembly: Upper Reflector')
    assembly.inner_duct_surface = assembly.surface_number
    assembly.inner_duct_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, inner_duct_position, fuel_height_vector,
                                                                    assembly_pitch, 'Assembly: Inner Duct (fuel portion)')
    assembly.outer_duct_surface = assembly.surface_number
    assembly.outer_duct_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, outer_duct_position, assembly_height_vector,
                                                                         assembly_pitch, 'Assembly: Outerduct/Universe')
    assembly.universe_surface = assembly.surface_number
    assembly.universe_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, universe_position, assembly_universe_height_vector,
                                                                         assembly_pitch, 'Assembly: Sodium universe')
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
    pin_pos = [0, 0, 50]

    # Create the surface for each section of a pin.
    fuel_assembly.pin.fuel_pellet_surface = fuel_assembly.surface_number
    fuel_assembly.pin.fuel_pellet_mcnp_surface, warning = mcnp_make_macro_RCC(fuel_assembly, pin_pos,
                                                                              [0, 0, fuel_pin_height], fuel_pellet_or,
                                                                              "Pin: Fuel pellet outer radius")

    fuel_assembly.pin.fuel_bond_surface = fuel_assembly.surface_number
    fuel_assembly.pin.fuel_bond_mcnp_surface, warning = mcnp_make_macro_RCC(fuel_assembly, pin_pos,
                                                                            [0, 0, fuel_pin_height], fuel_pin_ir,
                                                                            "Pin: Na bond outer radius")

    fuel_assembly.pin.fuel_clad_surface = fuel_assembly.surface_number
    fuel_assembly.pin.fuel_clad_mcnp_surface, warning = mcnp_make_macro_RCC(fuel_assembly, pin_pos,
                                                                            [0, 0, fuel_pin_height], fuel_pin_or,
                                                                            "Pin: Cladding outer radius")

    fuel_assembly.pin.fuel_pin_universe_surface = fuel_assembly.surface_number
    fuel_assembly.pin.fuel_pin_universe_mcnp_surface, warning = mcnp_make_macro_RHP(fuel_assembly, pin_pos,
                                                                                    [0, 0, fuel_pin_height], [1.0, 0, 0],
                                                                                    "$ Pin: Na universe for fuel pin")

    # Create the cell for each section of a pin
    fuel_assembly.pin.fuel_pellet_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_pellet_mcnp_cell, warning = mcnp_make_cell(fuel_assembly, fuel_assembly.fuel_id, fuel_assembly.pin.fuel_material[1],
                                                                 fuel_assembly.pin.fuel_pellet_surface, 1, 1,
                                                                 "Pin: Fuel Pellet")

    fuel_assembly.pin.fuel_bond_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_bond_mcnp_cell, warning = mcnp_make_concentric_cell(fuel_assembly, fuel_assembly.bond_id, fuel_assembly.pin.fuel_bond[1],
                                                                          fuel_assembly.pin.fuel_pellet_surface,
                                                                          fuel_assembly.pin.fuel_bond_surface, 1, 1,
                                                                          "Pin: Na Bond")

    fuel_assembly.pin.fuel_clad_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_clad_mcnp_cell, warning = mcnp_make_concentric_cell(fuel_assembly, fuel_assembly.pin.fuel_clad[1], 0.94,
                                                                          fuel_assembly.pin.fuel_bond_surface,
                                                                          fuel_assembly.pin.fuel_clad_surface, 1, 1,
                                                                          "Pin: Pin Cladding")

    fuel_assembly.pin.fuel_universe_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_universe_mcnp_cell, warning = mcnp_make_concentric_cell(fuel_assembly, fuel_assembly.coolant_id, 0.94,
                                                                              fuel_assembly.pin.fuel_clad_surface,
                                                                              fuel_assembly.pin.fuel_pin_universe_surface, 1, 1,
                                                                              "Pin: Wirewrap + Na coolant")
    return


def mcnp_make_macro_RCC(fuel_assembly, position, height, radius, comment):
    """
        Creates a right circular cylinder for an MCNP input file.

        args:
            fuel_assembly(class): holds information on the surface number to be used
            position (float array): contains the x,y,z coordinates for the bottom and center of the cylinder
            height (float array): contains the vector in x,y,z for which to extend the cylinder
            radius (float): the radius of the cylinder
            comment (str): an accomanpying string to describe the cylinder
        return:
            mcnp_output (str): string containing the input line for MCNP
            mcnp_length_warning (bool): warns if the mcnp line is longer than
            """
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.surface_number) + " RCC  " + str(position[0]) + " " + str(position[1]) + " " + str(position[2]) \
        + "   " + str(height[0]) + " " + str(height[1]) + "   " + str(height[2]) + "   " + str(np.round(radius, 6)) \
        + "   $" + comment
    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Surface %d has a line that is longer than 80 characters")
    fuel_assembly.surface_number += 1
    return mcnp_output, mcnp_length_warning


def mcnp_make_macro_RHP(fuel_assembly, position, height, pitch, comment):
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.surface_number) + " RHP  " + str(position[0]) + " " + str(position[1]) + " " + str(position[2]) \
        + "   " + str(height[0]) + " " + str(height[1]) + " " + str(height[2]) + "   " + str(np.round(pitch[0], 6)) \
        + " " + str(np.round(pitch[1], 6)) + " " + str(np.round(pitch[2], 6)) + "   $" + comment
    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Surface %d has a line that is longer than 80 characters")
    fuel_assembly.surface_number += 1
    return mcnp_output, mcnp_length_warning


def mcnp_make_concentric_cell(fuel_assembly, material_id, material_density, inner, outer, universe, importance, comment):
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.cell_number) + " " + str(material_id) + " " + str(material_density) + " " + str(inner) + " -" \
    + str(outer) + "      u=" + str(universe) + " imp:n=" + str(importance) + " $" + comment

    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters", fuel_assembly.cell_number)
    fuel_assembly.cell_number += 1
    return mcnp_output, mcnp_length_warning


def mcnp_make_cell(fuel_assembly, material_id, material_density, inner, universe, importance, comment):
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.cell_number) + " " + str(material_id) + " " + str(material_density) + " -" + str(inner) +\
        "      u=" + str(universe) + " imp:n=" + str(importance) + " $" + comment

    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters", fuel_assembly.cell_number)
    fuel_assembly.cell_number += 1
    return mcnp_output, mcnp_length_warning