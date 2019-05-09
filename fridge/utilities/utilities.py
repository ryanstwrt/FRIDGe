import math
import yaml


def get_hexagonal_prism_volume(pitch, height):
    """Returns the volume of a hexagonal prism."""
    half_pitch = pitch / 2
    area = math.sqrt(3) * 2 * pow(half_pitch, 2)
    volume = area * height
    return volume


def get_cylinder_volume(radius, height):
    """Returns the volume of a right circular cylinder"""
    volume = math.pi * pow(radius, 2) * height
    return volume


def get_toroidal_volume(inner_radius, toroid_radius, axial_pitch, height):
    """Returns the volume of a toroidal spring"""
    number_of_wraps = height / axial_pitch
    mean_radius = inner_radius + toroid_radius
    volume = (math.pi * pow(toroid_radius, 2)) * (2 * math.pi * number_of_wraps * mean_radius)
    return volume


def get_position_for_hex_lattice(position, pitch, z_position):
    """Get the centroid position of an assembly."""
    ring = int(position[:2]) - 1
    hextant = position[2]
    assembly_num = int(position[3:]) - 1
    sqrt_pitch = math.sqrt(pow(pitch, 2) - (pow(pitch/2, 2)))
    x = 0
    y = 0

    if hextant == 'A':
        if ring == 0:
            x = 0.0
        else:
            x = sqrt_pitch * (-ring + assembly_num)
        y = 1/2 * pitch * (ring + assembly_num)
    elif hextant == 'B':
        x = sqrt_pitch * assembly_num
        y = pitch * (ring - 1/2 * assembly_num)
    elif hextant == 'C':
        x = ring * sqrt_pitch
        y = pitch * (1/2 * ring - assembly_num)
    elif hextant == 'D':
        x = sqrt_pitch * (ring - assembly_num)
        y = -1/2 * pitch * (ring + assembly_num)
    elif hextant == 'E':
        x = -sqrt_pitch * assembly_num
        y = -pitch * (ring - 1/2 * assembly_num)
    elif hextant == 'F':
        x = -ring * sqrt_pitch
        y = pitch * (-1/2 * ring + assembly_num)
    return [round(x, 5), round(y, 5), z_position]


def yaml_reader(yaml_file_destination, known_directory, file_name):
    """Reads in the yaml file and returns the variables."""
    try:
        with open(yaml_file_destination[0], "r") as file:
            inputs = yaml.safe_load(file)
    except IndexError:
        raise IndexError("{} was not found in {}. Please ensure the file exists and then try again."
                         .format(file_name, known_directory))
    return inputs
