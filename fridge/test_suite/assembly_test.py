from FRIDGe.fridge.driver import Assembly
from FRIDGe.fridge.driver import global_variables as gb

global_vars = gb.GlobalVariables()
global_vars.read_input_file('A271_Assembly_Test')
assembly_info = [global_vars.assembly_name, '01A01', global_vars]


def test_assembly():
    """Check the base assembly init"""
    baseAssembly = Assembly.Assembly(assembly_info)
    assert baseAssembly.assemblyDesignation == 'A271_Test'
    assert baseAssembly.assemblyPosition == '01A01'
    assert baseAssembly.universe == 100
    assert baseAssembly.cellNum == 100
    assert baseAssembly.surfaceNum == 100
    assert baseAssembly.materialNum == 10
    assert baseAssembly.assemblyType == ''
    assert baseAssembly.pinsPerAssembly == 0
    assert baseAssembly.assemblyPitch == 0
    assert baseAssembly.ductInnerFlatToFlat == 0
    assert baseAssembly.ductOuterFlatToFlat == 0
    assert baseAssembly.ductOuterFlatToFlatUniverse == 0
    assert baseAssembly.assemblyGap == 0
    assert baseAssembly.assemblyHeight == 0
    assert baseAssembly.coolantMaterial == ''
    assert baseAssembly.assemblyMaterial == ''


def test_updateIdentifiers():
    """Check the updateIdentifiers function"""
    baseAssembly = Assembly.Assembly(assembly_info)
    assert baseAssembly.universe == 100
    assert baseAssembly.cellNum == 100
    assert baseAssembly.surfaceNum == 100
    assert baseAssembly.materialNum == 10
    baseAssembly.updateIdentifiers()
    assert baseAssembly.universe == 100
    assert baseAssembly.cellNum == 101
    assert baseAssembly.surfaceNum == 101
    assert baseAssembly.materialNum == 11
