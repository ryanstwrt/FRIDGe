import fridge.Assembly.FuelAssembly as FuelAssembly
import fridge.Assembly.SmearAssembly as SmearAssembly
import fridge.Assembly.Assembly as Assembly
import fridge.driver.global_variables as gb
import numpy as np

global_vars = gb.GlobalVariables()
global_vars.read_input_file('A271_Assembly_Shifted_Test')
assembly_info = [global_vars.file_name, '01A01', global_vars, None]


def test_assembly():
    """Check the base assembly init"""
    baseAssembly = Assembly.Assembly(assembly_info)
    assert baseAssembly.assembly_file_name == 'A271_Shifted_Test'
    assert baseAssembly.assemblyPosition == '01A01'
    assert baseAssembly.universe == 100
    assert baseAssembly.cellNum == 100
    assert baseAssembly.surfaceNum == 100
    assert baseAssembly.materialNum == 100
    assert baseAssembly.assemblyType == ''
    assert baseAssembly.pinsPerAssembly == 0
    assert baseAssembly.assemblyPitch == 0
    assert baseAssembly.ductInnerFlatToFlat == 0
    assert baseAssembly.ductOuterFlatToFlat == 0
    assert baseAssembly.ductOuterFlatToFlat == 0
    assert baseAssembly.assemblyHeight == 0
    assert baseAssembly.coolantMaterial == ''
    assert baseAssembly.assemblyMaterial == ''


def test_updateIdentifiers():
    """Check the updateIdentifiers function"""
    baseAssembly = Assembly.Assembly(assembly_info)
    assert baseAssembly.universe == 100
    assert baseAssembly.cellNum == 100
    assert baseAssembly.surfaceNum == 100
    assert baseAssembly.materialNum == 100
    baseAssembly.update_global_identifiers(False)
    assert baseAssembly.universe == 100
    assert baseAssembly.cellNum == 101
    assert baseAssembly.surfaceNum == 101
    assert baseAssembly.materialNum == 101


def test_getAssemblyLocation():
    assembly_info1 = ['Nonsense', '01A01', global_vars, None]
    a = None
    try:
        a = Assembly.Assembly(assembly_info1)
    except IndexError:
        assert a is None


global_vars = gb.GlobalVariables()
global_vars.read_input_file('Five_Axial_Fuel_Assembly_Test')
assembly_info2 = [global_vars.file_name, '01A01', global_vars, None]


