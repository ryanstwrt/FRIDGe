import fridge.Material.Material
import fridge.utilities.mcnpCreatorFunctions as MCF
import numpy as np

import fridge.utilities.utilities


def test_get_rcc():
    surface_card = MCF.build_right_circular_cylinder_surface(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    test_surface_card = '1 RCC 0.0 0.0 0.55556 0 0 10 0.5 $ Comment'
    assert surface_card == test_surface_card


def test_get_rhp():
    surface_card = MCF.build_right_hexagonal_prism_surface(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    test_surface_card = '1 RHP 0.0 0.0 0.55556 0 0 10 0.5 0 0 $ Comment'
    assert surface_card == test_surface_card


def test_get_rhs_rotated():
    surface_card = MCF.build_rotated_right_hexagonal_prism_surface(0.5, 10, [0.0, 0.0, 0.5555555], 1, '$ Comment')
    test_surface_card = '1 RHP 0.0 0.0 0.55556 0 0 10 0 0.5 0 $ Comment'
    assert surface_card == test_surface_card


def test_get_singel_cell():
    cell_card = MCF.build_single_cell(1, 2, 0.06, 3, 10, '$ Comment')
    test_cell_card = '1 2 0.06 -3 u=10 imp:n=1 $ Comment'
    assert cell_card == test_cell_card
    
    
def test_get_singel_cell_volume():
    cell_card = MCF.build_single_cell(1, 2, 0.06, 3, 10, '$ Comment', volume=10)
    test_cell_card = '1 2 0.06 -3 u=10 vol=10 imp:n=1 $ Comment'
    assert cell_card == test_cell_card


def test_get_concentric_cell_single():
    cell_card = MCF.build_concentric_cell(1, 2, 0.06, 4, 3, 10, '$ Comment')
    test_cell_card = '1 2 0.06 4 -3 u=10 imp:n=1 $ Comment'
    assert cell_card == test_cell_card


def test_get_concentric_cell_multiple():
    cell_card = MCF.build_concentric_cell(1, 2, 0.06, [4, 5, 6], 3, 10, '$ Comment')
    test_cell_card = '1 2 0.06  4 5 6 -3 u=10 imp:n=1 $ Comment'
    assert cell_card == test_cell_card


def test_get_outside_cell():
    cell_card = MCF.build_outside_cell(1, 2, 0.06, 3, 10, '$ Comment')
    test_cell_card = '1 2 0.06 3 u=10 imp:n=1 $ Comment'
    assert cell_card == test_cell_card


def test_get_fuel_lattice_cell():
    cell_card = MCF.build_fuel_lattice_cell(1, 2, 20, 10, '$ Comment')
    test_cell_card = '1 0 -2 u=20 fill=10 imp:n=1 $ Comment'
    assert cell_card == test_cell_card


def test_get_assembly_universe_cell():
    cell_card = MCF.build_assembly_universe_cell(1, 2, 10, '$ Comment')
    test_cell_card = '1 0 -2 fill=10 imp:n=1 $ Comment'
    assert cell_card == test_cell_card


def test_get_everything_else_card():
    cell_card = MCF.build_everything_else_cell(1, 2, '$ Comment')
    test_cell_card = '1 0 2 imp:n=0 $ Comment'
    assert cell_card == test_cell_card


def test_smeared_material():
    smear_mat_dict = {'LiquidNa': 0.5, 'Void': 0.5}
    smeared_material = fridge.Material.Material.get_smeared_material(smear_mat_dict)
    assert np.allclose(smeared_material.atomDensity, 0.01214, 5)
    assert smeared_material.name == "['LiquidNa', 'Void']"
    assert smeared_material.atomPercent[11023] == 1.0


def test_smeared_material_voided():
    smear_mat_dict = {'LiquidNa': 0.5, 'Void': 0.5}
    smeared_material = fridge.Material.Material.get_smeared_material(smear_mat_dict, void_material='LiquidNa',
                                                                     void_percent=0.1)
    assert np.allclose(smeared_material.atomDensity, 0.001214, 5)
    assert smeared_material.name == "['LiquidNa', 'Void']"
    assert smeared_material.atomPercent[11023] == 1.0


def test_coolant_wire_wrap_smear():
    info = [60, 0.53, 0.126, 2, 0.66144, 'LiquidNa', 'Void']
    smear_mat_dict = fridge.Material.Material.smear_coolant_wirewrap(info)
    smeared_material = {'LiquidNa': 0.918819, 'Void': 0.081181}
    for k, v in smeared_material.items():
        assert np.allclose(smear_mat_dict[k], v, 5)


def test_get_position_02a01():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('02A01', 2, 10)
    assem_position = [-1.73205, 1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_02b01():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('02B01', 2, 10)
    assem_position = [0.0, 2.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_02c01():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('02C01', 2, 10)
    assem_position = [1.73205, 1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_02d01():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('02D01', 2, 10)
    assem_position = [1.73205, -1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_02e01():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('02E01', 2, 10)
    assem_position = [0.0, -2.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_02f01():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('02F01', 2, 10)
    assem_position = [-1.73205, -1.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_01a01():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('01A01', 2, 10)
    assem_position = [0, 0, 10]
    assert position == assem_position


def test_get_position_03a02():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('03A02', 2, 10)
    assem_position = [-1.73205, 3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_03b02():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('03B02', 2, 10)
    assem_position = [1.73205, 3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_03c03():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('03C02', 2, 10)
    assem_position = [3.46410, 0.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_03d03():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('03D02', 2, 10)
    assem_position = [1.73205, -3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_03e03():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('03E02', 2, 10)
    assem_position = [-1.73205, -3.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_03f03():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('03F02', 2, 10)
    assem_position = [-3.46410, 0.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_position_04b03():
    position = fridge.utilities.utilities.get_position_for_hex_lattice('04B03', 2, 10)
    assem_position = [3.4641, 4.0, 10]
    for i, pos in enumerate(position):
        assert np.allclose(assem_position[i], pos)


def test_get_rcc_volume():
    volume = fridge.utilities.utilities.get_cylinder_volume(0.2, 10)
    assert np.allclose(volume, 1.25664, 5)


def test_get_rhp__volume():
    volume = fridge.utilities.utilities.get_cylinder_volume(5, 10)
    assert np.allclose(volume, 216.506, 5)


def test_get_toroidal_volume():
    volume = fridge.utilities.utilities.get_toroidal_volume(0.5, 0.05, 5, 10)
    assert np.allclose(volume, 1.03631, 5)
