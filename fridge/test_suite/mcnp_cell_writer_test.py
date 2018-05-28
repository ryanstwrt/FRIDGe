import FRIDGe.fridge
from FRIDGe.fridge.driver import assembly_holder as ah, assembly_maker as pm
from FRIDGe.fridge.utilities import geometry_reader as geo_read, material_reader as mat_read

assembly_type = 'A271_test'

fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)

# Potentially throw these three functions into the assembly holder and unpack them when they are needed.
fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])

def test_mcnp_make_concentric_cell():
    """Make an MCNP surface with two concentric surfaces"""
    fuel_assembly = ah.Assembly(assembly_type, 1000)

    cell_number_test = fuel_assembly.cell_number
    output, warning = FRIDGe.fridge.utilities.mcnp_cell_writer.mcnp_make_concentric_cell(fuel_assembly, 10, 0.95, 10, 11, 1, 1, 'Test to make sure')
    assert cell_number_test + 1 == fuel_assembly.cell_number
    assert len(output) < 80
    assert warning == False

    output, warning = FRIDGe.fridge.utilities.mcnp_cell_writer.mcnp_make_concentric_cell(fuel_assembly, 10, 0.95, 10, 11, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_make_cell():
    """Test the ability to make an MCNP cell with only one surface"""
    fuel_assembly = ah.Assembly(assembly_type, 1000)

    cell_number_test = fuel_assembly.cell_number
    output, warning = FRIDGe.fridge.utilities.mcnp_cell_writer.mcnp_make_cell(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure')
    assert cell_number_test + 1 == fuel_assembly.cell_number
    assert len(output) < 80
    assert warning == False

    output, warning = FRIDGe.fridge.utilities.mcnp_cell_writer.mcnp_make_cell(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_make_cell_outside():
    """Test the ability to make an MCNP cell with only one surface"""
    fuel_assembly = ah.Assembly(assembly_type, 1000)

    cell_number_test = fuel_assembly.cell_number
    output, warning = FRIDGe.fridge.utilities.mcnp_cell_writer.mcnp_make_cell_outside(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure')
    assert cell_number_test + 1 == fuel_assembly.cell_number
    assert len(output) < 80
    assert warning == False

    output, warning = FRIDGe.fridge.utilities.mcnp_cell_writer.mcnp_make_cell(fuel_assembly, 10, 0.95, 10, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_lattice_maker():
    """Test of the lattice maker for MCNP"""
    fuel_assembly = ah.Assembly(assembly_type, 1000)
    fuel_assembly.assembly_data.ix['pins_per_assembly', 'assembly'] = 11
    pm.assembly_maker(fuel_assembly)
    output = fuel_assembly.lattice_mcnp_cell
    test_output = "1058 0      -1009 lat=2 u=1003 imp:n=1 \n\
      fill=-3:3 -3:3 0:0 \n\
      1002 1002 1002 1002 1002 1002 1002 1002 1002 1002\n\
      1001 1001 1001 1002 1002 1002 1001 1001 1001 1001\n\
      1002 1002 1001 1001 1001 1001 1001 1002 1001 1001\n\
      1001 1001 1001 1001 1002 1001 1001 1001 1001 1001\n\
      1001 1002 1002 1002 1002 1002 1002 1002 1002\n"

    assert output == test_output


def test_mcnp_make_lattice_holder():
    """Test the MCNP lattice holder function"""
    fuel_assembly = ah.Assembly(assembly_type, 1000)
    fuel_assembly.assembly_data.ix['pins_per_assembly', 'assembly'] = 37
    pm.assembly_maker(fuel_assembly)
    output = fuel_assembly.lattice_holder_mcnp_cell
    test_output = "1059 0 -1003    u=1000 fill=1003 imp:n=1 $ Assembly: Base Assembly\n\
1060 1052 0.0859836   -1004 1000 1001 1002 1003 u=1000   imp:n=1   $ Driver: Hex Duct\n\
1061 0   -1005 1011 -1012   fill=1000   imp:n=1   $ Assembly: Full Assembly\n"
    assert test_output == output


def test_make_mcnp_void_cell():
    fuel_assembly = ah.Assembly(assembly_type, 1000)
    pm.assembly_maker(fuel_assembly)
    output = fuel_assembly.void_mcnp_cell
    test_output = "1062 0    #1061   imp:n=0   $ Void\n"
    assert test_output == output