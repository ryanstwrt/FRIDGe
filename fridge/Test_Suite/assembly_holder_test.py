from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.input_readers import material_reader as mat_read

def test_assembly():
    """ Test the creation of the assembly class"""
    assembly_type = 'A271'
    fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)

    fuel_assembly = ah.Assembly(assembly, 'fueled')

    assert fuel_assembly.assembly_data.all == assembly.all
    assert fuel_assembly.assembly_type == 'fueled'

test_assembly()