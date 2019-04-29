import glob
import os
import yaml

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/assembly")


class Assembly(object):
    """
    Holds all information required for modeling a basic assembly. Can be inherited to make specific assembly type.
    Current types include:
    Fuel Assembly
    """

    def __init__(self, assemblyInformation):
        self.assemblyDesignation = assemblyInformation[0]
        self.assemblyPosition = assemblyInformation[1]
        self.globalVars = assemblyInformation[2]
        self.universe = self.globalVars.universe
        self.cellNum = self.globalVars.cellNumber
        self.surfaceNum = self.globalVars.surfaceNumber
        self.materialNum = self.globalVars.materialNumber
        self.xcSet = self.globalVars.xc_set
        self.assemblyType = ''
        self.pinsPerAssembly = 0
        self.assemblyPitch = 0.0
        self.ductInnerFlatToFlat = 0.0
        self.ductOuterFlatToFlat = 0.0
        self.ductOuterFlatToFlatMCNPEdge = 0.0
        self.assemblyGap = 0.0
        self.assemblyHeight = 0.0
        self.zPosition = 0.0
        self.coolantMaterial = ''
        self.assemblyMaterial = ''

    def getAssemblyInfo(self, inputs):
        """Assign assembly parameters based on yaml Assembly file."""
        self.pinsPerAssembly = int(inputs['Pins Per Assembly']) if 'Pins Per Assembly' in inputs else 0
        self.assemblyPitch = float(inputs['Assembly Pitch'])
        self.ductInnerFlatToFlat = float(inputs['Duct Inside Flat to Flat']) / 2 if 'Duct Inside Flat to Flat' in \
                                                                                inputs else 0.0
        thickness = float(inputs['Duct Thickness']) if 'Duct Thickness' in inputs else 0.0
        self.ductOuterFlatToFlat = self.ductInnerFlatToFlat + thickness
        self.ductOuterFlatToFlatMCNPEdge = self.ductOuterFlatToFlat * 1.00005
        self.assemblyGap = float(inputs['Assembly Gap']) if 'Assembly Gap' in inputs else 0.0
        self.assemblyHeight = float(inputs['Assembly Height'])
        self.coolantMaterial = inputs['Coolant']
        self.assemblyMaterial = inputs['Assembly Material']
        self.zPosition = float(inputs['Z Position']) if 'Z Position' in inputs else 0.0

    def updateIdentifiers(self, universeTest):
        """Updates cell, surface, material, and universe number to create uniqueness"""
        self.cellNum += 1
        self.surfaceNum += 1
        self.materialNum += 1
        if universeTest:
            self.universe += 1


def assemblyTypeReader(assemblyYamlFile):
    """Reads in the assembly type to determine what type of assembly to build."""
    with open(assemblyYamlFile[0], "r") as mat_file:
        inputs = yaml.safe_load(mat_file)
        assemblyType = inputs['Assembly Type']
    return assemblyType


def getAssemblyLocation(assemblyType):
    """Find the file location for the assembly, and determine if the given assembly exists."""
    assemblyYamlFile = glob.glob(os.path.join(geo_dir, assemblyType + '.yaml'))
    try:
        assert assemblyYamlFile[0][(-(len(assemblyType)+5)):] == '{}.yaml'.format(assemblyType)
    except AssertionError:
        print('No assembly type named {}. Change your assembly type to a previously created assembly, '
              'or create a new assembly.'.format(assemblyType))
    return assemblyYamlFile
