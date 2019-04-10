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
