from FRIDGe.fridge.utilities import geometry_reader as geo_read


def test_fuel_assembly_reader():
    """Tests the fuel assembly reader by reading in a known fuel
    assembly and ensure the values are accurate."""

    fuel_data, assembly_data, plenum_data, fuel_reflector_data = geo_read.fuel_assembly_geometry_reader('A271_Test')

    # Test the fuel data
    assert 0.53 == fuel_data.ix['pin_diameter', 'fuel']
    assert 0.037 == fuel_data.ix['clad_thickness', 'fuel']
    assert 0.75 == fuel_data.ix['fuel_smear', 'fuel']
    assert 0.661 == fuel_data.ix['pitch', 'fuel']
    assert 0.126 == fuel_data.ix['wire_wrap_diameter', 'fuel']
    assert 60.0 == fuel_data.ix['height', 'fuel']
    assert '27U' == fuel_data.ix['fuel', 'fuel']
    assert 'HT9' == fuel_data.ix['clad', 'fuel']
    assert 'Liquid_Na' == fuel_data.ix['bond', 'fuel']

    # Test the FuelAssembly data
    assert 271 == assembly_data.ix['pins_per_assembly', 'assembly']
    assert 12 == assembly_data.ix['assembly_pitch', 'assembly']
    assert 0.3 == assembly_data.ix['duct_thickness', 'assembly']
    assert 0.3 == assembly_data.ix['assembly_gap', 'assembly']
    assert 11.1 == assembly_data.ix['inside_flat_to_flat', 'assembly']
    assert 320 == assembly_data.ix['height', 'assembly']
    assert 'Liquid_Na' == assembly_data.ix['coolant', 'assembly']
    assert 'HT9' == assembly_data.ix['assembly', 'assembly']

    # Check the Plenum data
    assert 60 == plenum_data.ix['height', 'plenum']
    assert 0.50 == plenum_data.ix['coolant_per', 'plenum']
    assert 0.25 == plenum_data.ix['void_per', 'plenum']
    assert 0.25 == plenum_data.ix['clad_per', 'plenum']
    assert 'Liquid_Na' == plenum_data.ix['coolant', 'plenum']
    assert 'Void' == plenum_data.ix['void', 'plenum']
    assert 'HT9' == plenum_data.ix['clad', 'plenum']

    # Check the Fuel Reflector data
    assert 50 == fuel_reflector_data.ix['height', 'fuel_reflector']
    assert 0.3 == fuel_reflector_data.ix['coolant_per', 'fuel_reflector']
    assert 0.7 == fuel_reflector_data.ix['clad_per', 'fuel_reflector']
    assert 'Liquid_Na' == fuel_reflector_data.ix['coolant', 'fuel_reflector']
    assert 'HT9' == fuel_reflector_data.ix['clad', 'fuel_reflector']

    return