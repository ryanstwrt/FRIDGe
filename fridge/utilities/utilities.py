import math
import yaml


def getRHPVolume(pitch, height):
    """Returns the volume of a hexagonal prism."""
    halfPitch = pitch / 2
    area = math.sqrt(3) * 2 * pow(halfPitch, 2)
    volume = area * height
    return volume


def getRCCVolume(radius, height):
    """Returns the volume of a right circular cylinder"""
    volume = math.pi * pow(radius, 2) * height
    return volume


def getToroidalVolume(innerRadius, toroidRadius, axialPitch, height):
    """Returns the volume of a toroidal spring"""
    numberOfWraps = height / axialPitch
    meanRadius = innerRadius + toroidRadius
    volume = (math.pi*pow(toroidRadius, 2))*(2*math.pi*numberOfWraps*meanRadius)
    return volume


def getPosition(position, pitch, zPosition):
    """Get the centroid position of an assembly."""
    ring = int(position[:2]) - 1
    hextant = position[2]
    assemblyNum = int(position[3:]) - 1
    sqrtPitch = math.sqrt(pow(pitch, 2) - (pow(pitch/2, 2)))
    x = 0
    y = 0

    if hextant == 'A':
        if ring == 0:
            x = 0.0
        else:
            x = sqrtPitch * (-ring + assemblyNum)
        y = 1/2 * pitch * (ring + assemblyNum)
    elif hextant == 'B':
        x = sqrtPitch * assemblyNum
        y = pitch * (ring - 1/2 * assemblyNum)
    elif hextant == 'C':
        x = ring * sqrtPitch
        y = pitch * (1/2 * ring - assemblyNum)
    elif hextant == 'D':
        x = sqrtPitch * (ring - assemblyNum)
        y = -1/2 * pitch * (ring + assemblyNum)
    elif hextant == 'E':
        x = -sqrtPitch * assemblyNum
        y = -pitch * (ring - 1/2 * assemblyNum)
    elif hextant == 'F':
        x = -ring * sqrtPitch
        y = pitch * (-1/2 * ring + assemblyNum)
    return [x, y, zPosition]


def yaml_reader(yaml_file_destination, known_directory, file_name):
    """Reads in the yaml file and returns the variables."""
    try:
        with open(yaml_file_destination[0], "r") as file:
            inputs = yaml.safe_load(file)
    except IndexError:
        raise IndexError("{} was not found in {}. Please ensure the file exists and then try again."
                         .format(file_name, known_directory))
    return inputs
