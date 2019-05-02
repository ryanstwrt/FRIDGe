import fridge.Material.Material as materialReader
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
    uCard = ''
    if type(universe) is int:
        uCard = 'u=' + str(universe)
    cellCard = "{} {} {} -{} {} imp:n=1 {}".format(cellNum, matNum, round(density, 5), surfaceNum, uCard, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getConcentricCell(cellNum, matNum, density, innerSurface, outerSurface, universe, comment):
    """Create a cell which has multiple components inside a cell."""
    uCard = ''
    if type(universe) is int:
        uCard = 'u=' + str(universe)
    listType = []
    if type(innerSurface) == type(listType):
        newInnerSurface = ''
        i = 1
        for surface in innerSurface:
            if i % 5 == 0:
                newInnerSurface += ' {}\n     '.format(surface)
            else:
                newInnerSurface += ' {}'.format(surface)
            i += 1
        innerSurface = newInnerSurface

    cellCard = "{} {} {} {} -{} {} imp:n=1 {}".format(cellNum, matNum, round(density, 5), innerSurface, outerSurface,
                                                        uCard, comment)
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
        materialCard += " {}{} {:.4E}".format(isotope, xc, Decimal(atomDensity))
        i += 1
    return materialCard


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


def getSmearedMaterial(materials, voidMaterial = '', voidPercent = 1.0):
    """Create the material data card for a smeared material."""
    smearMaterial = {}
    avogadros = materialReader.AVOGADROS_NUMBER
    voidMultiplier = 1.0
    for material, materialWeightPercent in materials.items():
        if material == 'Void':
            pass
        else:
            materialClass = materialReader.Material()
            materialClass.set_material(material)

            if materialClass.materialName == voidMaterial:
                voidMultiplier = voidPercent
            else:
                voidMultiplier = 1.0

            for isotope, isotopeWeightPercent in materialClass.weightPercent.items():
                element = str(isotope)
                if len(element) < 5:
                    currentElement = element[:1] + '000'
                else:
                    currentElement = element[:2] + '000'
                currentElement = int(currentElement)
                try:
                    smearMaterial[isotope] += isotopeWeightPercent * materialWeightPercent * materialClass.density \
                                              * avogadros * voidMultiplier / \
                                              materialClass.elementDict[currentElement].molecularMassDict[isotope]
                except KeyError:
                    smearMaterial[isotope] = isotopeWeightPercent * materialWeightPercent * materialClass.density \
                                             * avogadros * voidMultiplier / \
                                             materialClass.elementDict[currentElement].molecularMassDict[isotope]
    newMaterial = materialReader.Material()
    newMaterial.name = "{}".format([val for val in materials])
    newMaterial.atomDensity = sum(smearMaterial.values())
    smearMaterialAtomPercent = {}
    for k, v in smearMaterial.items():
        smearMaterialAtomPercent[k] = v / newMaterial.atomDensity
    newMaterial.atomPercent = smearMaterialAtomPercent
    return newMaterial


def getCoolantWireWrapSmear(info):
    """Returns a smeared material for the coolant and wire wrap."""
    height = info[0]
    fuelradius = info[1] / 2
    wireWrapRadius = info[2] / 2
    wireWrapAxialPitch = info[3]
    fuelPitch = info[4]
    coolantMaterial = info[5]
    cladMaterial = info[6]
    fuelVolume = getRCCVolume(fuelradius, height)
    wireWrapVolume = getToroidalVolume(fuelradius, wireWrapRadius, wireWrapAxialPitch, height)
    pinHexagonalUniverseVolume = getRHPVolume(fuelPitch, height)
    coolantVolume = pinHexagonalUniverseVolume - fuelVolume - wireWrapVolume
    totalCoolantWireWrapVolume = coolantVolume + wireWrapVolume
    wireWrapVolumePercent = wireWrapVolume / totalCoolantWireWrapVolume
    coolantVolumePercent = coolantVolume / totalCoolantWireWrapVolume
    smearedMaterialDict = {cladMaterial: wireWrapVolumePercent, coolantMaterial: coolantVolumePercent}
    return smearedMaterialDict


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


def make_mcnp_problem(global_vars):
    """Create the MCNP specific kcode options."""
    kopts_output = ''
    if global_vars.kopts:
        kopts_output = 'kopts BLOCKSIZE=10 KINETICS=YES PRECURSOR=Yes \n'

    kcode_output = 'kcode ' + str(global_vars.number_particles_generation) + " 1.0 " + \
                   str(global_vars.number_skipped_generations) + " " + str(global_vars.number_generations) + '\n'
    ksrc_output = 'ksrc 0 -12 40 \n'
    prdmp_output = 'PRDMP 100 10 100 1 \n'
    dbcn_output = 'DBCN 68J 50000 \n'

    mcnp_output = kcode_output + ksrc_output + prdmp_output + kopts_output + dbcn_output
    return mcnp_output