def test_fiveAxialFuelAssembly():
    a = FuelAssembly.FuelAssembly(assembly_info2)
    assert a.assemblyPitch == 12
    assert a.coolantMaterial == 'LiquidNa'
    assert a.assemblyMaterial == 'HT9'
    assert a.xcSet == '.81c'

    #Check fuel pins
    assert a.cladOD == 0.53
    assert a.cladID == 0.53 - 0.037 * 2
    assert np.allclose(a.fuelDiameter, 0.394907)
    assert a.fuelPitch == 0.66144
    assert a.wireWrapDiameter == 0.126
    assert a.fuelHeight == 60
    assert a.pinsPerAssembly == 271
    assert np.allclose(a.fuel_volume, 1991.597)
    assert a.fuelMaterial == '5Pu22U10Zr'
    assert a.cladMaterial == 'HT9'
    assert a.bondMaterial == 'LiquidNa'

    #Check Axial smear materials
    known_mats = [{'LiquidNa': 0.2, 'HT9': 0.8}, {}, {'LiquidNa': 0.50, 'Void': 0.25, 'HT9': 0.25}, {'LiquidNa': 0.2, 'HT9': 0.8}]
    known_cell = ['100 100 0.07364 -100 u=100 imp:n=1 $Assembly: Lower Reflector', {},
                  '109 109 0.03364 -109 u=100 imp:n=1 $Assembly: Plenum',
                  '110 110 0.07364 -110 u=100 imp:n=1 $Assembly: Upper Reflector']
    known_surf = ['100 RHP 0.0 0.0 -20.1 0 0 20.1 0 5.80529 0 $Assembly: Lower Reflector', {},
                  '109 RHP 0.0 0.0 60.6 0 0 60 0 5.80529 0 $Assembly: Plenum',
                  '110 RHP 0.0 0.0 120.6 0 0 20 0 5.80529 0 $Assembly: Upper Reflector']
    for k, v in a.axialRegions.items():
        assert v.materialSmear == known_mats[k-1]
        assert v.cellCard == known_cell[k-1]
        assert v.surfaceCard == known_surf[k-1]

    #Check fuel section
    assert a.fuel.cellCard == '101 101 0.04574 -101 u=101 vol=1991.597 imp:n=1 $Pin: Fuel'
    assert a.fuel.surfaceCard == '101 RCC 0.0 0.0 0.0 0 0 60.0 0.19745 $Pin: Fuel'
    assert a.bond.cellCard == '102 102 0.02428 101 -102 u=101 imp:n=1 $Pin: Bond'
    assert a.bond.surfaceCard == '102 RCC 0.0 0.0 0.0 0 0 60.6 0.228 $Pin: Bond - 1% higher than fuel'
    assert a.clad.cellCard == '103 103 0.08598 102 -103 u=101 imp:n=1 $Pin: Clad'
    assert a.clad.surfaceCard == '103 RCC 0.0 0.0 0.0 0 0 60.6 0.265 $Pin: Clad - 1% higher than fuel'
    assert a.coolant.cellCard == '104 104 0.02929 103 u=101 imp:n=1 $Pin: Wirewrap + Coolant'
    assert a.coolant.surfaceCard == '104 RHP 0.0 0.0 0.0 0 0 60.6 0.66144 0 0 $Pin: Coolant - 1% higher than fuel'
    assert a.blankCoolant.cellCard == '105 105 0.02428 -104 u=102 imp:n=1 $Pin: Blank Pin Coolant'
    assert a.blankCoolant.surfaceCard == '105 RHP 0.0 0.0 0.0 0 0 60.6 0.33072 0 0 $Pin: Blank Pin - 1%\
 higher than fuel'
    assert a.fuelUniverse.cellCard == '106 0 -105 lat=2 u=103 imp:n=1\n'\
                                      '     fill=-10:10 -10:10 0:0\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 102 102 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 102 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 102 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 102 102 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102'
    assert a.innerDuct.cellCard == '107 0 -107 u=100 fill=103 imp:n=1 $Assembly: Inner Portion of Assembly'
    assert a.innerDuct.surfaceCard == '107 RHP 0.0 0.0 0.0 0 0 60.6 0 5.505 0 $Assembly: Duct Inner Surface'
    assert a.duct.cellCard == '108 108 0.08598 107 -108 u=100 imp:n=1 $Assembly: Assembly Duct'
    assert a.duct.surfaceCard == '108 RHP 0.0 0.0 0.0 0 0 60.6 0 5.80529 0 $Assembly: Duct Outer Surface'
    assert a.assemblyShell.cellCard == '111 0 -111 fill=100 imp:n=1 $Assembly'
    assert a.assemblyShell.surfaceCard == '111 RHP 0.0 0.0 -20 0 0 160.0 0 5.805 0 $Assembly: Full Assembly Surface'
    assert a.everythingElse.cellCard == '112 0 111 imp:n=0 $Everything Else'


global_vars = gb.GlobalVariables()
global_vars.read_input_file('Three_Axial_Fuel_Assembly_Test')
assembly_info3 = [global_vars.file_name, '01A01', global_vars, None]

