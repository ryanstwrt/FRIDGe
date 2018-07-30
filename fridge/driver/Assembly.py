import FRIDGe.fridge.utilities.materialReader as materialReader
import numpy as np
import pandas as pd
import glob
import os
import yaml

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/assembly")

class Assembly(object):

    def __init__(self, assemblyInformation):
        self.assemblyType = assemblyInformation[0]
        self.position = assemblyInformation[1]
        self.assemblyReader(self.assemblyType)
        self.getAssemblyMCNP()

    def getAssemblyMCNP(self):
        self.innerDuct = Region([1,1,1, '5Pu22U10Zr', '900K'])

    def getReflectorInfo(self, inputs):
        self.reflectorHeight = float(inputs['Fuel Reflector Height'])
        reflectorSmear = [float(i) for i in inputs['Smear']]
        reflectorMaterial = inputs['Material']
        self.reflectorMaterial = {}
        for num, material in enumerate(reflectorMaterial):
            self.reflectorMaterial[material] = reflectorSmear[num]

    def getAssemblyInfo(self, inputs):
        self.pinsPerAssembly = float(inputs['Pins Per Assembly'])
        self.assemblyPitch = float(inputs['Assembly Pitch'])
        self.ductThickness = float(inputs['Duct Thickness'])
        self.assemblGap = float(inputs['Assembly Gap'])
        self.ductInnerFlatToFlat = float(inputs['Duct Inside Flat to Flat'])
        self.assemblyHeight = float(inputs['Assembly Height'])
        self.coolant = inputs['Coolant']
        self.assemblyMaterial = inputs['Assembly Material']


class FuelAssembly(Assembly):

    def assemblyReader(self, assemblyType):
        assembly_yaml_file = glob.glob(os.path.join(geo_dir, assemblyType + '.yaml'))

        if assembly_yaml_file == []:
            print('\n\033[1;37;31mFatal Error: No assembly type named %s. \nChange your assembly type to a previously created assembly, '
                  'or create a new assembly using the utilities.' % assemblyType)
            quit()

        with open(assembly_yaml_file[0], "r") as mat_file:
            inputs = yaml.load(mat_file)
            self.getFuelRegionInfo(inputs)
            self.getPlenumRegionInfo(inputs)
            self.getReflectorInfo(inputs)
            self.getAssemblyInfo(inputs)

    def getFuelRegionInfo(self, inputs):
        self.fuelDiameter = float(inputs["Pin Diameter"])
        self.cladThickness = float(inputs['Clad Thickness'])
        self.Smear = float(inputs['Fuel Smear'])
        self.fuelPitch = float(inputs['Pitch'])
        self.wireWrapDiameter = float(inputs['Wire Wrap Diameter'])
        self.fuelHeight = float(inputs['Fuel Height'])
        self.fuelMaterial = inputs['Fuel']
        self.cladMaterial = inputs['Clad']
        self.bondMaterial = inputs['Bond']

    def getPlenumRegionInfo(self, inputs):
        self.plenumHeight = float(inputs['Plenum Height'])
        plenumSmear = [float(i) for i in inputs['Plenum Smear']]
        plenumMaterial = inputs["Plenum Material"]
        self.plenumMaterial = {}
        for num, material in enumerate(plenumMaterial):
            self.plenumMaterial[material] = plenumSmear[num]

class Region(object):
    def __init__(self, regionInfo):
        self.universe = regionInfo[0]
        self.surfaceNum = regionInfo[1] + 1
        self.surface = None
        self.cellNum = regionInfo[2] + 1
        self.materialLibrary = regionInfo[4]
        self.cell = None
        self.materialNum = None
        self.position = None
        self.getMaterialCard(regionInfo[3])

    def getMaterialCard(self, material):
        self.materialNum = self.cellNum
        self.material = materialReader.Material(material)
        pass


assembly = FuelAssembly(['A271', '01A01'])
print(assembly.plenumMaterial, assembly.position)