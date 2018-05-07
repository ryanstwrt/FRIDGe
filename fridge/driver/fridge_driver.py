from FRIDGe.fridge.input_readers import material_reader as mat_read
from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import pin_maker

print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
assembly_type = 'A271'# input('Please input the assembly type you would like to model: ')

fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)

# Potentially throw these three functions into the assembly holder and unpack them when they are needed.
fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])

fuel_assembly = ah.Assembly(assembly, 'fuel', [fuel, fuel_material_fuel, fuel_material_bond, fuel_material_cladding], 1000)
fuel_pin = pin_maker.fuel_pin_maker(fuel_assembly)

print(fuel_assembly.pin.fuel_pellet_surface)
print(fuel_assembly.pin.fuel_pellet_mcnp_surface)
print(fuel_assembly.pin.fuel_pellet_cell)
print(fuel_assembly.pin.fuel_pellet_mcnp_cell)
print(fuel_assembly.pin.fuel_bond_surface)
print(fuel_assembly.pin.fuel_bond_mcnp_surface)
print(fuel_assembly.pin.fuel_bond_cell)
print(fuel_assembly.pin.fuel_bond_mcnp_cell)
