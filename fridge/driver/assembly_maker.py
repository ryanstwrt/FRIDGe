import numpy as np
import FRIDGe.fridge.input_readers.material_reader as mat_read


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
    inner_duct_position = [0, 0, fuel_reflector_height]
    outer_duct_position = [0, 0, -1]
    universe_position = [0, 0, -0.45]
    lower_fuel_reflector_position = [0, 0, 0]
    plenum_position = [0, 0, fuel_reflector_height + fuel_height]
    upper_fuel_reflector_position = [0, 0, fuel_reflector_height + fuel_height + plenum_height]
    assembly_height_vector = [0, 0, assembly_height+2]
    assembly_universe_height_vector = [0, 0, assembly_height + 1.6]
    fuel_reflector_height_vector = [0, 0, fuel_reflector_height]
    plenum_height_vector = [0, 0, plenum_height]
    fuel_height_vector = [0, 0, fuel_height]
    inner_assembly_pitch = [0, inner_flat/2, 0]
    outer_assembly_pitch = [0, (inner_flat + (2 * duct_thickness + assembly_gap))/2, 0]
    gap_assembly_pitch = [0, (inner_flat + 2 * duct_thickness )/2, 0]

    # Create the surfaces for the assembly
    assembly.lower_reflector_surface = assembly.surface_number
    assembly.lower_reflector_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, lower_fuel_reflector_position, fuel_reflector_height_vector,
                                                                         inner_assembly_pitch, 'Assembly: Lower Reflector\n')
    assembly.plenum_surface = assembly.surface_number
    assembly.plenum_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, plenum_position,
                                                                         plenum_height_vector,
                                                                         inner_assembly_pitch, 'Assembly: Plenum\n')
    assembly.upper_reflector_surface = assembly.surface_number
    assembly.upper_reflector_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, upper_fuel_reflector_position, fuel_reflector_height_vector,
                                                                         inner_assembly_pitch, 'Assembly: Upper Reflector\n')
    assembly.inner_duct_surface = assembly.surface_number
    assembly.inner_duct_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, inner_duct_position, fuel_height_vector,
                                                                    inner_assembly_pitch, 'Assembly: Inner Duct (fuel portion)\n')
    assembly.outer_duct_surface = assembly.surface_number
    assembly.outer_duct_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, outer_duct_position, assembly_height_vector,
                                                                         outer_assembly_pitch, 'Assembly: Outerduct/Universe\n')
    assembly.universe_surface = assembly.surface_number
    assembly.universe_mcnp_surface, warning = mcnp_make_macro_RHP(assembly, universe_position, assembly_universe_height_vector,
                                                                         gap_assembly_pitch, 'Assembly: Sodium universe\n')
    assembly.universe_mcnp_surface = '*' + assembly.universe_mcnp_surface

    # Create the fuel pin to be used for this assembly.
    fuel_pin_maker(assembly)

    # Create cells for assembly
    assembly.lower_reflector_cell = assembly.cell_number
    assembly.lower_reflector_mcnp_cell, warning = mcnp_make_cell(assembly, assembly.fuel_reflector_id,
                                                                 100000,
                                                                 assembly.lower_reflector_surface,
                                                                 assembly.assembly_universe, 1,
                                                                 "Assembly: Lower Reflector\n")
    assembly.plenum_cell = assembly.cell_number
    assembly.plenum_mcnp_cell, warning = mcnp_make_cell(assembly, assembly.plenum_id,
                                                                 100000,
                                                                 assembly.plenum_surface,
                                                                 assembly.assembly_universe, 1,
                                                                 "Assembly: Fission Product Plenum\n")
    assembly.upper_reflector_cell = assembly.cell_number
    assembly.upper_reflector_mcnp_cell, warning = mcnp_make_cell(assembly, assembly.fuel_reflector_id,
                                                                 100000,
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

    assembly_data_maker(assembly)
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
                                                                                    [0, 0, fuel_pin_height], [1.0, 0, 0],
                                                                                    "$ Pin: Na universe for fuel pin\n")

    # Create the cell for each section of a pin
    fuel_assembly.pin.fuel_pellet_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_pellet_mcnp_cell, warning = mcnp_make_cell(fuel_assembly, fuel_assembly.fuel_id, fuel_assembly.pin.fuel_material[1],
                                                                 fuel_assembly.pin.fuel_pellet_surface,
                                                                 fuel_assembly.universe_counter, 1,
                                                                 "Pin: Fuel Pellet\n")

    fuel_assembly.pin.fuel_bond_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_bond_mcnp_cell, warning = mcnp_make_concentric_cell(fuel_assembly, fuel_assembly.bond_id, fuel_assembly.pin.fuel_bond[1],
                                                                          fuel_assembly.pin.fuel_pellet_surface,
                                                                          fuel_assembly.pin.fuel_bond_surface,
                                                                          fuel_assembly.universe_counter, 1,
                                                                          "Pin: Na Bond\n")

    fuel_assembly.pin.fuel_clad_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_clad_mcnp_cell, warning = mcnp_make_concentric_cell(fuel_assembly, fuel_assembly.clad_id,
                                                                               fuel_assembly.pin.fuel_clad[1],
                                                                          fuel_assembly.pin.fuel_bond_surface,
                                                                          fuel_assembly.pin.fuel_clad_surface,
                                                                          fuel_assembly.universe_counter, 1,
                                                                          "Pin: Pin Cladding\n")

    fuel_assembly.pin.fuel_universe_cell = fuel_assembly.cell_number
    fuel_assembly.pin.fuel_universe_mcnp_cell, warning = mcnp_make_cell_outside(fuel_assembly, fuel_assembly.coolant_id,
                                                                                   0.94,
                                                                              fuel_assembly.pin.fuel_clad_surface,
                                                                              fuel_assembly.universe_counter, 1,
                                                                              "Pin: Wirewrap + Na coolant\n")

    fuel_assembly.universe_counter += 1
    fuel_assembly.pin.na_cell_universe = fuel_assembly.universe_counter
    fuel_assembly.pin.na_cell = fuel_assembly.cell_number
    fuel_assembly.pin.na_mcnp_cell, warning = mcnp_make_cell(fuel_assembly, fuel_assembly.coolant_id, 0.94,
                                                                              fuel_assembly.pin.fuel_pin_universe_surface,
                                                                              fuel_assembly.universe_counter, 1,
                                                                              "Pin: Na Pin\n")
    return