def test_threeAxialFuelAssembly():
    a = FuelAssembly.FuelAssembly(assembly_info3)
    assert a.assemblyPitch == 12
    assert a.coolantMaterial == 'LiquidNa'
    assert a.assemblyMaterial == 'HT9'
    assert a.xcSet == '.37c'

    #Check fuel pins
    assert a.cladOD == 0.53
    assert a.cladID == 0.53 - 0.037 * 2
    assert np.allclose(a.fuelDiameter, 0.394907)
    assert a.fuelPitch == 0.66144
    assert a.wireWrapDiameter == 0.126
    assert a.fuelHeight == 60
    assert a.pinsPerAssembly == 271
    assert np.allclose(a.fuel.volume, 1994.916)
    assert a.fuelMaterial == '5Pu22U10Zr'
    assert a.cladMaterial == 'HT9'
    assert a.bondMaterial == 'LiquidNa'

    #Check Axial smear materials
    known_mats = [{}, {'LiquidNa': 0.50, 'Void': 0.25, 'HT9': 0.25}, {'LiquidNa': 0.2, 'HT9': 0.8}]
    known_cell = [{},
                  '108 108 0.03364 -108 u=100 imp:n=1 $Assembly: Plenum',
                  '109 109 0.07364 -109 u=100 imp:n=1 $Assembly: Upper Reflector']
    known_surf = [{},
                  '108 RHP 0.0 0.0 60.6 0 0 60 0 5.80529 0 $Assembly: Plenum',
                  '109 RHP 0.0 0.0 120.6 0 0 20 0 5.80529 0 $Assembly: Upper Reflector']

    for k, v in a.axialRegions.items():
        assert v.materialSmear == known_mats[k-1]
        assert v.cellCard == known_cell[k-1]
        assert v.surfaceCard == known_surf[k-1]

    #Check fuel section
    assert a.fuel.cellCard == '100 100 0.04574 -100 u=101 vol=1994.916 imp:n=1 $Pin: Fuel'
    assert a.fuel.surfaceCard == '100 RCC 0.0 0.0 -0.1 0 0 60.1 0.19745 $Pin: Fuel'
    assert a.bond.cellCard == '101 101 0.02428 100 -101 u=101 imp:n=1 $Pin: Bond'
    assert a.bond.surfaceCard == '101 RCC 0.0 0.0 -0.1 0 0 60.7 0.228 $Pin: Bond - 1% higher than fuel'
    assert a.clad.cellCard == '102 102 0.08598 101 -102 u=101 imp:n=1 $Pin: Clad'
    assert a.clad.surfaceCard == '102 RCC 0.0 0.0 -0.1 0 0 60.7 0.265 $Pin: Clad - 1% higher than fuel'
    assert a.coolant.cellCard == '103 103 0.02929 102 u=101 imp:n=1 $Pin: Wirewrap + Coolant'
    assert a.coolant.surfaceCard == '103 RHP 0.0 0.0 -0.1 0 0 60.7 0.66144 0 0 $Pin: Coolant - 1% higher than fuel'
    assert a.blankCoolant.cellCard == '104 104 0.02428 -103 u=102 imp:n=1 $Pin: Blank Pin Coolant'
    assert a.blankCoolant.surfaceCard == '104 RHP 0.0 0.0 -0.1 0 0 60.7 0.33072 0 0 $Pin: Blank Pin - 1%\
 higher than fuel'
    assert a.fuelUniverse.cellCard == '105 0 -104 lat=2 u=103 imp:n=1\n'\
                                      '     fill=-10:10 -10:10 0:0\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 102 102 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 102 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 102 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 102 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 102 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 102 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 102 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 102\n'\
                                      '      102 101 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 101 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 101 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 101 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 101 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 101 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 101 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 102 101 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 102 102 101\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      101 101 101 101 101 101 101 101 101 101\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102 102 102 102 102 102 102 102 102 102\n'\
                                      '      102'
    assert a.innerDuct.cellCard == '106 0 -106 u=100 fill=103 imp:n=1 $Assembly: Inner Portion of Assembly'
    assert a.innerDuct.surfaceCard == '106 RHP 0.0 0.0 -0.1 0 0 60.7 0 5.505 0 $Assembly: Duct Inner Surface'
    assert a.duct.cellCard == '107 107 0.08598 106 -107 u=100 imp:n=1 $Assembly: Assembly Duct'
    assert a.duct.surfaceCard == '107 RHP 0.0 0.0 -0.1 0 0 60.7 0 5.80529 0 $Assembly: Duct Outer Surface'
    assert a.assemblyShell.cellCard == '110 0 -110 fill=100 imp:n=1 $Assembly'
    assert a.assemblyShell.surfaceCard == '110 RHP 0.0 0.0 0 0 0 140.0 0 5.805 0 $Assembly: Full Assembly Surface'
    assert a.everythingElse.cellCard == '111 0 110 imp:n=0 $Everything Else'


global_vars = gb.GlobalVariables()
global_vars.read_input_file('A271_Assembly_Shifted_Test')
assembly_info4 = [global_vars.file_name, '01A01', global_vars, None]

