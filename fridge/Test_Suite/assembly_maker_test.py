from FRIDGe.fridge.input_readers import material_reader as mat_read
from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import assembly_maker as pm

assembly_type = 'A271'

fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)

# Potentially throw these three functions into the assembly holder and unpack them when they are needed.
fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])


def test_mcnp_macro_RCC():
    """Make a right circular cylinder surface"""
    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    surface_number_test = fuel_assembly.surface_number
    output, warning = pm.mcnp_make_macro_RCC(fuel_assembly, [0, 0, 0], [0, 0, 10], 0.5, 'Testing to make sure')
    assert surface_number_test + 1 == fuel_assembly.surface_number
    assert len(output) < 80
    assert warning == False
    output, warning = pm.mcnp_make_macro_RCC(fuel_assembly, [0,0,0], [0,0,10], 0.5, 'Testing to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_macro_RHP():
    """Make a right hexagonal prism surface"""
    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    surface_number_test = fuel_assembly.surface_number
    output, warning = pm.mcnp_make_macro_RHP(fuel_assembly, [0,0,0], [0,0,10], [0, 0.5, 0], 'Testing to make sure')
    assert surface_number_test + 1 == fuel_assembly.surface_number
    assert len(output) < 80
    assert warning == False
    output, warning = pm.mcnp_make_macro_RHP(fuel_assembly, [0,0,0], [0,0,10], [0, 0.5, 0], 'Testing to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_make_concentric_cell():
    """Make an MCNP surface with two concentric surfaces"""
    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    cell_number_test = fuel_assembly.cell_number
    output, warning = pm.mcnp_make_concentric_cell(fuel_assembly, 10, 0.95, 10, 11, 1, 1, 'Test to make sure')
    assert cell_number_test + 1 == fuel_assembly.cell_number
    assert len(output) < 80
    assert warning == False

    output, warning = pm.mcnp_make_concentric_cell(fuel_assembly, 10, 0.95, 10, 11, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_make_cell():
    """Test the ability to make an MCNP cell with only one surface"""
    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    cell_number_test = fuel_assembly.cell_number
    output, warning = pm.mcnp_make_cell(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure')
    assert cell_number_test + 1 == fuel_assembly.cell_number
    assert len(output) < 80
    assert warning == False

    output, warning = pm.mcnp_make_cell(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True

def test_mcnp_make_cell_outside():
    """Test the ability to make an MCNP cell with only one surface"""
    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    cell_number_test = fuel_assembly.cell_number
    output, warning = pm.mcnp_make_cell_outside(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure')
    assert cell_number_test + 1 == fuel_assembly.cell_number
    assert len(output) < 80
    assert warning == False

    output, warning = pm.mcnp_make_cell(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_lattice_maker():
    """Test of the lattice maker for MCNP"""
    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    output = pm.make_lattice(fuel_assembly)



def test_pin_maker():
    """Test of the pin maker function"""
    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    pm.fuel_pin_maker(fuel_assembly)

    assert fuel_assembly.pin.fuel_material[1] == fuel_material_fuel[1]
    assert fuel_assembly.pin.fuel_bond[1] == fuel_material_bond[1]
    assert fuel_assembly.pin.fuel_clad[1] == fuel_material_cladding[1]
    assert fuel_assembly.pin.fuel_pellet_surface == 1000
    assert fuel_assembly.pin.fuel_pellet_mcnp_surface == "1000 RCC  0 0 50   0 0   60.0   0.197454   $Pin: Fuel pellet outer radius"
    assert fuel_assembly.pin.fuel_bond_surface == 1001
    assert fuel_assembly.pin.fuel_bond_mcnp_surface == "1001 RCC  0 0 50   0 0   60.0   0.228   $Pin: Na bond outer radius"
    assert fuel_assembly.pin.fuel_clad_surface == 1002
    assert fuel_assembly.pin.fuel_clad_mcnp_surface == "1002 RCC  0 0 50   0 0   60.0   0.265   $Pin: Cladding outer radius"
    assert fuel_assembly.pin.fuel_pin_universe_surface == 1003
    assert fuel_assembly.pin.fuel_pin_universe_mcnp_surface == "1003 RHP  0 0 50   0 0 60.0   1.0 0 0   $$ Pin: Na universe for fuel pin"
    assert fuel_assembly.pin.fuel_pellet_cell == 1050
    assert fuel_assembly.pin.fuel_pellet_mcnp_cell == "1050 1022 0.0481048   -1000      u=1001 imp:n=1 $Pin: Fuel Pellet"
    assert fuel_assembly.pin.fuel_bond_cell == 1051
    assert fuel_assembly.pin.fuel_bond_mcnp_cell == "1051 1023 0.0242826   1000 -1001      u=1001 imp:n=1 $Pin: Na Bond"
    assert fuel_assembly.pin.fuel_clad_cell == 1052
    assert fuel_assembly.pin.fuel_clad_mcnp_cell == "1052 1024 0.0859836   1001 -1002      u=1001 imp:n=1 $Pin: Pin Cladding"
    assert fuel_assembly.pin.fuel_universe_cell == 1053
    assert fuel_assembly.pin.fuel_universe_mcnp_cell == "1053 1025 0.94   1002      u=1001 imp:n=1 $Pin: Wirewrap + Na coolant"
    assert fuel_assembly.pin.na_cell_universe == 1002
    assert fuel_assembly.pin.na_cell == 1054
    assert fuel_assembly.pin.na_mcnp_cell == "1054 1025 0.94   -1003      u=1002 imp:n=1 $Pin: Na Pin"



def test_assembly_maker():
    """Test of the assembly maker function"""
    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    pm.assembly_maker(fuel_assembly)
    assert fuel_assembly.lower_reflector_surface == 1000
    assert fuel_assembly.lower_reflector_mcnp_surface == "1000 RHP  0 0 0   0 0 50.0   0 5.55 0   $Assembly: Lower Reflector"
    assert fuel_assembly.plenum_surface == 1001
    assert fuel_assembly.plenum_mcnp_surface == "1001 RHP  0 0 110.0   0 0 60.0   0 5.55 0   $Assembly: Plenum"
    assert fuel_assembly.upper_reflector_surface == 1002
    assert fuel_assembly.upper_reflector_mcnp_surface == "1002 RHP  0 0 170.0   0 0 50.0   0 5.55 0   $Assembly: Upper Reflector"
    assert fuel_assembly.inner_duct_surface == 1003
    assert fuel_assembly.inner_duct_mcnp_surface == "1003 RHP  0 0 50.0   0 0 60.0   0 5.55 0   $Assembly: Inner Duct (fuel portion)"
    assert fuel_assembly.outer_duct_surface == 1004
    assert fuel_assembly.outer_duct_mcnp_surface == "1004 RHP  0 0 -1   0 0 322.0   0 5.55 0   $Assembly: Outerduct/Universe"
    assert fuel_assembly.universe_surface == 1005
    assert fuel_assembly.universe_mcnp_surface == "*1005 RHP  0 0 -0.45   0 0 321.6   0 5.55 0   $Assembly: Sodium universe"




test_mcnp_macro_RCC()
test_mcnp_macro_RHP()
test_mcnp_make_cell()
test_mcnp_make_concentric_cell()
test_assembly_maker()



