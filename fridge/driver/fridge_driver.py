import FRIDGe.fridge.driver.data_maker as dm
import FRIDGe.fridge.Assembly.FuelAssembly as FuelAssembly
import FRIDGe.fridge.Assembly.Assembly as Assembly
import FRIDGe.fridge.utilities.mcnp_input_deck_maker as midm
import FRIDGe.fridge.driver.global_variables as gb

# TODO implement sodium voiding
# TODO implement fuel radial expansion (density/volume change)
# TODO implement fuel axial expansion
# TODO implement coolant expansion
# TODO implement clad expansion
# TODO implement homogenization
# TODO add sensitivity parameter's to input
# TODO split XC to fuel, coolant, structure
# TODO add catch for clad greater than sodium universe
# TODO add catch for clad+wire wrap greater than sodium universe
# TODO add catch for fuel/bond greater than each other or clad
# TODO Allow user to input fuel diameter
# TODO Finish adding tests
# TODO Add more documentation
# TODO create atom number check for smear
# TODO convert AssertionErrors to print to screen errors
# TODO utilize an avogadro's number from somewhere


def main(file_name):
    print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
    file_name = 'A271_Assembly'
    # input('Please input the file name you would like to model: ')

    global_vars = gb.GlobalVariables()
    global_vars.read_input_file(file_name)
    print('Creating your Assembly/Core... Please Wait')
    assemblyInfo = [global_vars.assembly_name, '01A01', global_vars]
    assemblyLocation = Assembly.getAssemblyLocation(global_vars.assembly_name)
    assemblyType = Assembly.assemblyTypeReader(assemblyLocation)
    assembly = None
    if assemblyType == 'Fuel':
        assembly = FuelAssembly.FuelAssembly(assemblyInfo)
    k_card = dm.make_mcnp_problem(global_vars)
    print('FRIDGe has finished creating your Assembly/Core')
    midm.mcnp_input_deck_maker(assembly, k_card, global_vars)