def test_shifted_fuel_assembly():
    a = FuelAssembly.FuelAssembly(assembly_info4)
    assert a.assemblyPitch == 12
    assert a.coolantMaterial == 'LiquidNa'
    assert a.assemblyMaterial == 'HT9'
    assert a.xcSet == '.72c'

    # Check fuel pins
    assert a.cladOD == 0.53
    assert a.cladID == 0.53 - 0.037 * 2
    assert np.allclose(a.fuelDiameter, 0.394907)
    assert a.fuelPitch == 0.66144
    assert a.wireWrapDiameter == 0.126
    assert a.fuelHeight == 60
    assert a.pinsPerAssembly == 271
    assert np.allclose(a.fuel.volume, 1994.916)
    assert a.fuelMaterial == '5Pu22U10Zr'
    assert a.cladMaterial == 'HT9'
    assert a.bondMaterial == 'LiquidNa'

    # Check Axial smear materials
    known_mats = [{}, {'LiquidNa': 0.50, 'Void': 0.25, 'HT9': 0.25}, {'LiquidNa': 0.2, 'HT9': 0.8}]
    known_cell = [{},
                  '108 108 0.03364 -108 u=100 imp:n=1 $Assembly: Plenum',
                  '109 109 0.07364 -109 u=100 imp:n=1 $Assembly: Upper Reflector']
    known_surf = [{},
                  '108 RHP 0.0 0.0 60.6 0 0 60 0 5.80529 0 $Assembly: Plenum',
                  '109 RHP 0.0 0.0 120.6 0 0 20 0 5.80529 0 $Assembly: Upper Reflector']

    for k, v in a.axialRegions.items():
        assert v.materialSmear == known_mats[k - 1]
        assert v.cellCard == known_cell[k - 1]
        assert v.surfaceCard == known_surf[k - 1]

    # Check fuel section
    assert a.fuel.cellCard == '100 100 0.04574 -100 u=101 vol=1994.916 imp:n=1 $Pin: Fuel'
    assert a.fuel.surfaceCard == '100 RCC 0.0 0.0 -0.1 0 0 60.1 0.19745 $Pin: Fuel'
    assert a.bond.cellCard == '101 101 0.02428 100 -101 u=101 imp:n=1 $Pin: Bond'
    assert a.bond.surfaceCard == '101 RCC 0.0 0.0 -0.1 0 0 60.7 0.228 $Pin: Bond - 1% higher than fuel'
    assert a.clad.cellCard == '102 102 0.08598 101 -102 u=101 imp:n=1 $Pin: Clad'
    assert a.clad.surfaceCard == '102 RCC 0.0 0.0 -0.1 0 0 60.7 0.265 $Pin: Clad - 1% higher than fuel'
    assert a.coolant.cellCard == '103 103 0.02929 102 u=101 imp:n=1 $Pin: Wirewrap + Coolant'
    assert a.coolant.surfaceCard == '103 RHP 0.0 0.0 -0.1 0 0 60.7 0.66144 0 0 $Pin: Coolant - 1% higher than fuel'
    assert a.blankCoolant.cellCard == '104 104 0.02428 -103 u=102 imp:n=1 $Pin: Blank Pin Coolant'
    assert a.blankCoolant.surfaceCard == '104 RHP 0.0 0.0 -0.1 0 0 60.7 0.33072 0 0 $Pin: Blank Pin - 1% higher than fuel'
    assert a.fuelUniverse.cellCard == '105 0 -104 lat=2 u=103 imp:n=1\n' \
                                      '     fill=-10:10 -10:10 0:0\n' \
                                      '      102 102 102 102 102 102 102 102 102 102\n' \
                                      '      102 102 102 102 102 102 102 102 102 102\n' \
                                      '      102 102 102 102 102 102 102 102 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 102 102 102 102 102 102 102 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 102 102 102 102 102 102 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 102 102 102 102 102 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 102 102 102 102 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 102 102 102 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 102 102 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 102 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 102 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 102\n' \
                                      '      102 101 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 101 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 101 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 102 101 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 102 102 101 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 102 102 102 101 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 102 102 102 102 101 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 102 102 102 102 102 101 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 102 102 102 102 102 102 101\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 102 102 102 102 102 102 102\n' \
                                      '      101 101 101 101 101 101 101 101 101 101\n' \
                                      '      102 102 102 102 102 102 102 102 102 102\n' \
                                      '      102 102 102 102 102 102 102 102 102 102\n' \
                                      '      102 102 102 102 102 102 102 102 102 102\n' \
                                      '      102'
    assert a.innerDuct.cellCard == '106 0 -106 u=100 fill=103 imp:n=1 $Assembly: Inner Portion of Assembly'
    assert a.innerDuct.surfaceCard == '106 RHP 0.0 0.0 -0.1 0 0 60.7 0 5.505 0 $Assembly: Duct Inner Surface'
    assert a.duct.cellCard == '107 107 0.08598 106 -107 u=100 imp:n=1 $Assembly: Assembly Duct'
    assert a.duct.surfaceCard == '107 RHP 0.0 0.0 -0.1 0 0 60.7 0 5.80529 0 $Assembly: Duct Outer Surface'
    assert a.assemblyShell.cellCard == '110 0 -110 fill=100 imp:n=1 $Assembly'
    assert a.assemblyShell.surfaceCard == '110 RHP 0.0 0.0 0 0 0 140.0 0 5.805 0 $Assembly: Full Assembly Surface'
    assert a.everythingElse.cellCard == '111 0 110 imp:n=0 $Everything Else'


global_vars = gb.GlobalVariables()
core = 'Three_Axial_Fuel_Assembly_Test'
assem = 'A271_Three_Axial_Test'
global_vars.read_input_file(core, assembly_perturbations={assem: {'fuelMaterial': 'U10Zr', 'fuelDiameter': 0.1,
                                                                  'cladMaterial': 'SS316'}})
