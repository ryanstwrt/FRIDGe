from FRIDGe.fridge.utilities import materialReader
import numpy as np


def test_element_C():
    e = materialReader.Element('C')
    assert e.name == 'Carbon'
    assert e.zaid == 6000
    assert e.isotopes == [6000]
    assert e.molecularMass == [12.0107]
    assert e.abundance == [1]
    assert e.density == 1.8
    assert e.linearCoeffExpansion == 0.0


def test_element_Fe():
    e = materialReader.Element('Fe')
    assert e.name == 'Iron'
    assert e.zaid == 26000
    assert e.isotopes == [26054, 26056, 26057, 26058]
    assert e.molecularMass == [53.939608, 55.934935, 56.935392, 57.933273]
    assert e.abundance == [0.05845, 0.91754, 0.02119, 0.00282]
    assert e.density == 7.874
    assert e.linearCoeffExpansion == 0.0


def test_element_Pu():
    e = materialReader.Element('Pu')
    assert e.name == 'Plutonium'
    assert e.zaid == 94000
    assert e.isotopes == [94238, 94239, 94240, 94241, 94242]
    assert e.molecularMass == [238.0495582, 239.0521617, 240.0538118, 241.0538497, 242.0587410]
    assert e.abundance == [0.0, 0.0, 0.0, 0.0, 0.0]
    assert e.density == 19.84
    assert e.linearCoeffExpansion == 0.0


def test_material():
    m = materialReader.Material()
    assert m.enrichmentDict == {}
    assert m.isotopeDict == {}
    assert m.weightPercent == {}
    assert m.atomPercent == {}
    assert m.atomDensity == 0.0
    assert m.elementDict == {}
    assert m.name == ''
    assert m.elements == []
    assert m.zaids == []
    assert m.weightFraction == []
    assert m.density == 0.0
    assert m.linearCoeffExpansion == 0.0
    assert m.enrichmentZaids == []
    assert m.enrichmentIsotopes == []
    assert m.enrichmentVector == []


def test_material_liqduiNa():
    m = materialReader.Material()
    m.setMaterial('LiquidNa')
    assert m.name == 'Liquid Sodium'
    assert m.elements == ['Na']
    assert m.zaids == [11000]
    assert m.weightFraction == [1.0]
    assert m.enrichmentZaids == []
    assert m.enrichmentIsotopes == []
    assert m.enrichmentVector == []
    assert m.density == 0.927
    assert np.allclose(m.atomDensity, 0.0242826)
    assert m.atomPercent == {11023: 1.0}


def test_material_5Pu22U10Zr():
    m = materialReader.Material()
    m.setMaterial('5Pu22U10Zr')
    assert m.name == '5Pu22U10Zr'
    assert m.elements == ['U', 'Pu', 'Zr']
    assert m.zaids == [92000, 94000, 40000]
    assert m.weightFraction == [0.85, 0.05, 0.1]
    assert m.enrichmentZaids == [92000, 94000]
    assert m.enrichmentIsotopes == [[92234, 92235, 92236, 92238], [94239, 94240]]
    assert m.enrichmentVector == [[0.0, 0.2588, 0.0, 0.7412], [0.94, 0.060]]


def test_material_UO2():
    """
    Test material is from the Compendium of Material Composition Data for Radiation Transport Modeling: Revision 1
    The atom density form the Compendium lists 0.07335, however the calculated atom density is 0.073361. This may
    be due to slighty variations in abundance definitions. The error is within 0.01% of the known atom density.
    """
    m = materialReader.Material()
    m.setMaterial('UO2')
    assert m.name == 'Uranium Dioxide'
    assert m.elements == ['U', 'O']
    assert m.zaids == [92000, 8000]
    assert m.weightFraction == [0.881467, 0.118533]
    assert m.enrichmentZaids == [92000, 8000]
    assert m.enrichmentIsotopes == [[92234, 92235, 92236, 92238], [8016, 8017, 8018]]
    assert m.enrichmentVector == [[0.00026660018529341, 0.029999988655276, 0.0001384056351514, 0.96959500496104],
                                  [1.0, 0.0, 0.0]]
    assert m.density == 10.96
    assert np.allclose(m.atomDensity, 0.07336, 5)
    atomPercentKnown = {92234: 0.000090, 92235: 0.010124, 92236: 0.000046, 92238: 0.323072, 8016: 0.666667}
    for k, v in atomPercentKnown.items():
        assert np.allclose(m.atomPercent[k], v, 5)

def test_material_HT9():
    """
    Test material is from the Compendium of Material Composition Data for Radiation Transport Modeling: Revision 1
    """
