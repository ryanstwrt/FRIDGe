import fridge.Constituent.Constituent as Constituent
import fridge.Constituent.BlankCoolant as BlankCoolant
import fridge.Constituent.Duct as Duct
import fridge.Constituent.EveryThingElse as EveryThingElse
import fridge.Constituent.FuelBond as FuelBond
import fridge.Constituent.FuelClad as FuelClad
import fridge.Constituent.FuelCoolant as FuelCoolant
import fridge.Constituent.FuelPin as FuelPin
import fridge.Constituent.FuelUniverse as FuelUniverse
import fridge.Constituent.InnerDuct as InnerDuct
import fridge.Constituent.LowerCoolant as LowerCoolant
import fridge.Constituent.OuterShell as OuterShell
import fridge.Constituent.Smear as Smear
import fridge.Constituent.UpperCoolant as UpperCoolant
import fridge.Constituent.CoreCoolant as CoreCoolant
import fridge.Constituent.ReactorVessel as ReactorVessel
import fridge.utilities.materialReader as mr

constituentInfo = [[0, 1, 2, 'LiquidNa', '.82c', [1, 1, 1], 3], []]


def test_constituent():
    c = Constituent.Constituent(constituentInfo)
    c.makeComponent([0])
    assert c.universe == 0
    assert c.surfaceNum == 2
    assert c.cellNum == 1
    assert c.materialXCLibrary == '.82c'
    assert c.position == [1, 1, 1]
    assert c.materialNum == 3
    assert c.surfaceCard == ''
    assert c.cellCard == ''
    assert c.materialCard == ''
    assert c.material is None


def test_constituent_getMaterialCard():
    c = Constituent.Constituent(constituentInfo)
    sodium = mr.Material()
    sodium.setMaterial('LiquidNa')
    knownMaterialCard = '\nc Material: Liquid Sodium; Density: 0.02428 atoms/bn*cm \nm3 11023.82c 1.0000E+0'
    c.getMaterialCard(constituentInfo[0][3])
    assert sodium.name == c.material.name
    assert knownMaterialCard == c.materialCard


def test_blankCoolant():
    blankCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = BlankCoolant.BlankCoolant(blankCoolantInfo)
    cellCard = '1 3 0.02428 -4 u=0 imp:n=1 $Pin: Blank Pin Coolant'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.2 0.05 0 0 $Pin: Blank Pin - 1% higher than fuel'
    assert c.pitch == 0.1 / 2
    assert c.height == 0.2
    assert c.blankCoolantSurfaceNum == 4
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_blankCoolant_voided():
    blankCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = BlankCoolant.BlankCoolant(blankCoolantInfo, voidPercent=0.1)
    cellCard = '1 3 0.00243 -4 u=0 imp:n=1 $Pin: Blank Pin Coolant'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.2 0.05 0 0 $Pin: Blank Pin - 1% higher than fuel'
    assert c.pitch == 0.1 / 2
    assert c.height == 0.2
    assert c.blankCoolantSurfaceNum == 4
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_duct():
    ductInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = Duct.Duct(ductInfo)
    cellCard = '1 3 0.02428 4 -2 u=0 imp:n=1 $Assembly: Assembly Duct'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.2 0 0.1 0 $Assembly: Duct Outer Surface'
    assert c.flat2flat == 0.1
    assert c.height == 0.20
    assert c.innerSurfaceNum == 4
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_EverythingElse():
    everyThingElseInfo = [1, 2]
    c = EveryThingElse.EveryThingElse(everyThingElseInfo)
    cellCard = '1 0 2 imp:n=0 $Everything Else'
    assert c.assemblySurfaceNum == 2
    assert cellCard == c.cellCard


