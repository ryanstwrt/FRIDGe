import fridge.Material.Material
import fridge.utilities.mcnpCreatorFunctions as MCF
import numpy as np

import fridge.utilities.utilities


def test_getRCC():
    surfaceCard = MCF.build_right_circular_cylinder_surface(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    surfaceCardKnown = '1 RCC 0.0 0.0 0.55556 0 0 10 0.5 $ Comment'
    assert surfaceCard == surfaceCardKnown


def test_getRHP():
    surfaceCard = MCF.build_right_hexagonal_prism_surface(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    surfaceCardKnown = '1 RHP 0.0 0.0 0.55556 0 0 10 0.5 0 0 $ Comment'
    assert surfaceCard == surfaceCardKnown


def test_getRHSRotated():
    surfaceCard = MCF.build_rotated_right_hexagonal_prism_surface(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    surfaceCardKnown = '1 RHP 0.0 0.0 0.55556 0 0 10 0 0.5 0 $ Comment'
    assert surfaceCard == surfaceCardKnown


def test_getSingleCell():
    cellCard = MCF.build_single_cell(1, 2, 0.06, 3, 10, '$ Comment')
    cellCardKnown = '1 2 0.06 -3 u=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getConcentricCell_Single():
    cellCard = MCF.build_concentric_cell(1, 2, 0.06, 4, 3, 10, '$ Comment')
    cellCardKnown = '1 2 0.06 4 -3 u=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getConcentricCell_Multiple():
    cellCard = MCF.build_concentric_cell(1, 2, 0.06, [4, 5, 6], 3, 10, '$ Comment')
    cellCardKnown = '1 2 0.06  4 5 6 -3 u=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getOutsideCell():
    cellCard = MCF.build_outside_cell(1, 2, 0.06, 3, 10, '$ Comment')
    cellCardKnown = '1 2 0.06 3 u=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getFuelLatticeCell():
    cellCard = MCF.build_fuel_lattice_cell(1, 2, 20, 10, '$ Comment')
    cellCardKnown = '1 0 -2 u=20 fill=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getAssemblyUniverseCell():
    cellCard = MCF.build_assembly_universe_cell(1, 2, 10, '$ Comment')
    cellCardKnown = '1 0 -2 fill=10 imp:n=1 $ Comment'
    assert cellCard == cellCardKnown


def test_getEverythingElseCard():
    cellCard = MCF.build_everything_else_cell(1, 2, '$ Comment')
    cellCardKnown = '1 0 2 imp:n=0 $ Comment'
    assert cellCard == cellCardKnown


def test_smearedMaterial():
    smearMaterialDict = {'LiquidNa': 0.5, 'Void': 0.5}
    smearedMaterial = fridge.Material.Material.get_smeared_material(smearMaterialDict)
    assert np.allclose(smearedMaterial.atomDensity, 0.01214, 5)
    assert smearedMaterial.name == "['LiquidNa', 'Void']"
    assert smearedMaterial.atomPercent[11023] == 1.0

def test_smearedMAterial_voided():
    smearMaterialDict = {'LiquidNa': 0.5, 'Void': 0.5}
    smearedMaterial = fridge.Material.Material.get_smeared_material(smearMaterialDict, void_material='LiquidNa', void_percent=0.1)
    assert np.allclose(smearedMaterial.atomDensity, 0.001214, 5)
    assert smearedMaterial.name == "['LiquidNa', 'Void']"
    assert smearedMaterial.atomPercent[11023] == 1.0

def test_coolantWireWrapSmear():
    info = [60, 0.53, 0.126, 2, 0.66144, 'LiquidNa', 'Void']
    smearedDict = fridge.Material.Material.smear_coolant_wirewrap(info)
    knownSmearDict = {'LiquidNa': 0.918819, 'Void': 0.081181}
    for k, v in knownSmearDict.items():
        assert np.allclose(smearedDict[k], v, 5)


def test_getPosition_02A01():
    position = fridge.utilities.utilities.getPosition('02A01', 2, 10)
    knownAPosition = [-1.73205, 1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02B01():
    position = fridge.utilities.utilities.getPosition('02B01', 2, 10)
    knownAPosition = [0.0, 2.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02C01():
    position = fridge.utilities.utilities.getPosition('02C01', 2, 10)
    knownAPosition = [1.73205, 1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02D01():
    position = fridge.utilities.utilities.getPosition('02D01', 2, 10)
    knownAPosition = [1.73205, -1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02E01():
    position = fridge.utilities.utilities.getPosition('02E01', 2, 10)
    knownAPosition = [0.0, -2.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_02F01():
    position = fridge.utilities.utilities.getPosition('02F01', 2, 10)
    knownAPosition = [-1.73205, -1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_01A01():
    position = fridge.utilities.utilities.getPosition('01A01', 2, 10)
    knownPosition = [0, 0, 10]
    assert position == knownPosition


def test_getPosition_03A02():
    position = fridge.utilities.utilities.getPosition('03A02', 2, 10)
    knownAPosition = [-1.73205, 3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_03B02():
    position = fridge.utilities.utilities.getPosition('03B02', 2, 10)
    knownAPosition = [1.73205, 3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_03C03():
    position = fridge.utilities.utilities.getPosition('03C02', 2, 10)
    knownAPosition = [3.46410, 0.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_D03():
    position = fridge.utilities.utilities.getPosition('03D02', 2, 10)
    knownAPosition = [1.73205, -3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_E03():
    position = fridge.utilities.utilities.getPosition('03E02', 2, 10)
    knownAPosition = [-1.73205, -3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_03F03():
    position = fridge.utilities.utilities.getPosition('03F02', 2, 10)
    knownAPosition = [-3.46410, 0.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getPosition_04B03():
    position = fridge.utilities.utilities.getPosition('04B03', 2, 10)
    knownAPosition = [3.4641, 4.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(knownAPosition[i], pos)


def test_getRCCVolume():
    volume = fridge.utilities.utilities.getRCCVolume(0.2, 10)
    assert np.allclose(volume, 1.25664, 5)


def test_getRHPVolume():
    volume = fridge.utilities.utilities.getRCCVolume(5, 10)
    assert np.allclose(volume, 216.506, 5)


def test_getToroidalVolume():
    volume = fridge.utilities.utilities.getToroidalVolume(0.5, 0.05, 5, 10)
    assert np.allclose(volume, 1.03631, 5)
