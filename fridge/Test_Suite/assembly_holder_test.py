from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.input_readers import material_reader as mat_read

def test_assembly():
    """ Test the creation of the assembly class with a fueled assembly"""
    assembly_type = 'A271'
    fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)
    fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
    fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
    fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])
    universe = 1000

    fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 1000)

    assert fuel_assembly.assembly_data.all == assembly.all
    assert fuel_assembly.assembly_universe == universe
    assert fuel_assembly.surface_number == universe
    assert fuel_assembly.cell_number == universe + 50
    assert fuel_assembly.pin.pin_data.all == fuel.all
    assert fuel_assembly.universe_counter == universe

    ah.FuelPin(fuel)

    assert fuel_assembly.fuel_id == universe + 22
    assert fuel_assembly.bond_id == universe + 23
    assert fuel_assembly.clad_id == universe + 24
    assert fuel_assembly.coolant_id == universe + 25
    assert fuel_assembly.assembly_id == universe + 20
    assert fuel_assembly.assembly_coolant_id == universe + 21


def test_pin():
    """ Test the creation of the pin class"""
    assembly_type = 'A271'
    fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)
    fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
    fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
    fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])

    fuel_pin = ah.FuelPin(fuel)

    assert fuel_pin.pin_data.all == fuel.all
    assert fuel_pin.fuel_material[1] == fuel_material_fuel[1]
    assert fuel_pin.fuel_bond[1] == fuel_material_bond[1]
    assert fuel_pin.fuel_clad[1] == fuel_material_cladding[1]


test_assembly()
test_pin()