assembly_info5 = [global_vars.file_name, '01A01', global_vars, None]


def test_fueled_perturbation():
    a = FuelAssembly.FuelAssembly(assembly_info5)
    assert a.fuelMaterial == 'U10Zr'
    assert a.fuelDiameter == 0.1
    assert a.cladMaterial == 'SS316'


global_vars = gb.GlobalVariables()
global_vars.read_input_file('Smear_Assembly_Test')
assembly_inf6 = [global_vars.file_name, '01A01', global_vars, None]


def test_smearAssemblyUniAxial():
    a = SmearAssembly.SmearAssembly(assembly_inf6)
    assert a.assemblyPitch == 12
    assert a.coolantMaterial == 'LiquidNa'
    assert a.assemblyMaterial == 'HT9'
    known_mats = [{'LiquidNa': 0.9, 'HT9': 0.1}]
    known_cell = ['100 100 0.03045 -100 u=100 imp:n=1 $Assembly: Test_Region']
    known_surf = ['100 RHP 0.0 0.0 -50.1 0 0 110.1 0 5.85029 0 $Assembly: Test_Region']
    for k, v in a.smearRegions.items():
        assert v.materialSmear == known_mats[k-1]
        assert v.cellCard == known_cell[k-1]
        assert v.surfaceCard == known_surf[k-1]

    assert a.assemblyShell.cellCard == '101 0 -101 fill=100 imp:n=1 $Assembly'
    assert a.assemblyShell.surfaceCard == '101 RHP 0.0 0.0 -50.0 0 0 110.0 0 5.85 0 $Assembly: Full Assembly Surface'


global_vars = gb.GlobalVariables()
global_vars.read_input_file('Axial_Smear_Assembly_Test')
assembly_info7 = [global_vars.file_name, '01A01', global_vars, None]


def test_smearAssemblyMultiAxial():
    a = SmearAssembly.SmearAssembly(assembly_info7)
    assert a.assemblyPitch == 12
    assert a.coolantMaterial == 'LiquidNa'
    assert a.assemblyMaterial == 'HT9'
    known_mats = [{'LiquidNa': 0.9, 'HT9': 0.1}, {'LiquidNa': 0.5, 'HT9': 0.5}, {'LiquidNa': 0.6, 'HT9': 0.4}]
    known_cell = ['100 100 0.03045 -100 u=100 imp:n=1 $Assembly: Test_Region',
                  '101 101 0.05513 -101 u=100 imp:n=1 $Assembly: Test_Region2',
                  '102 102 0.04896 -102 u=100 imp:n=1 $Assembly: Test_Region3']
    known_surf = ['100 RHP 0.0 0.0 -50.1 0 0 110.1 0 5.85029 0 $Assembly: Test_Region',
                  '101 RHP 0.0 0.0 60.0 0 0 110 0 5.85029 0 $Assembly: Test_Region2',
                  '102 RHP 0.0 0.0 170.0 0 0 50 0 5.85029 0 $Assembly: Test_Region3']
    for k, v in a.smearRegions.items():
        assert v.materialSmear == known_mats[k-1]
        assert v.cellCard == known_cell[k-1]
        assert v.surfaceCard == known_surf[k-1]

    assert a.assemblyShell.cellCard == '103 0 -103 fill=100 imp:n=1 $Assembly'
    assert a.assemblyShell.surfaceCard == '103 RHP 0.0 0.0 -50.0 0 0 270.0 0 5.85 0 $Assembly: Full Assembly Surface'

global_vars = gb.GlobalVariables()
core = 'Smear_Assembly_Test'
assem = 'Axial_Blank'
global_vars.read_input_file(core, assembly_perturbations={assem: {'Axial Region 1':
                                                                 {'Smear Materials': {'LiquidPb': 1.0},
                                                                  'Smear Height': 50}, 'zPosition': 50}})
assembly_info8 = [global_vars.file_name, '01A01', global_vars, None]

def test_smear_perturbation():
    a = SmearAssembly.SmearAssembly(assembly_info8)
    axial_region = a.smearRegions[1]
    assert axial_region.materialSmear == {'LiquidPb': 1.0}
    assert a.zPosition == 50
    assert axial_region.height == 50.1

global_vars = gb.GlobalVariables()
global_vars.read_input_file('FFTF_Driver')
assembly_info9 = [global_vars.file_name, '01A01', global_vars, None]

def test_fftf_driver():
    a = FuelAssembly.FuelAssembly(assembly_info9)
    for k, v in a.coolant.material.atomDensities.items():
        print(k, v)
    print(a.coolant.material.atomDensity)
