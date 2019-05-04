from decimal import Decimal
import os
cur_dir = os.path.dirname(__file__)
mcnp_dir = os.path.join(cur_dir, "../mcnp_input_files/")


def build_right_circular_cylinder_surface(radius, height, position, surface_num, comment):
    """Create a right circular cylinder in the z direction."""
    surface_card = "{} RCC {} {} {} 0 0 {} {} {}".format(surface_num, position[0], position[1], round(position[2], 5),
                                                         round(height, 5), round(radius, 5), comment)
    assert (len(surface_card) - len(comment)) < 80
    return surface_card


def build_right_hexagonal_prism_surface(pitch, height, position, surface_num, comment):
    """Create a right hexagonal prism in the z direction."""
    surface_card = "{} RHP {} {} {} 0 0 {} {} 0 0 {}".format(surface_num, position[0], position[1],
                                                             round(position[2], 5),
                                                             round(height, 5), round(pitch, 5), comment)
    assert (len(surface_card) - len(comment)) < 80
    return surface_card


def build_rotated_right_hexagonal_prism_surface(pitch, height, position, surface_num, comment):
    """Create a right hexagonal prism in the z direction, rotated 30 degrees."""
    surface_card = "{} RHP {} {} {} 0 0 {} 0 {} 0 {}".format(surface_num, position[0], position[1],
                                                             round(position[2], 5),
                                                             round(height, 5), round(pitch, 5), comment)
    assert (len(surface_card) - len(comment)) < 80
    return surface_card


def build_single_cell(cell_num, mat_num, density, surface_num, universe, comment):
    """Create a cell with one component"""
    universe_card = ''
    if type(universe) is int:
        universe_card = 'u=' + str(universe)
    cell_card = "{} {} {} -{} {} imp:n=1 {}".format(cell_num, mat_num, round(density, 5), surface_num, universe_card,
                                                    comment)
    assert (len(cell_card) - len(comment)) < 80
    return cell_card


def build_concentric_cell(cell_num, mat_num, density, inner_surface, outer_surface, universe, comment):
    """Create a cell which has multiple components inside a cell."""
    universe_card = ''
    if type(universe) is int:
        universe_card = 'u=' + str(universe)
    list_type = []
    if type(inner_surface) == type(list_type):
        new_inner_surface = ''
        i = 1
        for surface in inner_surface:
            if i % 5 == 0:
                new_inner_surface += ' {}\n     '.format(surface)
            else:
                new_inner_surface += ' {}'.format(surface)
            i += 1
        inner_surface = new_inner_surface

    cell_card = "{} {} {} {} -{} {} imp:n=1 {}".format(cell_num, mat_num, round(density, 5), inner_surface,
                                                       outer_surface, universe_card, comment)
    return cell_card


def build_outside_cell(cell_num, mat_num, density, surface_num, universe, comment):
    """Create a cell which encompasses everything outside it."""
    cell_card = "{} {} {} {} u={} imp:n=1 {}".format(cell_num, mat_num, round(density, 5), surface_num, universe,
                                                     comment)
    assert (len(cell_card) - len(comment)) < 80
    return cell_card


def build_fuel_lattice_cell(cell_num, surface_num, assembly_universe, lattice_universe, comment):
    """Create a hexagonal lattice cell."""
    cell_card = "{} 0 -{} u={} fill={} imp:n=1 {}".format(cell_num, surface_num, assembly_universe, lattice_universe,
                                                          comment)
    assert (len(cell_card) - len(comment)) < 80
    return cell_card


def build_assembly_universe_cell(cell_num, surface_num, universe, comment):
    """Create a cell which will encompass all aspects of an assembly."""
    cell_card = "{} 0 -{} fill={} imp:n=1 {}".format(cell_num, surface_num, universe, comment)
    assert (len(cell_card) - len(comment)) < 80
    return cell_card


def build_everything_else_cell(cell_num, surface_num, comment):
    """Create a cell which encompasses everything outside an assembly/core."""
    cell_card = "{} 0 {} imp:n=0 {}".format(cell_num, surface_num, comment)
    assert (len(cell_card) - len(comment)) < 80
    return cell_card


def build_material_card(material, xc, mat_num):
    """Create the MCNP material data card."""
    material_card = "\nc Material: {}; Density: {} atoms/bn*cm \nm{}".format(material.name,
                                                                             round(material.atomDensity, 5), mat_num)
    i = 0
    for isotope, atomDensity in material.atomPercent.items():
        if i == 3:
            material_card += "\n    "
            i = 0
        material_card += " {}{} {:.4E}".format(isotope, xc, Decimal(atomDensity))
        i += 1
    return material_card


