from FRIDGe.fridge.Constituent import Constituent
from FRIDGe.fridge.Constituent import BlankCoolant
from FRIDGe.fridge.Constituent import Duct
from FRIDGe.fridge.Constituent import EveryThingElse
from FRIDGe.fridge.Constituent import FuelBond
from FRIDGe.fridge.Constituent import FuelClad
from FRIDGe.fridge.Constituent import FuelCoolant
from FRIDGe.fridge.Constituent import FuelPin
from FRIDGe.fridge.Constituent import FuelUniverse
from FRIDGe.fridge.Constituent import InnerDuct
from FRIDGe.fridge.Constituent import LowerSodium
from FRIDGe.fridge.Constituent import OuterShell
from FRIDGe.fridge.Constituent import Smear
from FRIDGe.fridge.Constituent import UpperSodium
from FRIDGe.fridge.utilities import materialReader as mr

constituentInfo = [[0, 1, 2, 'LiquidNa', '82c', [1, 1, 1], 3], []]


def test_constituent():
    c = Constituent.Constituent(constituentInfo)
    assert c.universe == 0
    assert c.surfaceNum == 2
    assert c.cellNum == 1
    assert c.materialXCLibrary == '82c'
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
    knownMaterialCard = '\nc Material: Liquid Sodium; Density: 0.927 atoms/bn*cm \nm3 11023.82c 1.0000E+0'
    c.getMaterialCard(constituentInfo[0][3])
    assert sodium.name == c.material.name
    assert knownMaterialCard == c.materialCard


def test_blankCoolant():
    blankCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = BlankCoolant.BlankCoolant(blankCoolantInfo)
    cellCard = '1 3 0.927 -4 u=0 imp:n=1 $Pin: Blank Pin Coolant'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.202 0 0.05 0 $Pin: Blank Pin - 1% higher than fuel'
    assert c.pitch == 0.1 / 2
    assert c.height == 0.2 * 1.01
    assert c.blankCoolantSurfaceNum == 4
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_duct():
    ductInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = Duct.Duct(ductInfo)
    cellCard = '1 3 0.927 4 -2 u=0 imp:n=1 $Assembly: Assembly Duct'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.2 0.1 0 0 $Assembly:Duct Outer Surface'
    assert c.flat2flat == 0.1
    assert c.height == 0.20
    assert c.innerSurfaceNum == 4
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_EverythingElse():
    everyThingElseInfo = [1, 2]
    c = EveryThingElse.EveryThingElse(everyThingElseInfo)
    cellCard = '1 0 2 imp:n=0 $Assembly: Outside Assembly'
    assert c.assemblySurfaceNum == 2
    assert cellCard == c.cellCard


def test_fuelBond():
    fuelBondInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = FuelBond.FuelBond(fuelBondInfo)
    cellCard = '1 3 0.927 4 -2 u=0 imp:n=1 $Pin: Bond'
    surfaceCard = '2 RCC 1.0 1.0 1.0 0 0 0.202 0.05 $Pin: Bond - 1% higher than fuel'
    assert c.radius == 0.1 / 2
    assert c.height == 0.2 * 1.01
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelClad():
    fuelCladInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = FuelClad.FuelClad(fuelCladInfo)
    cellCard = '1 3 0.927 4 -2 u=0 imp:n=1 $Pin: Clad'
    surfaceCard = '2 RCC 1.0 1.0 1.0 0 0 0.202 0.05 $Pin: Clad - 1% higher than fuel'
    assert c.radius == 0.1 / 2
    assert c.height == 0.2 * 1.01
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelCoolant():
    fuelCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 4]]
    c = FuelCoolant.FuelCoolant(fuelCoolantInfo)
    cellCard = '1 3 0.927 4 u=0 imp:n=1 $Pin: Wirewrap + Coolant'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.202 0 0.1 0 $Pin: Coolant - 1% higher than fuel'
    assert c.pitch == 0.1
    assert c.height == 0.2 * 1.01
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelPin():
    fuelPinInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2]]
    c = FuelPin.FuelPin(fuelPinInfo)
    cellCard = '1 3 0.927 -2 u=0 imp:n=1 $Pin: Fuel'
    surfaceCard = '2 RCC 1.0 1.0 1.0 0 0 0.2 0.05 $Pin: Fuel'
    assert c.radius == 0.1 / 2
    assert c.height == 0.2
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard


def test_fuelUniverse():
    fuelUniverseInfo = [1, 2, 7, 3, 4, 5]
    c = FuelUniverse.FuelUniverse(fuelUniverseInfo)
    cellCard = '3 0 -4 lat=2 u=5 imp:n=1\n     fill=-2:2 -2:2 0:0\n      ' \
               '2 2 2 2 2 2 2 1 1 2 2 1 1 1 2 2 1 1 2 2 2 2 2 2 2'
    assert cellCard == c.cellCard


def test_innerDuct():
    innerDuctInfo = [[0, 1, 2, 'HT9', '82c', [1.0, 1.0, 1.0], 3], [4, 5, 0.1, 0.2]]
    c = InnerDuct.InnerDuct(innerDuctInfo)
    cellCard = '1 0 -2 u=4 fill=5 imp:n=1 $Assembly: Inner Portion of Assembly'
    surfaceCard = '2 RHP 1.0 1.0 1.0 0 0 0.202 0.1 0 0 $Assembly: Duct Inner Surface'
    assert c.assemblyUniverse == 4
    assert c.latticeUniverse == 5
    assert c.flat2flat == 0.1
    assert c.height == 0.2 * 1.01
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_lowerSodium():
    outerShellInfo = [[0, 1, 2, 'HT9', '82c', [], 3], [10, 10, 10, 50, 0.2, '01A01']]
    assemblyShell = OuterShell.OuterShell(outerShellInfo)
    lowerSodiumInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [assemblyShell, 0.2]]
    c = LowerSodium.LowerSodium(lowerSodiumInfo)
    cellCard = '1 3 0.927 -2 u=0 imp:n=1 $Assembly: Lower Sodium'
    surfaceCard = '2 RHP 0.0 0.0 -14.95 0 0 4.95 0.2 0 0 $Assembly: Lower Sodium'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_outershell():
    outerShellInfo = [[0, 1, 2, 'LiquidNa', '82c', [], 3], [10, 10, 10, 50, 0.2, '01A01']]
    c = OuterShell.OuterShell(outerShellInfo)
    cellCard = '2 0 -1 fill=0 imp:n=1 $Assembly'
    surfaceCard = '2 RHP 0.0 0.0 -14.95 0 0 50 0.2 0 0 $Assembly: Full Assembly Surface'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_smear():
    smearInfo = [[0, 1, 2, {'HT9': 0.5, 'LiquidNa': 0.5}, '82c', [1.0, 1.0, 1.0], 3], [0.2, 10], 'Plenum']
    c = Smear.Smear(smearInfo)
    cellCard = '2 3 0.05514 -1 u=0 imp:n=1 $Assembly: Plenum'
    surfaceCard = '1 RHP 1.0 1.0 1.0 0 0 10 0.2 0 0 $Assembly: Plenum'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard


def test_upperSodium():
    outerShellInfo = [[0, 1, 2, 'HT9', '82c', [], 3], [10, 10, 10, 50, 0.2, '01A01']]
    assemblyShell = OuterShell.OuterShell(outerShellInfo)
    upperSodiumInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [assemblyShell, 0.2]]
    c = UpperSodium.UpperSodium(upperSodiumInfo)
    cellCard = '1 3 0.927 -2 u=0 imp:n=1 $Assembly: Upper Sodium'
    surfaceCard = '2 RHP 0.0 0.0 30.1 0 0 4.95 0.2 0 0 $Assembly: Upper Sodium'
    assert c.cellCard == cellCard
    assert c.surfaceCard == surfaceCard
