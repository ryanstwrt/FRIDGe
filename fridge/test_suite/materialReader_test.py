from FRIDGe.fridge.utilities import materialReader


def test_element_carbon():
    e = materialReader.Element('C')
    assert e.name == 'Carbon'
    assert e.zaid == 6000
    assert e.isotopes == [6000]
    assert e.molecularMass == [12.0107]
    assert e.abundance == [1]
    assert e.density == 1.8
    assert e.linearCoeffExpansion == 0.0


def test_element_iron():
    e = materialReader.Element('Fe')
    assert e.name == 'Iron'
    assert e.zaid == 26000
    assert e.isotopes == [26054, 26056, 26057, 26058]
    assert e.molecularMass == [53.939608, 55.934935, 56.935392, 57.933273]
    assert e.abundance == [0.05845, 0.91754, 0.02119, 0.00282]
    assert e.density == 7.874
    assert e.linearCoeffExpansion == 0.0


def test_element_plutonium():
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

