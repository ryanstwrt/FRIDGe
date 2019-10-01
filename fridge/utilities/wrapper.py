import fridge.driver.fridge_driver as fd


def create_core(core_list, assem_perts={}):
    """Wrapper around FRIDGe to create multiple cores concurrently"""

    for core in core_list:
        print('Core: ' + core)
        core_type = core[9:17]

        file = 'FC_' + core_type + '_' + fuel
        fd.main(core, assembly_perturbations=assem_perts, output_name=file)
        file='FC_' + core_type + '_' + fuel + '_600K'
#        fd.main(core, assembly_perturbations=assem_perts, temperature=600, output_name=file)
        file='FC_' + core_type + '_' + fuel + '_Void'
#        fd.main(core, assembly_perturbations=assem_perts, void_per=0.001, output_name=file)


cores = ['FullCore_FS70_H50_15Pu_12U']#, 'FullCore_FS70_H60_15Pu_12U', 'FullCore_FS70_H70_15Pu_12U', 'FullCore_FS70_H80_15Pu_12U']
fuel = '7Pu20U10Zr'
assembly = 'A271_FS70_H50'
reflector = 'Reflector_H50'
create_core(cores, assem_perts={assembly: {'fuelMaterial': fuel}, reflector: {'smearRegionHeight': 200}})
