import fridge.Assembly.FuelAssembly as FuelAssembly
import fridge.Assembly.Assembly as Assembly
import fridge.Assembly.BlankAssembly as BlankAssembly
import fridge.utilities.mcnpCreatorFunctions as mcf
import fridge.Core.Core as Core


def singleAssemblyMaker(global_vars):
    assemblyInfo = [global_vars.file_name, '01A01', global_vars]
    assemblyLocation = Assembly.getAssemblyLocation(global_vars.file_name)
    assemblyType = Assembly.assemblyTypeReader(assemblyLocation)
    assembly = None
    if assemblyType == 'Fuel':
        assembly = FuelAssembly.FuelAssembly(assemblyInfo)
    elif assemblyType == 'Blank':
        assembly = BlankAssembly.BlankAssembly(assemblyInfo)
    k_card = mcf.make_mcnp_problem(global_vars)
    mcf.mcnp_input_deck_maker(assembly, k_card, global_vars)


def coreMaker(global_vars):
    coreInfo = [global_vars.file_name, global_vars]
    core = Core.Core()
    coreData = core.getCoreData(global_vars.file_name)
    print(coreData)
    print(type(coreData))

    pass