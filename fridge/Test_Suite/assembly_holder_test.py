from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.input_readers import material_reader as mat_read

def test_assembly():
    """ Test the creation of the assembly class"""
    assembly_type = 'A271'
    fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)

    fuel_assembly = ah.Assembly(assembly, 'fuel')

    assert fuel_assembly.assembly_data.all == assembly.all
    assert fuel_assembly.assembly_type == 'fuel'


def test_pin():
    """ Test the creation of the pin class"""
    assembly_type = 'A271'
    fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)
    fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
    fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
    fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])

    fuel_pin = ah.FuelPin(fuel, fuel_material_fuel, fuel_material_bond, fuel_material_cladding)

    assert fuel_pin.pin_data.all == fuel.all
    assert fuel_pin.fuel_material == fuel_material_fuel
    assert fuel_pin.fuel_bond == fuel_material_bond
    assert fuel_pin.fuel_clad == fuel_material_cladding


test_assembly()
test_pin()