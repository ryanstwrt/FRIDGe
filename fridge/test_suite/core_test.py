import fridge.Core.Core as Core
import fridge.driver.global_variables as gb

global_vars = gb.GlobalVariables()
global_vars.read_input_file('Full_Core_Test')


def test_baseCore():
    core = Core.Core()
    assert core.name == ''
    assert core.assemblyList == []
    assert core.excessCoolant is None
    assert core.vessel is None
    assert core.vesselThickness == 0
    assert core.coolantSurfaceCard == ''
    assert core.coolantCellCard == ''
    assert core.materialCard == ''
    assert core.vesselMaterial is None
    assert core.vesselMaterialString == ''
    assert core.coolantRadius == 0
    assert core.coolantHeight == 0
    assert core.coolantPosition == []
    assert core.coolantMaterial is None
    assert core.vesselRadius == 0
    assert core.vesselPosition == []
    assert core.vesselSurfaceCard == ''
    assert core.coreCellList == []
    assert core.coreSurfaceList == []
    assert core.coreMaterialList == []
    assert core.everythingElse is None


def test_getCoreData():
    core = Core.Core()
    core.getCoreData('Core_Test')
    assert core.name == 'Test_Core'
    assert core.vesselThickness == 10
    assert core.vesselMaterialString == 'HT9'


#def test_getCore():
#    core = Core.Core()
#    core.getCoreData('Core_Test')
#    core.getCore(global_vars)
#
#    assert core.vesselMaterial is not None
#    assert core.coolantMaterial is not None
#    assert core.everythingElse is not None
#    assert core.excessCoolant is not None
#    assert core.vessel is not None
#    assert core.coolantRadius == 5.4
#    assert core.coolantHeight == 352
#    assert core.coolantPosition == [0, 0, -70]
#    assert core.vesselRadius == 15.4
#    assert core.vesselPosition == [0, 0, -80]
#    assert core.vesselHeight == 372
#    assert len(core.assemblyList) == 7
