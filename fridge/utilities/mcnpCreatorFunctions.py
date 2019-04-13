import FRIDGe.fridge.utilities.materialReader as materialReader
from decimal import Decimal
import math
import os
cur_dir = os.path.dirname(__file__)
mcnp_dir = os.path.join(cur_dir, "../mcnp_input_files/")


def getRCC(radius, height, position, surfaceNum, comment):
    """Create a right circular cylinder in the z direction."""
    surfaceCard = "{} RCC {} {} {} 0 0 {} {} {}".format(surfaceNum, position[0], position[1], round(position[2], 5),
                                                        round(height, 5), round(radius, 5), comment)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getRHP(pitch, height, position, surfaceNum, comment):
    """Create a right hexagonal prism in the z direction."""
    surfaceCard = "{} RHP {} {} {} 0 0 {} {} 0 0 {}".format(surfaceNum, position[0], position[1], round(position[2], 5),
                                                            round(height, 5), round(pitch, 5), comment)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getRHPRotated(pitch, height, position, surfaceNum, comment):
    """Create a right hexagonal prism in the z direction, rotated 30 degrees."""
    surfaceCard = "{} RHP {} {} {} 0 0 {} 0 {} 0 {}".format(surfaceNum, position[0], position[1], round(position[2], 5),
                                                            round(height, 5), round(pitch, 5), comment)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getSingleCell(cellNum, matNum, density, surfaceNum, universe, comment):
    """Create a cell with one component"""
    cellCard = "{} {} {} -{} u={} imp:n=1 {}".format(cellNum, matNum, round(density, 5), surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getConcentricCell(cellNum, matNum, density, innerSurface, outerSurface, universe, comment):
    """Create a cell which has multiple components inside a cell."""
    listType = []
    if type(innerSurface) == type(listType):
        newInnerSurface = ''
        for i in innerSurface:
            newInnerSurface += ' {}'.format(i)
        innerSurface = newInnerSurface

    cellCard = "{} {} {} {} -{} u={} imp:n=1 {}".format(cellNum, matNum, round(density, 5), innerSurface, outerSurface,
                                                        universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getOutsideCell(cellNum, matNum, density, surfaceNum, universe, comment):
    """Create a cell which encompasses everything outside it."""
    cellCard = "{} {} {} {} u={} imp:n=1 {}".format(cellNum, matNum, round(density, 5), surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getFuelLatticeCell(cellNum, surfaceNum, assemblyUniverse, latticeUniverse, comment):
    """Create a hexagonal lattice cell."""
    cellCard = "{} 0 -{} u={} fill={} imp:n=1 {}".format(cellNum, surfaceNum, assemblyUniverse, latticeUniverse,
                                                         comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getAssemblyUniverseCell(cellNum, surfaceNum, universe, comment):
    """Create a cell which will encompass all aspects of an assembly."""
    cellCard = "{} 0 -{} fill={} imp:n=1 {}".format(cellNum, surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getEverythingElseCard(cellNum, surfaceNum, comment):
    """Create a cell which encompasses everything outside an assembly/core."""
    cellCard = "{} 0 {} imp:n=0 {}".format(cellNum, surfaceNum, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getMaterialCard(material, xc, matNum):
    """Create the MCNP material data card."""
    materialCard = "\nc Material: {}; Density: {} atoms/bn*cm \nm{}".format(material.name,
                                                                            round(material.atomDensity, 5), matNum)
    i = 0
    for isotope, atomDensity in material.atomPercent.items():
        if i == 3:
            materialCard += "\n    "
            i = 0
        materialCard += " {}.{} {:.4E}".format(isotope, xc, Decimal(atomDensity))
        i += 1
    return materialCard


def getSmearedMaterial(materials):
    """Create the material data card for a smeared material."""
    smearMaterial = {}
    avogadros = materialReader.AVOGADROS_NUMBER
    for material, materialWeightPercent in materials.items():
        if material == 'Void':
            pass
        else:
            materialClass = materialReader.Material()
            materialClass.setMaterial(material)
            for isotope, isotopeWeightPercent in materialClass.weightPercent.items():
                element = str(isotope)
                if len(element) < 5:
                    currentElement = element[:1] + '000'
                else:
                    currentElement = element[:2] + '000'
                currentElement = int(currentElement)
                try:
                    smearMaterial[isotope] += isotopeWeightPercent * materialWeightPercent * materialClass.density \
                                              * avogadros / \
                                              materialClass.elementDict[currentElement].molecularMassDict[isotope]
                except KeyError:
                    smearMaterial[isotope] = isotopeWeightPercent * materialWeightPercent * materialClass.density \
                                             * avogadros / \
                                             materialClass.elementDict[currentElement].molecularMassDict[isotope]
    newMaterial = materialReader.Material()
    newMaterial.name = "{}".format([val for val in materials])
    newMaterial.atomPercent = smearMaterial
    newMaterial.atomDensity = sum(smearMaterial.values())
    return newMaterial


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


def mcnp_input_deck_maker(assembly, k_card, global_vars):
    """Create the MCNP input deck based on the assembly/core data."""
    file = open(mcnp_dir + global_vars.output_name + ".i", "w")
    file.write("Input deck created by FRIDGe\n")
    file.write("c " + "Title".center(77, "*") + "\n")
    assembly_cell_title = "Cell Cards for Assembly: {}".format(assembly.assemblyPosition)
    file.write("c " + assembly_cell_title.center(77, "*") + " \n")
    units = [assembly.fuel, assembly.bond, assembly.clad, assembly.coolant, assembly.blankCoolant,
             assembly.fuelUniverse, assembly.innerDuct, assembly.duct, assembly.plenum,
             assembly.upperReflector, assembly.lowerReflector, assembly.lowerSodium, assembly.upperSodium,
             assembly.assemblyShell, assembly.everythingElse]
    for cell in units:
        file.write(cell.cellCard + '\n')
    file.write("\n")
    assembly_surface_title = "Surface Cards for Fuel Assembly: {}".format(assembly.assemblyPosition)
    file.write("c " + assembly_surface_title.center(77, "*") + "\n")
    units = [assembly.fuel, assembly.bond, assembly.clad, assembly.coolant, assembly.blankCoolant,
             assembly.innerDuct, assembly.plenum,
             assembly.upperReflector, assembly.lowerReflector, assembly.duct, assembly.assemblyShell,
             assembly.lowerSodium, assembly.upperSodium]
    for surface in units:
        file.write(surface.surfaceCard + '\n')
    file.write("\n")
    assembly_data_title = "Data Cards"
    file.write("c " + assembly_data_title.center(77, "*") + "\n")
    assembly_kcode_title = "k-code Information"
    file.write("c " + assembly_kcode_title.center(77, "*") + "\n")
    file.write(k_card)
    file.write("c " + "Material Information".center(77, "*"))
    units = [assembly.fuel, assembly.bond, assembly.clad, assembly.coolant, assembly.blankCoolant,
             assembly.plenum, assembly.upperReflector, assembly.lowerReflector,
             assembly.duct, assembly.assemblyShell, assembly.lowerSodium, assembly.upperSodium]
    for material in units:
        file.write(material.materialCard)
    file.close()


def make_mcnp_problem(global_vars):
    """Create the MCNP specific kcode options."""
    kopts_output = ''
    if global_vars.kopts:
        kopts_output = 'kopts BLOCKSIZE=10 KINETICS=YES PRECURSOR=Yes \n'

    kcode_output = 'kcode ' + str(global_vars.number_particles_generation) + " 1.0 " + \
                   str(global_vars.number_skipped_generations) + " " + str(global_vars.number_generations) + '\n'
    ksrc_output = 'ksrc 0 0 80 \n'
    prdmp_output = 'PRDMP 100 10 100 1 \n'

    mcnp_output = kcode_output + ksrc_output + prdmp_output + kopts_output
    return mcnp_output
