import FRIDGe.fridge.Assembly.FuelAssembly as FuelAssembly
import FRIDGe.fridge.Assembly.Assembly as Assembly
import FRIDGe.fridge.driver.global_variables as gb
import numpy as np

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
    assert baseAssembly.ductOuterFlatToFlat == 0
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
    baseAssembly.updateIdentifiers(False)
    assert baseAssembly.universe == 100
    assert baseAssembly.cellNum == 101
    assert baseAssembly.surfaceNum == 101
    assert baseAssembly.materialNum == 11


def test_fuel_assembly():
    """Check the Fuel Assembly subclass of Assembly."""
    a = FuelAssembly.FuelAssembly(assembly_info)
    assert a.universe == 104
    assert a.cellNum == 114
    assert a.surfaceNum == 114
    assert a.materialNum == 24
    assert a.fuel is not None
    assert a.fuel is not None
    assert a.bond is not None
    assert a.clad is not None
    assert a.coolant is not None
    assert a.blankUniverse is not None
    assert a.blankCoolant is not None
    assert a.latticeUniverse is not None
    assert a.fuelUniverse is not None
    assert a.innerDuct is not None 
    assert a.duct is not None
    assert a.plenum is not None
    assert a.upperReflector is not None
    assert a.lowerReflector is not None
    assert a.upperSodium is not None
    assert a.lowerSodium is not None
    assert a.assemblyShell is not None
    assert a.upperReflectorPosition == [0, 0, 120.6]
    assert a.lowerReflectorPosition == [0, 0, -60.0]
    assert a.everythingElse is not None

    assert a.cladOD == 0.53
    assert a.cladID == 0.53 - 0.037 * 2 
    assert np.allclose(a.fuelDiameter, 0.394907)
    assert a.fuelPitch == 0.66144
    assert a.wireWrapDiameter == 0.126
    assert a.fuelHeight == 60
    assert a.fuelMaterial == '5Pu22U10Zr'
    assert a.cladMaterial == 'HT9'
    assert a.bondMaterial == 'LiquidNa'

    assert a.plenumHeight == 60
    assert a.plenumMaterial == {'HT9': 0.25, 'Void': 0.25, 'LiquidNa': 0.5}
    assert a.plenumPosition == [0, 0, 60.6]

    assert a.reflectorHeight == 60
    assert a.reflectorMaterial == {'LiquidNa': 0.20, 'HT9': 0.80}


def test_getAssemblyLocation():
    assembly_info1 = ['Nonsense', '01A01', global_vars]
    a = Assembly.Assembly(assembly_info1)
    assert a.assemblyType == ''