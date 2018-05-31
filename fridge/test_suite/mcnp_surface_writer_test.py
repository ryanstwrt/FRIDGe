import FRIDGe.fridge
from FRIDGe.fridge.utilities import geometry_reader as geo_read, material_reader as mat_read
from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import global_variables as gb

assembly_type = 'A271_Assembly'
global_vars = gb.global_variables(assembly_type)
fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(global_vars.assembly_type)

# Potentially throw these three functions into the assembly holder and unpack them when they are needed.
fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])

def test_mcnp_macro_RCC():
    """Make a right circular cylinder surface"""
    fuel_assembly = ah.Assembly(global_vars.assembly_type, 1000, global_vars)

    surface_number_test = fuel_assembly.surface_number
    output, warning = FRIDGe.fridge.utilities.mcnp_surface_writer.mcnp_make_macro_RCC(fuel_assembly, [0, 0, 0], [0, 0, 10], 0.5, 'Testing to make sure')
    assert surface_number_test + 1 == fuel_assembly.surface_number
    assert len(output) < 80
    assert warning == False
    output, warning = FRIDGe.fridge.utilities.mcnp_surface_writer.mcnp_make_macro_RCC(fuel_assembly, [0, 0, 0], [0, 0, 10], 0.5, 'Testing to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_macro_RHP():
    """Make a right hexagonal prism surface"""
    fuel_assembly = ah.Assembly(global_vars.assembly_type, 1000, global_vars)

    surface_number_test = fuel_assembly.surface_number
    output, warning = FRIDGe.fridge.utilities.mcnp_surface_writer.mcnp_make_macro_RHP(fuel_assembly, [0, 0, 0], [0, 0, 10], [0, 0.5, 0], 'Testing to make sure')
    assert surface_number_test + 1 == fuel_assembly.surface_number
    assert len(output) < 80
    assert warning == False
    output, warning = FRIDGe.fridge.utilities.mcnp_surface_writer.mcnp_make_macro_RHP(fuel_assembly, [0, 0, 0], [0, 0, 10], [0, 0.5, 0], 'Testing to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True