def assembly_data_maker(assembly):
    assembly.material.fuel = mat_read.material_reader([assembly.pin.pin_data.ix['fuel', 'fuel']])
    assembly.material.bond = mat_read.material_reader([assembly.pin.pin_data.ix['bond', 'fuel']])
    assembly.material.clad = mat_read.material_reader([assembly.pin.pin_data.ix['clad', 'fuel']])
    assembly.material.fuel_reflector = mat_read.material_reader([assembly.fuel_reflector_data.ix['clad', 'fuel_reflector']])
    assembly.material.plenum = mat_read.material_reader([assembly.plenum_data.ix['coolant', 'plenum']])
    assembly.material.assembly = mat_read.material_reader([assembly.assembly_data.ix['assembly', 'assembly']])
    assembly.material.assembly_coolant = mat_read.material_reader([assembly.assembly_data.ix['coolant', 'assembly']])

    assembly.material.fuel_num = assembly.material_number
    make_mcnp_material_data(assembly, assembly.pin.pin_data.ix['fuel', 'fuel'], assembly.material.fuel[0], assembly.material.fuel[1], '.82c', 1000)


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
    """
        Creates a right hexagonal prism for an MCNP input file.

        args:
            fuel_assembly(class): holds information on the surface number to be used
            position (float array): contains the x,y,z coordinates for the bottom and center of the RHP
            height (float array): contains the vector in x,y,z for which to extend the RHP
            radius (float): half_pitch of the RHP
            comment (str): an accomanpying string to describe the RHP
        return:
            mcnp_output (str): string containing the input line for MCNP
            mcnp_length_warning (bool): warns if the mcnp line is longer than
    """
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.surface_number) + " RHP  " + str(position[0]) + " " + str(position[1]) + " " + str(position[2]) \
        + "   " + str(height[0]) + " " + str(height[1]) + " " + str(height[2]) + "   " + str(np.round(pitch[0], 7)) \
        + " " + str(np.round(pitch[1], 7)) + " " + str(np.round(pitch[2], 7)) + "   $" + comment
    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Surface %d has a line that is longer than 80 characters")
    fuel_assembly.surface_number += 1
    return mcnp_output, mcnp_length_warning


