import fridge.driver.fridge_driver as fd

def create_core(core_list, assem_perts={}):
    """Wrapper around FRIDGe to create multiple cores concurrently"""

    for core in core_list:
        print('Core: ' + core)
        core_type = core[9:17]
        print(core_type)
        print(assem_perts)
        file = 'FC_' + core_type + '_' + fuel + '_BU'
        fd.main(core, assembly_perturbations=assem_perts, output_name=file)
        file='FC_' + core_type + '_' + fuel + '_600K'
        #fd.main(core, assembly_perturbations=assem_perts, temperature=600, output_name=file)
        file='FC_' + core_type + '_' + fuel + '_Void'
        #fd.main(core, assembly_perturbations=assem_perts, void_per=0.001, output_name=file)


cores = ['FullCore_FS50_H50']#, 'FullCore_FS70_H70', 'FullCore_FS70_H60', 'FullCore_FS70_H50']
fuel_list = ['7Pu20U10Zr', '15Pu12U10Zr', '20Pu7U10Zr', '27Pu0U10Zr', '27U10Zr']
assembly = 'A271_FS50_H50'
for fuel in fuel_list:
    create_core(cores, assem_perts={assembly: {'fuelMaterial': fuel}})
