import glob
import os
import yaml

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/assembly")


class Assembly(object):

    def __init__(self, assemblyInformation):
        self.assemblyDesignation = assemblyInformation[0]
        self.assemblyPosition = assemblyInformation[1]
        self.globalVars = assemblyInformation[2]
        self.universe = self.globalVars.universe
        self.cellNum = self.globalVars.cellNumber
        self.surfaceNum = self.globalVars.surfaceNumber
        self.materialNum = self.globalVars.materialNumber
        self.assemblyType = ''
        self.pinsPerAssembly = 0
        self.assemblyPitch = 0
        self.ductInnerFlatToFlat = 0
        self.ductOuterFlatToFlat = 0
        self.ductOuterFlatToFlatMCNPEdge = 0
        self.assemblyGap = 0
        self.assemblyHeight = 0
        self.coolantMaterial = ''
        self.assemblyMaterial = ''

    def getAssemblyInfo(self, inputs):
        self.pinsPerAssembly = float(inputs['Pins Per Assembly'])
        self.assemblyPitch = float(inputs['Assembly Pitch'])
        self.ductInnerFlatToFlat = float(inputs['Duct Inside Flat to Flat'])
        self.ductOuterFlatToFlat = self.ductInnerFlatToFlat + 2*float(inputs['Duct Thickness'])
        self.ductOuterFlatToFlatMCNPEdge = self.ductOuterFlatToFlat * 1.00005
        self.assemblyGap = float(inputs['Assembly Gap'])
        self.assemblyHeight = float(inputs['Assembly Height'])
        self.coolantMaterial = inputs['Coolant']
        self.assemblyMaterial = inputs['Assembly Material']

    def updateIdentifiers(self, universeTest):
        self.cellNum += 1
        self.surfaceNum += 1
        self.materialNum += 1
        if universeTest:
            self.universe += 1


def assemblyTypeReader(assemblyYamlFile):
    with open(assemblyYamlFile[0], "r") as mat_file:
        inputs = yaml.load(mat_file)
        assemblyType = inputs['Assembly Type']
    return assemblyType


def getAssemblyLocation(assemblyType):
    assemblyYamlFile = glob.glob(os.path.join(geo_dir, assemblyType + '.yaml'))
    try:
        assert assemblyYamlFile == '../data/assembly/{}.yaml'.format(assemblyType)
    except AssertionError:
        print('No assembly type named {}. Change your assembly type to a previously created assembly, '
              'or create a new assembly.'.format(assemblyType))
    return assemblyYamlFile