def mcnp_make_concentric_cell(fuel_assembly, material_id, material_density, inner, outer, universe, importance, comment):
    """
        Combinatorial geometry to create a cell which is outside the inner surface and inside the outer surface.

        args:
            fuel_assembly(class): holds information on the surface number to be used
            material_id (int): ID number which tells what material to reference from in the data card
            material_density (float): atom density of the material being used
            inner (int): the surface number of the inner surface
            outer (int): the surface number of the outer surface
            universe (int): the universe number associate with this particular cell
            importance (int): particle importance
            comment (str): an accomanpying string to describe the RHP
        return:
            mcnp_output (str): string containing the input line for MCNP
            mcnp_length_warning (bool): warns if the mcnp line is longer than 80 characters
    """
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.cell_number) + " " + str(material_id) + " " + str(round(material_density, 7)) + "   " + str(inner) + " -" \
    + str(outer) + "      u=" + str(universe) + " imp:n=" + str(importance) + " $" + comment

    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters", fuel_assembly.cell_number)
    fuel_assembly.cell_number += 1
    return mcnp_output, mcnp_length_warning


def mcnp_make_cell(fuel_assembly, material_id, material_density, inner, universe, importance, comment):
    """
        Combinatorial geometry to create a cell on the inside of one surface

        args:
            fuel_assembly(class): holds information on the surface number to be used
            material_id (int): ID number which tells what material to reference from in the data card
            material_density (float): atom density of the material being used
            inner (int): the surface number of the inner surface
            universe (int): the universe number associate with this particular cell
            importance (int): particle importance
            comment (str): an accomanpying string to describe the RHP
        return:
            mcnp_output (str): string containing the input line for MCNP
            mcnp_length_warning (bool): warns if the mcnp line is longer than 80 characters
    """
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.cell_number) + " " + str(material_id) + " " + str(np.round(material_density, 7)) + "   -" + str(inner) +\
        "      u=" + str(universe) + " imp:n=" + str(importance) + " $" + comment

    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters", fuel_assembly.cell_number)
    fuel_assembly.cell_number += 1
    return mcnp_output, mcnp_length_warning

def mcnp_make_cell_outside(fuel_assembly, material_id, material_density, inner, universe, importance, comment):
    """
        Combinatorial geometry to create a cell on the outside of one surface

        args:
            fuel_assembly(class): holds information on the surface number to be used
            material_id (int): ID number which tells what material to reference from in the data card
            material_density (float): atom density of the material being used
            inner (int): the surface number of the inner surface
            universe (int): the universe number associate with this particular cell
            importance (int): particle importance
            comment (str): an accomanpying string to describe the RHP
        return:
            mcnp_output (str): string containing the input line for MCNP
            mcnp_length_warning (bool): warns if the mcnp line is longer than 80 characters
    """
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.cell_number) + " " + str(material_id) + " " + str(np.round(material_density, 7)) + "   " + str(inner) +\
        "      u=" + str(universe) + " imp:n=" + str(importance) + " $" + comment

    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters", fuel_assembly.cell_number)
    fuel_assembly.cell_number += 1
    return mcnp_output, mcnp_length_warning


