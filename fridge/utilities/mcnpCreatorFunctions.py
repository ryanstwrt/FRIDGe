import FRIDGe.fridge.utilities.materialReader as materialReader
from decimal import Decimal
import math


def getRCC(radius, height, position, surfaceNum, comment):
    surfaceCard = "{} RCC {} {} {} 0 0 {} {} {}".format(surfaceNum, position[0], position[1], round(position[2], 5),
                                                        round(height, 5), round(radius, 5), comment)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getRHP(pitch, height, position, surfaceNum, comment):
    surfaceCard = "{} RHP {} {} {} 0 0 {} {} 0 0 {}".format(surfaceNum, position[0], position[1], round(position[2], 5),
                                                            round(height, 5), round(pitch, 5), comment)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getRHPRotated(pitch, height, position, surfaceNum, comment):
    surfaceCard = "{} RHP {} {} {} 0 0 {} 0 {} 0 {}".format(surfaceNum, position[0], position[1], round(position[2], 5),
                                                            round(height, 5), round(pitch, 5), comment)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getSingleCell(cellNum, matNum, density, surfaceNum, universe, comment):
    cellCard = "{} {} {} -{} u={} imp:n=1 {}".format(cellNum, matNum, round(density, 5), surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getConcentricCell(cellNum, matNum, density, innerSurface, outerSurface, universe, comment):
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
    cellCard = "{} {} {} {} u={} imp:n=1 {}".format(cellNum, matNum, round(density, 5), surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getFuelLatticeCell(cellNum, surfaceNum, assemblyUniverse, latticeUniverse, comment):
    cellCard = "{} 0 -{} u={} fill={} imp:n=1 {}".format(cellNum, surfaceNum, assemblyUniverse, latticeUniverse,
                                                         comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getAssemblyUniverseCell(cellNum, surfaceNum, universe, comment):
    cellCard = "{} 0 -{} fill={} imp:n=1 {}".format(cellNum, surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getEverythingElseCard(cellNum, surfaceNum, comment):
    cellCard = "{} 0 {} imp:n=0 {}".format(cellNum, surfaceNum, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getMaterialCard(material, xc, matNum):
    materialCard = "\nc Material: {}; Density: {} atoms/bn*cm \nm{}".format(material.name, material.density, matNum)
    i = 0
    for isotope, atomDensity in material.atomPercent.items():
        if i == 3:
            materialCard += "\n    ".format(isotope, xc, Decimal(atomDensity))
            i = 0
        materialCard += " {}.{} {:.4E}".format(isotope, xc, Decimal(atomDensity))
        i += 1
    return materialCard


def getSmearedMaterial(materials, xc, matNum):
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
    newMaterial.density = sum(smearMaterial.values())
    return newMaterial


def getPosition(position, pitch, zPosition):
    ring = int(position[:2]) - 1
    hextant = position[2]
    assemblyNum = int(position[3:]) - 1
    x = 0
    y = 0

    if hextant == 'A':
        x = -ring * math.sqrt(pow(pitch, 2) + (pow(pitch/2, 2)))
        y = ring * pow(pitch/2, 2) + pitch*assemblyNum
    elif hextant == 'B':
        x = pitch*assemblyNum
        y = ring*pitch + pitch/2*assemblyNum
    elif hextant == 'C':
        x = ring * math.sqrt((pow(pitch, 2) - pow(pitch / 2, 2)))
        y = ring * pow(pitch / 2, 2) - pitch * assemblyNum
    elif hextant == 'D':
        x = -ring * math.sqrt(pow(pitch, 2) + (pow(pitch / 2, 2)))
        y = -ring * pow(pitch / 2, 2) - pitch * assemblyNum
    elif hextant == 'E':
        x = -pitch*assemblyNum
        y = ring*pitch - pitch/2*assemblyNum
    elif hextant == 'F':
        x = -ring * math.sqrt((pow(pitch, 2)-pow(pitch/2, 2)))
        y = ring * pow(pitch/2, 2)+pitch*assemblyNum
    return [x, y, zPosition]
