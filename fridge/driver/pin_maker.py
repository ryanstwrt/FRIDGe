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

    surface_number = 10

    fuel_assembly.pin.fuel_pellet_surface, warning = mcnp_make_macro_RCC(10, pin_pos, [0, 0, fuel_pin_height], fuel_pellet_or, "Pin: Fuel pellet outer radius")
    fuel_assembly.pin.fuel_bond_surface, warning = mcnp_make_macro_RCC(11, pin_pos, [0, 0, fuel_pin_height], fuel_pin_ir, "Pin: Na bond outer radius")
    fuel_assembly.pin.fuel_clad_surface, warning = mcnp_make_macro_RCC(12, pin_pos, [0, 0, fuel_pin_height], fuel_pin_or, "Pin: Cladding outer radius")
    fuel_assembly.pin.fuel_pin_universe_surface, warning = mcnp_make_macro_RHP(13, pin_pos, [0, 0, fuel_pin_height], [1.0, 0, 0], "$ Pin: Na universe for fuel pin")

    fuel_assembly.pin.fuel_bond_cell, warning = mcnp_make_concentric_cell(10, 100, 0.94, surface_number, surface_number+1, 1, 1, "Pin: Na Bond")

    return


def mcnp_make_macro_RCC(surface_number, position, height, radius, comment):
    mcnp_length_warning = False
    mcnp_output = str(surface_number) + " RCC  " + str(position[0]) + " " + str(position[1]) + " " + str(position[2]) \
        + "   " + str(height[0]) + " " + str(height[1]) + "   " + str(height[2]) + "   " + str(np.round(radius, 6)) \
        + "   $" + comment
    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Surface %d has a line that is longer than 80 characters")
    return mcnp_output, mcnp_length_warning


def mcnp_make_macro_RHP(surface_number, position, height, pitch, comment):
    mcnp_length_warning = False
    mcnp_output = str(surface_number) + " RHP  " + str(position[0]) + " " + str(position[1]) + " " + str(position[2]) \
        + "   " + str(height[0]) + " " + str(height[1]) + "   " + str(height[2]) + "   " + str(np.round(pitch[0], 6)) \
        + str(np.round(pitch[1], 6)) + " " + str(np.round(pitch[2], 6)) + "   $" + comment
    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Surface %d has a line that is longer than 80 characters")
    return mcnp_output, mcnp_length_warning

def mcnp_make_concentric_cell(cell_number, material_id, material_density, inner, outer, universe, importance, comment):
    mcnp_length_warning = False
    mcnp_output = str(cell_number) + " " + str(material_id) + " " + str(material_density) + " " + str(inner) + " -" \
    + str(outer) + "      u=" + str(universe) + " imp:n=" + str(importance) + " $" + comment

    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters")
    return mcnp_output, mcnp_length_warning

def mcnp_make_cell(cell_number, material_id, material_density, inner, universe, importance, comment):
    mcnp_length_warning = False
    mcnp_output = str(cell_number) + " " + str(material_id) + " " + str(material_density) + " " + str(inner) +\
    "      u=" + str(universe) + " imp:n=" + str(importance) + " $" + comment

    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Cell %d has a line that is longer than 80 characters")
    return mcnp_output, mcnp_length_warning