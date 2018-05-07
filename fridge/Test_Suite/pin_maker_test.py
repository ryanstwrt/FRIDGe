from FRIDGe.fridge.input_readers import material_reader as mat_read
from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import pin_maker as pm

assembly_type = 'A271'

fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)

# Potentially throw these three functions into the assembly holder and unpack them when they are needed.
fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])



def test_mcnp_macro_RCC():
    fuel_assembly = ah.Assembly(assembly, 'fuel',
                                [fuel, fuel_material_fuel, fuel_material_bond, fuel_material_cladding], 1000)

    surface_number_test = fuel_assembly.surface_number
    output, warning = pm.mcnp_make_macro_RCC(fuel_assembly, [0, 0, 0], [0, 0, 10], 0.5, 'Testing to make sure')
    assert surface_number_test + 1 == fuel_assembly.surface_number
    assert len(output) < 80
    assert warning == False
    output, warning = pm.mcnp_make_macro_RCC(fuel_assembly, [0,0,0], [0,0,10], 0.5, 'Testing to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_macro_RHP():
    fuel_assembly = ah.Assembly(assembly, 'fuel',
                                [fuel, fuel_material_fuel, fuel_material_bond, fuel_material_cladding], 1000)

    surface_number_test = fuel_assembly.surface_number
    output, warning = pm.mcnp_make_macro_RCC(fuel_assembly, [0,0,0], [0,0,10], [0, 0.5, 0], 'Testing to make sure')
    assert surface_number_test + 1 == fuel_assembly.surface_number
    assert len(output) < 80
    assert warning == False
    output, warning = pm.mcnp_make_macro_RCC(fuel_assembly, [0,0,0], [0,0,10], [0, 0.5, 0], 'Testing to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_make_concentric_cell():
    fuel_assembly = ah.Assembly(assembly, 'fuel',
                                [fuel, fuel_material_fuel, fuel_material_bond, fuel_material_cladding], 1000)

    cell_number_test = fuel_assembly.cell_number
    output, warning = pm.mcnp_make_concentric_cell(fuel_assembly, 10, 0.95, 10, 11, 1, 1, 'Test to make sure')
    assert cell_number_test + 1 == fuel_assembly.cell_number
    assert len(output) < 80
    assert warning == False

    output, warning = pm.mcnp_make_concentric_cell(fuel_assembly, 10, 0.95, 10, 11, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_make_cell():
    fuel_assembly = ah.Assembly(assembly, 'fuel',
                                [fuel, fuel_material_fuel, fuel_material_bond, fuel_material_cladding], 1000)

    cell_number_test = fuel_assembly.cell_number
    output, warning = pm.mcnp_make_cell(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure')
    assert cell_number_test + 1 == fuel_assembly.cell_number
    assert len(output) < 80
    assert warning == False

    output, warning = pm.mcnp_make_cell(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_pin_maker():
    fuel_assembly = ah.Assembly(assembly, 'fuel',
                                [fuel, fuel_material_fuel, fuel_material_bond, fuel_material_cladding], 1000)

    fp = pm.fuel_pin_maker(fuel_assembly)

    assert fuel_assembly.pin.fuel_material == fuel_material_fuel
    assert fuel_assembly.pin.fuel_bond == fuel_material_bond
    assert fuel_assembly.pin.fuel_clad == fuel_material_cladding
    assert fuel_assembly.pin.fuel_pellet_surface == 1000
    assert fuel_assembly.pin.fuel_bond_surface == 1001
    assert fuel_assembly.pin.fuel_clad_surface == 1002
    assert fuel_assembly.pin.fuel_pin_universe_surface == 1003
    assert fuel_assembly.pin.fuel_pellet_cell == 1050
    assert fuel_assembly.pin.fuel_bond_cell == 1051
    assert fuel_assembly.pin.fuel_clad_cell == 1052
    assert fuel_assembly.pin.fuel_universe_cell == 1053




test_mcnp_macro_RCC()
test_mcnp_macro_RHP()
test_mcnp_make_cell()
test_mcnp_make_concentric_cell()