def test_fuelBond():
    fuelBondInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = FuelBond.FuelBond(fuelBondInfo)
    cellCard = '1 3 0.02428 4 -2 u=0 imp:n=1 $Pin: Bond'
    surfaceCard = '2 RCC 1.0 1.0 1.0 0 0 0.2 0.05 $Pin: Bond - 1% higher than fuel'
    assert c.radius == 0.1 / 2
    assert c.height == 0.2
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelClad():
    fuelCladInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = FuelClad.FuelClad(fuelCladInfo)
    cellCard = '1 3 0.02428 4 -2 u=0 imp:n=1 $Pin: Clad'
    surfaceCard = '2 RCC 1.0 1.0 1.0 0 0 0.2 0.05 $Pin: Clad - 1% higher than fuel'
    assert c.radius == 0.1 / 2
    assert c.height == 0.2
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelCoolant():
    fuelCoolantInfo = [[0, 1, 2, {'LiquidNa': 1.0}, '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4], 'Wirewrap + Coolant']
    c = FuelCoolant.FuelCoolant(fuelCoolantInfo)
    cellCard = '1 3 0.02428 4 u=0 imp:n=1 $Pin: Wirewrap + Coolant'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.2 0.1 0 0 $Pin: Coolant - 1% higher than fuel'
    assert c.flat2flat == 0.1
    assert c.height == 0.2
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelCoolant():
    fuelCoolantInfo = [[0, 1, 2, {'LiquidNa': 1.0}, '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4], 'Wirewrap + Coolant']
    c = FuelCoolant.FuelCoolant(fuelCoolantInfo, voidMaterial='LiquidNa', voidPercent=0.1)
    cellCard = '1 3 0.00243 4 u=0 imp:n=1 $Pin: Wirewrap + Coolant'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.2 0.1 0 0 $Pin: Coolant - 1% higher than fuel'
    assert c.flat2flat == 0.1
    assert c.height == 0.2
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelPin():
    fuelPinInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2]]
    c = FuelPin.FuelPin(fuelPinInfo)
    cellCard = '1 3 0.02428 -2 u=0 imp:n=1 $Pin: Fuel'
    surfaceCard = '2 RCC 1.0 1.0 1.0 0 0 0.2 0.05 $Pin: Fuel'
    assert c.radius == 0.1 / 2
    assert c.height == 0.2
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelUniverse():
    fuelUniverseInfo = [1, 2, 7, 3, 4, 5]
    c = FuelUniverse.FuelUniverse(fuelUniverseInfo)
    cellCard = '3 0 -4 lat=2 u=5 imp:n=1\n     fill=-2:2 -2:2 0:0\n' \
               '      2 2 2 2 2 2 2 1 1 2\n' \
               '      2 1 1 1 2 2 1 1 2 2\n' \
               '      2 2 2 2 2'
    assert cellCard == c.cellCard


def test_innerDuct():
    innerDuctInfo = [[0, 1, 2, 'HT9', '82c', [1.0, 1.0, 1.0], 3], [4, 5, 0.1, 0.2]]
    c = InnerDuct.InnerDuct(innerDuctInfo)
    cellCard = '1 0 -2 u=4 fill=5 imp:n=1 $Assembly: Inner Portion of Assembly'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.2 0 0.1 0 $Assembly: Duct Inner Surface'
    assert c.assemblyUniverse == 4
    assert c.latticeUniverse == 5
    assert c.flat2flat == 0.1
    assert c.height == 0.2
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_lowerCoolant():
    lowerCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [0.0, 0.0, -20.0], 3], [10.0, 0.2]]
    c = LowerCoolant.LowerCoolant(lowerCoolantInfo)
    cellCard = '1 3 0.02428 -2 u=0 imp:n=1 $Assembly: Lower Coolant'
    surfaceCard = '2 RHP 0.0 0.0 -20.1 0 0 10.1 0 0.2 0 $Assembly: Lower Coolant'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard

