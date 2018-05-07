import pandas as pd
import numpy as np
from FRIDGe.fridge.driver import assembly_holder as ah


def fuel_pin_maker(fuel_assembly):
    """
        Creates the surface geometry for the fuel pins.

    args:
        fuel_assembly (class): contains all the information regarding the fuel assembly and fuel pin type
    """
    # Unpack the information from the pin_datat DataFrame
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
        + "   " + str(height[0]) + " " + str(height[1]) + "   " + str(height[2]) + "   " + str(np.round(pitch[0], 6)) \
        + str(np.round(pitch[1], 6)) + " " + str(np.round(pitch[2], 6)) + "   $" + comment
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
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters")
    fuel_assembly.cell_number += 1
    return mcnp_output, mcnp_length_warning

def mcnp_make_cell(fuel_assembly, material_id, material_density, inner, universe, importance, comment):
    mcnp_length_warning = False
    mcnp_output = str(fuel_assembly.cell_number) + " " + str(material_id) + " " + str(material_density) + " -" + str(inner) +\
    "      u=" + str(universe) + " imp:n=" + str(importance) + " $" + comment

    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters")
    fuel_assembly.cell_number += 1
    return mcnp_output, mcnp_length_warning