import numpy as np


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
    mcnp_output = str(fuel_assembly.surface_number) + " RCC  " + str(position[0]) + " " + str(position[1]) \
                  + " " + str(position[2]) + "   " + str(height[0]) + " " + str(height[1]) + "   " + str(height[2]) \
                  + "   " + str(np.round(radius, 6)) \
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
    mcnp_output = str(fuel_assembly.surface_number) + " RHP  " + str(position[0]) + " " + str(position[1]) \
                  + " " + str(position[2]) + "   " + str(height[0]) + " " + str(height[1]) + " " + str(height[2]) \
                  + "   " + str(np.round(pitch[0], 7)) + " " + str(np.round(pitch[1], 7)) + " " \
                  + str(np.round(pitch[2], 7)) + "   $" + comment
    if len(mcnp_output) > 80:
        mcnp_length_warning = True
        print("\033[1;37:33mWarning: Surface %d has a line that is longer than 80 characters")
    fuel_assembly.surface_number += 1
    return mcnp_output, mcnp_length_warning


def mcnp_make_z_plane(assembly, z):
    mcnp_output = str(assembly.surface_number) + " PZ " + str(z) + "\n"
    assembly.surface_number += 1
    return mcnp_output