def make_lattice(assembly):
    """
    Creates a pin lattice for the fuel based on the number of pins present in an assembly.

    params:
        assembly (class): holds information on the surface number to be used
    return:
        mcnp_output(str): the MCNP string to be used for the input file.
    """
    number_pins = assembly.assembly_data.ix['pins_per_assembly', 'assembly']
    assembly.lattice_universe = assembly.universe_counter
    number_rings = 0
    temp = 0
    while temp < number_pins:
        if number_rings == 0:
            temp += 1
            number_rings = 1
        else:
            temp += 6 * number_rings
            number_rings += 1

    lattice_array = np.zeros((number_rings * 2 + 1, number_rings * 2 + 1))
    for x in range(number_rings * 2 + 1):
        for y in range(number_rings * 2 + 1):
            if x == 0 or x == 2*number_rings:
                lattice_array[x][y] = assembly.pin.na_cell_universe
            elif x < 11:
                if y < (number_rings + 1 - x) or y == (2 * number_rings):
                    lattice_array[x][y] = assembly.pin.na_cell_universe
                else:
                    lattice_array[x][y] = assembly.pin.fuel_pin_universe
            else:
                if y > (2 * number_rings - (x - number_rings)) or y == 0:
                    lattice_array[x][y] = assembly.pin.na_cell_universe
                else:
                    lattice_array[x][y] = assembly.pin.fuel_pin_universe

    mcnp_lattice = ''
    lat_iter = 1
    total_lattice_elements = sum(len(x) for x in lattice_array)
    for row in lattice_array:
        for element in row:
            if (lat_iter) == total_lattice_elements:
                mcnp_lattice += ' ' + str(int(element)) + '\n'
            elif lat_iter %10 == 0:
                mcnp_lattice += ' ' + str(int(element)) + '\n' + '     '
            else:
                mcnp_lattice += ' ' + str(int(element))
            lat_iter += 1

    mcnp_output = str(assembly.cell_number) + " 0      -" + str(assembly.inner_duct_surface) + \
                    " lat=2 u=" + str(assembly.lattice_universe) + " imp:n=1 \n" + \
                    "      fill=-" + str(number_rings) + ":" + str(number_rings) + " -" + \
                    str(number_rings) + ":" + str(number_rings) + " 0:0 \n" + '     '+ mcnp_lattice

    assembly.cell_number += 1
    return mcnp_output


def mcnp_make_lattice_holder(assembly):
    mcnp_block1 = str(assembly.cell_number) + " 0 -" + str(assembly.inner_duct_surface) + "    u=" \
                  + str(assembly.assembly_universe) + " fill=" + str(assembly.lattice_universe) \
                  + " imp:n=1 $ Assembly: Base Assembly"

    assembly.cell_number += 1
    mcnp_block2 = str(assembly.cell_number) + " " + str(assembly.assembly_id) + " " \
                  + str(round(assembly.assembly_material[1], 7)) + "   -" + str(assembly.inner_duct_surface) \
                  + " " + str(assembly.lower_reflector_surface) + " " + str(assembly.upper_reflector_surface) \
                  + " " + str(assembly.plenum_surface) + "   u=" + str(assembly.assembly_universe) \
                  + "   imp:n=1   $ Driver: Hex Duct"

    assembly.cell_number += 1
    mcnp_block3 = str(assembly.cell_number) + " 0   -" + str(assembly.universe_surface) + " " \
                  + str(assembly.lower_plane_surface) + " -" + str(assembly.upper_plane_surface) + "   u=" \
                  + str(assembly.assembly_universe) + "   imp:n=1   $ Assembly: Full Assembly"
    mcnp_block = mcnp_block1 + '\n' + mcnp_block2 + '\n' + mcnp_block3 + '\n'
    assembly.lattice_holder_cell = assembly.cell_number
    assembly.cell_number += 1

    return mcnp_block


def mcnp_make_z_plane(assembly, z):
    mcnp_output = str(assembly.surface_number) + " PZ " + str(z) + "\n"
    assembly.surface_number += 1
    return mcnp_output


def make_mcnp_assembly_void(assembly):
    mcnp_output = str(assembly.cell_number) + " 0    #" + str(assembly.lattice_holder_cell) + \
                  "   imp:n=0   $ Void\n"
    return mcnp_output

def make_mcnp_material_data(assembly, material_name, material_zaids, material_density, material_xc_set, universe):
    print(material_zaids)
    material_header = 'c  Material: ' + str(material_name) + '  ; Density: ' + str(material_density) + '  a/(bn*cm)\n'
    material_data = 'm' + str(assembly.material_number) + '\n' + '     '
    for iter, material in enumerate(material_zaids):
        print(material[3])
        print(len(material_zaids))
        if (iter + 1) % 3 == 0:
            material_data += str(int(material[1])) + material_xc_set + ' -' + '{:0.6e}'.format(material[3]) + '\n' + '     '
        elif (iter + 1) == len(material_zaids):
            material_data += str(int(material[1])) + material_xc_set + ' -' + '{:0.6e}'.format(material[3]) + '\n'
        else:
            material_data += str(int(material[1])) + material_xc_set + ' -' + '{:0.6e}'.format(material[3]) + ' '
    assembly.material_number += 1
    print(material_header)
    print(material_data)