def mcnp_input_deck_maker(assembly, k_card, global_vars):
    """Create the MCNP input deck based on the assembly/core data."""
    file = open(mcnp_dir + global_vars.output_name + ".i", "w")
    file.write("Input deck created by FRIDGe\n")
    file.write("c " + global_vars.assembly_file_name.center(77, "*") + "\n")
    assembly_cell_title = "Cell Cards for Assembly: {}".format(assembly.assemblyPosition)
    file.write("c " + assembly_cell_title.center(77, "*") + " \n")
    for cell in assembly.assemblyCellList:
        file.write(cell.cellCard + '\n')
    file.write("\n")

    assembly_surface_title = "Surface Cards for Fuel Assembly: {}".format(assembly.assemblyPosition)
    file.write("c " + assembly_surface_title.center(77, "*") + "\n")
    for surface in assembly.assemblySurfaceList:
        file.write(surface.surfaceCard + '\n')
    file.write("\n")

    assembly_data_title = "Data Cards"
    file.write("c " + assembly_data_title.center(77, "*") + "\n")
    assembly_kcode_title = "k-code Information"
    file.write("c " + assembly_kcode_title.center(77, "*") + "\n")
    file.write(k_card)
    file.write("c " + "Material Information".center(77, "*"))
    for material in assembly.assemblyMaterialList:
        file.write(material.materialCard)
    file.close()


def mcnp_input_deck_maker_core(core, k_card, global_vars):
    """Create the MCNP input deck based on the assembly/core data."""
    file = open(mcnp_dir + global_vars.output_name + ".i", "w")
    file.write("Input deck created by FRIDGe\n")
    file.write("c " + global_vars.assembly_file_name.center(77, "*") + "\n")
    for assembly in core.assemblyList:
        assembly_cell_title = "Cell Cards for Assembly: {}".format(assembly.assemblyPosition)
        file.write("c " + assembly_cell_title.center(77, "*") + " \n")
        for cell in assembly.assemblyCellList:
            file.write(cell.cellCard + '\n')
    for cell in core.coreCellList:
        file.write(cell.cellCard + '\n')
    file.write("\n")

    for assembly in core.assemblyList:
        assembly_surface_title = "Surface Cards for Fuel Assembly: {}".format(assembly.assemblyPosition)
        file.write("c " + assembly_surface_title.center(77, "*") + "\n")
        for surface in assembly.assemblySurfaceList:
            file.write(surface.surfaceCard + '\n')
    for surface in core.coreSurfaceList:
        file.write(surface.surfaceCard + '\n')
    file.write("\n")

    assembly_data_title = "Data Cards"
    file.write("c " + assembly_data_title.center(77, "*") + "\n")
    assembly_kcode_title = "k-code Information"
    file.write("c " + assembly_kcode_title.center(77, "*") + "\n")
    file.write(k_card)
    file.write("c " + "Material Information".center(77, "*"))
    for assembly in core.assemblyList:
        for material in assembly.assemblyMaterialList:
            file.write(material.materialCard)
    for material in core.coreMaterialList:
        file.write(material.materialCard)
    file.close()


def make_mcnp_problem(global_vars, core=None):
    """Create the MCNP specific kcode options."""
    kopts_output = ''
    if global_vars.kopts:
        kopts_output = 'kopts BLOCKSIZE=10 KINETICS=YES PRECURSOR=Yes \n'

    ksrc_output = 'ksrc '
    if core is not None:
        for assembly in core.assemblyList:
            if assembly.assemblyType == 'Fuel':
                fuel = assembly.fuel
                position = fuel.fuel_position
                position[2] += fuel.height/2
                position = map(str, position)
                position_string = ' '.join(position)
                ksrc_output += '     {}\n'.format(position_string)
    else:
        ksrc_output += '0 0 10\n'

    kcode_output = 'kcode ' + str(global_vars.number_particles_generation) + " 1.0 " + \
                   str(global_vars.number_skipped_generations) + " " + str(global_vars.number_generations) + '\n'
    prdmp_output = 'PRDMP 100 10 100 1 \n'
    dbcn_output = 'DBCN 68J 50000 \n'

    mcnp_output = kcode_output + ksrc_output + prdmp_output + kopts_output + dbcn_output
    return mcnp_output
