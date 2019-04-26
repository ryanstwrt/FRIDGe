import fridge.driver.global_variables as gb
import fridge.driver.reactorMaker as rm

# TODO implement sodium voiding
# TODO implement fuel radial expansion (density/volume change)
# TODO implement fuel axial expansion
# TODO implement coolant expansion
# TODO implement clad expansion
# TODO implement homogenization
# TODO add sensitivity parameter's to input
# TODO split XC to fuel, coolant, structure
# TODO utilize an avogadro's number from somewhere


def main(file_name):
    print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
    global_vars = gb.GlobalVariables()
    global_vars.read_input_file(file_name)
    print(global_vars.input_type)
    if global_vars.input_type == 'Single':
        print('Creating assembly: {}... Please Wait'.format(global_vars.file_name))
        rm.singleAssemblyMaker(global_vars)
        print('FRIDGe has finished creating your assembly')
    elif global_vars.input_type == 'Core':
        print('Creating core: {}... Please Wait'.format(global_vars.file_name))
        rm.coreMaker(global_vars)
        print('FRIDGe has finished creating your core')
