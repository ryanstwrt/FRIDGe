from FRIDGe.fridge.utilities import geometry_reader as geo_read, material_reader as mat_read
from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import assembly_maker as pm
from FRIDGe.fridge.driver import global_variables as gb

assembly_type = 'A271_Assembly_Test'
global_vars = gb.global_variables(assembly_type)

fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(global_vars.assembly_type)

# Potentially throw these three functions into the assembly holder and unpack them when they are needed.
fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])


def test_pin_maker():
    """Test of the pin maker function"""
    fuel_assembly = ah.FuelAssembly(global_vars, global_vars.assembly_type)

    fuel_assembly.material.fuel_num = 1022
    fuel_assembly.material.bond_num = 1023
    fuel_assembly.material.clad_num = 1024

    pm.assembly_maker(fuel_assembly)

    assert fuel_assembly.pin.fuel_material[1] == fuel_material_fuel[1]
    assert fuel_assembly.pin.fuel_bond[1] == fuel_material_bond[1]
    assert fuel_assembly.pin.fuel_clad[1] == fuel_material_cladding[1]
    assert fuel_assembly.pin.fuel_pellet_surface == 1006
    assert fuel_assembly.pin.fuel_pellet_mcnp_surface == "1006 RCC  0 0 50   0 0   60.0   0.197454   $Pin: Fuel pellet outer radius\n"
    assert fuel_assembly.pin.fuel_bond_surface == 1007
    assert fuel_assembly.pin.fuel_bond_mcnp_surface == "1007 RCC  0 0 50   0 0   60.0   0.228   $Pin: Na bond outer radius\n"
    assert fuel_assembly.pin.fuel_clad_surface == 1008
    assert fuel_assembly.pin.fuel_clad_mcnp_surface == "1008 RCC  0 0 50   0 0   60.0   0.265   $Pin: Cladding outer radius\n"
    assert fuel_assembly.pin.fuel_pin_universe_surface == 1009
    assert fuel_assembly.pin.fuel_pin_universe_mcnp_surface == "1009 RHP  0 0 50   0 0 60.0   0.3305 0 0   $$ Pin: Na universe for fuel pin\n"
    assert fuel_assembly.pin.fuel_pellet_cell == 1050
    assert fuel_assembly.pin.fuel_pellet_mcnp_cell == "1050 1050 0.0481048   -1006      u=1001 imp:n=1 $Pin: Fuel Pellet\n"
    assert fuel_assembly.pin.fuel_bond_cell == 1051
    assert fuel_assembly.pin.fuel_bond_mcnp_cell == "1051 1051 0.0242826   1006 -1007      u=1001 imp:n=1 $Pin: Na Bond\n"
    assert fuel_assembly.pin.fuel_clad_cell == 1052
    assert fuel_assembly.pin.fuel_clad_mcnp_cell == "1052 1052 0.0859836   1007 -1008      u=1001 imp:n=1 $Pin: Pin Cladding\n"
    assert fuel_assembly.pin.fuel_universe_cell == 1053
    assert fuel_assembly.pin.fuel_universe_mcnp_cell == "1053 1053 0.0364616   1008      u=1001 imp:n=1 $Pin: Wirewrap + Na coolant\n"
    assert fuel_assembly.pin.na_cell_universe == 1002
    assert fuel_assembly.pin.na_cell == 1054
    assert fuel_assembly.pin.na_mcnp_cell == "1054 1051 0.0242826   -1010      u=1002 imp:n=1 $Pin: Na Pin\n"


def test_assembly_maker():
    """Test of the assembly maker function"""
    fuel_assembly = ah.FuelAssembly(global_vars, global_vars.assembly_type)

    pm.assembly_maker(fuel_assembly)
    assert fuel_assembly.lower_reflector_surface == 1000
    assert fuel_assembly.lower_reflector_mcnp_surface == "1000 RHP  0 0 0   0 0 50.0   0 5.55 0   $FuelAssembly: Lower Reflector\n"
    assert fuel_assembly.plenum_surface == 1001
    assert fuel_assembly.plenum_mcnp_surface == "1001 RHP  0 0 110.0   0 0 60.0   0 5.55 0   $FuelAssembly: Plenum\n"
    assert fuel_assembly.upper_reflector_surface == 1002
    assert fuel_assembly.upper_reflector_mcnp_surface == "1002 RHP  0 0 170.0   0 0 50.0   0 5.55 0   $FuelAssembly: Upper Reflector\n"
    assert fuel_assembly.inner_duct_surface == 1003
    assert fuel_assembly.inner_duct_mcnp_surface == "1003 RHP  0 0 50.0   0 0 60.0   0 5.55 0   $FuelAssembly: Inner Duct (fuel portion)\n"
    assert fuel_assembly.outer_duct_surface == 1004
    assert fuel_assembly.outer_duct_mcnp_surface == "1004 RHP  0 0 -1   0 0 322.0   0 6.0 0   $FuelAssembly: Outerduct/Universe\n"
    assert fuel_assembly.universe_surface == 1005
    assert fuel_assembly.universe_mcnp_surface == "*1005 RHP  0 0 -0.45   0 0 321.6   0 5.85 0   $FuelAssembly: Sodium universe\n"
