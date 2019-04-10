from FRIDGe.fridge.utilities import mcnpCreatorFunctions as MCF
import numpy as np


def test_getRCC():
    surfaceCard = MCF.getRCC(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    surfaceCardKnown = '1 RCC 0.0 0.0 0.55556 0 0 10 0.5 $ Comment'
    assert surfaceCard == surfaceCardKnown


def test_getRHP():
    surfaceCard = MCF.getRHP(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    surfaceCardKnown = '1 RHP 0.0 0.0 0.55556 0 0 10 0.5 0 0 $ Comment'
    assert surfaceCard == surfaceCardKnown


def test_getRHSRotated():
    surfaceCard = MCF.getRHPRotated(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    surfaceCardKnown = '1 RHP 0.0 0.0 0.55556 0 0 10 0 0.5 0 $ Comment'
    assert surfaceCard == surfaceCardKnown


def test_getSingleCell():
    cellCard = MCF.getSingleCell(1, 2, 0.06, 3, 10, '$ Comment')
    cellCardKnown = '1 2 0.06 -3 u=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getConcentricCell_Single():
    cellCard = MCF.getConcentricCell(1, 2, 0.06, 4, 3, 10, '$ Comment')
    cellCardKnown = '1 2 0.06 4 -3 u=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getConcentricCell_Multiple():
    cellCard = MCF.getConcentricCell(1, 2, 0.06, [4, 5, 6], 3, 10, '$ Comment')
    cellCardKnown = '1 2 0.06  4 5 6 -3 u=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getOutsideCell():
    cellCard = MCF.getOutsideCell(1, 2, 0.06, 3, 10, '$ Comment')
    cellCardKnown = '1 2 0.06 3 u=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getFuelLatticeCell():
    cellCard = MCF.getFuelLatticeCell(1, 2, 20, 10, '$ Comment')
    cellCardKnown = '1 0 -2 u=20 fill=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getAssemblyUniverseCell():
    cellCard = MCF.getAssemblyUniverseCell(1, 2, 10, '$ Comment')
    cellCardKnown = '1 0 -2 fill=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getEverythingElseCard():
    cellCard = MCF.getEverythingElseCard(1, 2, '$ Comment')
    cellCardKnown = '1 0 2 imp:n=0 $ Comment'
    assert cellCard == cellCardKnown


def test_getPosition_02A01():
    position = MCF.getPosition('02A01', 2, 10)
    knownAPosition = [-1.73205, 1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02B01():
    position = MCF.getPosition('02B01', 2, 10)
    knownAPosition = [0.0, 2.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)

def test_getPosition_02C01():
    position = MCF.getPosition('02C01', 2, 10)
    knownAPosition = [1.73205, 1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02D01():
    position = MCF.getPosition('02D01', 2, 10)
    knownAPosition = [1.73205, -1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02E01():
    position = MCF.getPosition('02E01', 2, 10)
    knownAPosition = [0.0, -2.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02F01():
    position = MCF.getPosition('02F01', 2, 10)
    knownAPosition = [-1.73205, -1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_01A01():
    position = MCF.getPosition('01A01', 2, 10)
    knownPosition = [0, 0, 10]
    assert position == knownPosition


def test_getPosition_03A02():
    position = MCF.getPosition('03A02', 2, 10)
    knownAPosition = [-1.73205, 3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_03B02():
    position = MCF.getPosition('03B02', 2, 10)
    knownAPosition = [1.73205, 3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_03C03():
    position = MCF.getPosition('03C02', 2, 10)
    knownAPosition = [3.46410, 0.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_D03():
    position = MCF.getPosition('03D02', 2, 10)
    knownAPosition = [1.73205, -3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_E03():
    position = MCF.getPosition('03E02', 2, 10)
    knownAPosition = [-1.73205, -3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_03F03():
    position = MCF.getPosition('03F02', 2, 10)
    knownAPosition = [-3.46410, 0.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_04B03():
    position = MCF.getPosition('04B03', 2, 10)
    knownAPosition = [3.4641, 4.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)