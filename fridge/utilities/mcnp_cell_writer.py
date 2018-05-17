import numpy as np


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
                if y > (2 * number_rings - (x - number_rings +1)) or y == 0:
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

    mcnp_output = str(assembly.cell_number) + " 0      -" + str(assembly.pin.fuel_pin_universe_surface) + \
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
    mcnp_block2 = str(assembly.cell_number) + " " + str(assembly.material.assembly_num) + " " \
                  + str(round(assembly.assembly_material[1], 7)) + "   -" + str(assembly.outer_duct_surface) \
                  + " " + str(assembly.lower_reflector_surface) + " " + str(assembly.plenum_surface) \
                  +  " " + str(assembly.upper_reflector_surface)+ " " + str(assembly.inner_duct_surface) + " u=" + str(assembly.assembly_universe) \
                  + "   imp:n=1   $ Driver: Hex Duct"

    assembly.cell_number += 1
    mcnp_block3 = str(assembly.cell_number) + " 0   -" + str(assembly.universe_surface) + " " \
                  + str(assembly.lower_plane_surface) + " -" + str(assembly.upper_plane_surface) + "   fill=" \
                  + str(assembly.assembly_universe) + "   imp:n=1   $ Assembly: Full Assembly"
    mcnp_block = mcnp_block1 + '\n' + mcnp_block2 + '\n' + mcnp_block3 + '\n'
    assembly.lattice_holder_cell = assembly.cell_number
    assembly.cell_number += 1

    return mcnp_block


def make_mcnp_assembly_void(assembly):
    mcnp_output = str(assembly.cell_number) + " 0    #" + str(assembly.lattice_holder_cell) + \
                  "   imp:n=0   $ Void\n"
    return mcnp_output