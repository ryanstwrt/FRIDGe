from FRIDGe.fridge.Constituent import Constituent
from FRIDGe.fridge.Constituent import BlankCoolant
from FRIDGe.fridge.utilities import materialReader as mr

constituentInfo = [[0, 1, 2, 'LiquidNa', '82c', [1, 1, 1], 3], []]


def test_constituent():
    c = Constituent.Constituent(constituentInfo)
    assert c.universe == 0
    assert c.surfaceNum == 1
    assert c.cellNum == 2
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
    blankCoolantInfo = [[0, 1, 2, 'LiquidNa', '82c', [1.0, 1.0, 1.0], 3], [0.1, 0.2, 3]]
    c = BlankCoolant.BlankCoolant(blankCoolantInfo)
    cellCard = '2 3 0.927 -3 u=0 imp:n=1  $Pin: Blank Pin Coolant'
    surfaceCard = '1 RHP 1.0 1.0 1.0 0 0 0.202 0 0.05 0 $Pin: Blank Pin - 1% higher than fuel'
    assert c.pitch == 0.1 / 2
    assert c.height == 0.2 * 1.01
    assert c.blankCoolantSurfaceNum == 3
    assert cellCard == c.cellCard
    assert surfaceCard == c.surfaceCard
