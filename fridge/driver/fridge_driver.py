from FRIDGe.fridge.input_readers import material_reader as mat_read
from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.driver import assembly_holder as ah

print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
assembly_type = 'A271'# input('Please input the assembly type you would like to model: ')

fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)


fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])

fuel_assembly = ah.Assembly(assembly, 'fuel')



print(fuel_pin.pin_data)