def test_lowerCoolant_void():
    lowerCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [0.0, 0.0, -20.0], 3], [10.0, 0.2]]
    c = LowerCoolant.LowerCoolant(lowerCoolantInfo, voidPercent=0.1)
    cellCard = '1 3 0.00243 -2 u=0 imp:n=1 $Assembly: Lower Coolant'
    surfaceCard = '2 RHP 0.0 0.0 -20.1 0 0 10.1 0 0.2 0 $Assembly: Lower Coolant'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_outershell():
    outerShellInfo = [[0, 1, 2, 'LiquidNa', '82c', [0.0, 0.0, -20.0], 3], [50, 0.2]]
    c = OuterShell.OuterShell(outerShellInfo)
    cellCard = '2 0 -1 fill=0 imp:n=1 $Assembly'
    surfaceCard = '2 RHP 0.0 0.0 -20.0 0 0 50 0 0.2 0 $Assembly: Full Assembly Surface'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_smear():
    smearInfo = [[0, 1, 2, {'HT9': 0.5, 'LiquidNa': 0.5}, '82c', [1.0, 1.0, 1.0], 3], [0.2, 10], 'Plenum']
    c = Smear.Smear(smearInfo)
    cellCard = '1 3 0.05513 -2 u=0 imp:n=1 $Assembly: Plenum'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 10 0 0.2 0 $Assembly: Plenum'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_smear_void():
    smearInfo = [[0, 1, 2, {'HT9': 0.5, 'LiquidNa': 0.5}, '82c', [1.0, 1.0, 1.0], 3], [0.2, 10], 'Plenum']
    c = Smear.Smear(smearInfo, voidMaterial='LiquidNa', voidPercent=0.1)
    cellCard = '1 3 0.04421 -2 u=0 imp:n=1 $Assembly: Plenum'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 10 0 0.2 0 $Assembly: Plenum'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_upperCoolant():
    upperCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [0.0, 0.0, 20], 3], [10.0, 0.2]]
    c = UpperCoolant.UpperCoolant(upperCoolantInfo)
    cellCard = '1 3 0.02428 -2 u=0 imp:n=1 $Assembly: Upper Coolant'
    surfaceCard = '2 RHP 0.0 0.0 20 0 0 10.0 0 0.2 0 $Assembly: Upper Coolant'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_upperCoolant_void():
    upperCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [0.0, 0.0, 20], 3], [10.0, 0.2]]
    c = UpperCoolant.UpperCoolant(upperCoolantInfo, voidPercent=0.1)
    cellCard = '1 3 0.00243 -2 u=0 imp:n=1 $Assembly: Upper Coolant'
    surfaceCard = '2 RHP 0.0 0.0 20 0 0 10.0 0 0.2 0 $Assembly: Upper Coolant'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_coreCoolant():
    coreCoolantInfo = [[0, 10, 11, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [2, 5, [1, 2]]]
    c = CoreCoolant.CoreCoolant(coreCoolantInfo)
    cellCard = '10 3 0.02428  1 2 -11  imp:n=1 $Coolant Surrounding Assemblies'
    surfaceCard = '11 RCC 1.0 1.0 1.0 0 0 5 2 $Coolant Surrounding Assemblies'
    print(cellCard)
    print(c.cellCard)
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_coreCoolant():
    coreCoolantInfo = [[0, 10, 11, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [2, 5, [1, 2]]]
    c = CoreCoolant.CoreCoolant(coreCoolantInfo, voidPercent=0.1)
    cellCard = '10 3 0.00243  1 2 -11  imp:n=1 $Coolant Surrounding Assemblies'
    surfaceCard = '11 RCC 1.0 1.0 1.0 0 0 5 2 $Coolant Surrounding Assemblies'
    print(cellCard)
    print(c.cellCard)
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_reactorVessel():
    reactorVesselInfo = [[0, 10, 11, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [2, 5, 15]]
    c = ReactorVessel.ReactorVessel(reactorVesselInfo)
    cellCard = '10 3 0.02428  15 -11  imp:n=1 $Reactor Vessel'
    surfaceCard = '11 RCC 1.0 1.0 1.0 0 0 5 2 $Vessel surrounding the core'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard
