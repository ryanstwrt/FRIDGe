import FRIDGe.fridge.driver.global_variables as gb
import FRIDGe.fridge.driver.reactorMaker as rm

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
    print('Creating your Assembly/Core... Please Wait')
    if 'Input Type' == 'Single':
        rm.singleAssemblyMaker(global_vars)
    elif 'Input Type' == 'Core':
        rm.coreMaker(global_vars)
    print('FRIDGe has finished creating your Assembly/Core')