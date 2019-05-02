import fridge.Assembly.Assembly as Assembly
import fridge.Constituent.FuelPin as Fuelpin
import fridge.Constituent.FuelBond as Fuelbond
import fridge.Constituent.FuelClad as Fuelclad
import fridge.Constituent.FuelCoolant as Fuelcoolant
import fridge.Constituent.BlankCoolant as Blankcoolant
import fridge.Constituent.FuelUniverse as Fueluniverse
import fridge.Constituent.InnerDuct as Innerduct
import fridge.Constituent.Duct as Outerduct
import fridge.Constituent.Smear as Smeared
import fridge.Constituent.OuterShell as Outershell
import fridge.Constituent.UpperCoolant as Uppersodium
import fridge.Constituent.LowerCoolant as Lowersodium
import fridge.Constituent.EveryThingElse as Everythingelse
import fridge.Material.Material as Material
import fridge.utilities.utilities as utilities
import math


class FuelAssembly(Assembly.Assembly):
    """
    Subclass of base assembly for fuel assemblies.

    Fuel assembly consists of upper/lower sodium region, upper/lower reflector regions,
    a plenum region, and a fuel region. All information for fuel, reflector and plenum regions are read in from the
    assembly yaml file.
    """

    def __init__(self, assembly_information):
        super().__init__(assembly_information)
        self.assemblyUniverse = 0
        self.pinUniverse = 0
        self.fuel = None
        self.bond = None
        self.clad = None
        self.coolant = None
        self.blankUniverse = None
        self.blankCoolant = None
        self.latticeUniverse = None
        self.fuelUniverse = None
        self.innerDuct = None
        self.duct = None
        self.plenum = None
        self.upperReflector = None
        self.lowerReflector = None
        self.upperSodium = None
        self.lowerSodium = None
        self.assemblyShell = None
        self.assemblyCellList = []
        self.assemblySurfaceList = []
        self.assemblyMaterialList = []
        self.everythingElse = None

        self.position = []
        self.cladOD = 0
        self.cladID = 0
        self.fuelDiameter = 0
        self.fuelPitch = 0
        self.wireWrapDiameter = 0
        self.wireWrapAxialPitch = 0
        self.bondAboveFuel = 0.0
        self.fuelHeight = 0
        self.fuel_height_with_bond = 0
        self.fuelMaterial = ''
        self.cladMaterial = ''
        self.bondMaterial = ''

        self.plenumHeight = 0
        self.plenumMaterial = ''
        self.plenumPosition = []

        self.reflectorHeight = 0
        self.reflectorMaterial = ''

        self.read_fuel_assembly_data()
        self.build_fuel_assembly()

    def read_fuel_assembly_data(self):
        """ Reads in data from assembly yaml file."""
        self.get_assembly_data(self.inputs)
        self.read_fuel_region_data(self.inputs)
        self.read_plenum_region_data(self.inputs)
        self.read_reflector_region_data(self.inputs)

    def build_fuel_assembly(self):
        """Creates each component of the assembly."""
        self.fuel_height_with_bond = self.fuelHeight + self.bondAboveFuel
        defined_height = 2 * self.reflectorHeight + self.fuel_height_with_bond + self.plenumHeight
        excess_coolant_height = (self.assemblyHeight - defined_height) / 2
        height_to_upper_coolant = defined_height - self.reflectorHeight
        height_to_upper_reflector = self.fuel_height_with_bond + self.plenumHeight
        upper_coolant_position = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                        height_to_upper_coolant)
        upper_reflector_position = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                          height_to_upper_reflector)
        lower_reflector_position = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                          -self.reflectorHeight)
        bottom_coolant_position = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                         -(self.reflectorHeight
                                                          + excess_coolant_height))

        self.assemblyUniverse = self.universe
        self.universe += 1
        self.pinUniverse = self.universe
        self.fuel = Fuelpin.FuelPin([[self.universe, self.cellNum, self.surfaceNum, self.fuelMaterial, self.xcSet,
                                      self.position, self.materialNum], [self.fuelDiameter, self.fuelHeight]])

        self.update_global_identifiers(False)
        self.bond = Fuelbond.FuelBond([[self.universe, self.cellNum, self.surfaceNum, self.bondMaterial, self.xcSet,
                                        self.position, self.materialNum],
                                       [self.cladID, self.fuel_height_with_bond, self.fuel.surfaceNum]])

        self.update_global_identifiers(False)
        self.clad = Fuelclad.FuelClad([[self.universe, self.cellNum, self.surfaceNum, self.cladMaterial, self.xcSet,
                                        self.position, self.materialNum],
                                       [self.cladOD, self.fuel_height_with_bond, self.bond.surfaceNum]])

        self.update_global_identifiers(False)
        smeared_coolant_info = [self.fuel_height_with_bond, self.cladOD, self.wireWrapDiameter,
                                self.wireWrapAxialPitch, self.fuelPitch, self.coolantMaterial, self.cladMaterial]
        smeared_coolant_material = Material.smear_coolant_wirewrap(smeared_coolant_info)
        self.coolant = Fuelcoolant.FuelCoolant([[self.universe, self.cellNum, self.surfaceNum, smeared_coolant_material,
                                                 self.xcSet, self.position, self.materialNum],
                                                [self.fuelPitch, self.fuel_height_with_bond, self.clad.surfaceNum],
                                                'Wire Wrap + Coolant'], void_material=self.coolantMaterial,
                                               void_percent=self.voidPercent)
        self.update_global_identifiers(True)
        self.blankUniverse = self.universe
        self.blankCoolant = Blankcoolant.BlankCoolant([[self.universe, self.cellNum, self.surfaceNum,
                                                        self.coolantMaterial, self.xcSet, self.position,
                                                        self.materialNum],
                                                       [self.fuelPitch, self.fuel_height_with_bond,
                                                        self.coolant.surfaceNum]], void_percent=self.voidPercent)
        self.update_global_identifiers(True)
        self.latticeUniverse = self.universe
        self.fuelUniverse = Fueluniverse.FuelUniverse([self.pinUniverse, self.blankUniverse, self.pinsPerAssembly,
                                                       self.cellNum, self.blankCoolant.cellNum, self.latticeUniverse])

        self.update_global_identifiers(True)
        self.innerDuct = Innerduct.InnerDuct([[self.universe, self.cellNum, self.surfaceNum, '', self.xcSet,
                                               self.position, self.materialNum],
                                              [self.assemblyUniverse, self.latticeUniverse, self.ductInnerFlatToFlat,
                                               self.fuel_height_with_bond]])

        self.update_global_identifiers(False)
        self.plenum = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.plenumMaterial,
                                      self.xcSet, self.plenumPosition, self.materialNum],
                                     [self.ductInnerFlatToFlat, self.plenumHeight], 'Plenum'],
                                    void_material=self.coolantMaterial, void_percent=self.voidPercent)

        self.update_global_identifiers(False)
        self.upperReflector = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                              self.reflectorMaterial, self.xcSet, upper_reflector_position,
                                              self.materialNum],
                                             [self.ductInnerFlatToFlat, self.reflectorHeight], 'Upper Reflector'],
                                            void_material=self.coolantMaterial, void_percent=self.voidPercent)

        self.update_global_identifiers(False)
        self.lowerReflector = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                              self.reflectorMaterial, self.xcSet, lower_reflector_position,
                                              self.materialNum],
                                             [self.ductInnerFlatToFlat, self.reflectorHeight], 'Lower Reflector'],
                                            void_material=self.coolantMaterial, void_percent=self.voidPercent)

        self.update_global_identifiers(False)
        inner_surface_nums = [self.innerDuct.surfaceNum, self.lowerReflector.surfaceNum, self.upperReflector.surfaceNum,
                              self.plenum.surfaceNum]
        self.duct = Outerduct.Duct([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.assemblyMaterial,
                                     self.xcSet, lower_reflector_position, self.materialNum],
                                    [self.ductOuterFlatToFlatMCNPEdge, defined_height, inner_surface_nums]])

        self.update_global_identifiers(False)
        self.lowerSodium = Lowersodium.LowerCoolant([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                      self.coolantMaterial, self.xcSet, bottom_coolant_position,
                                                      self.materialNum],
                                                     [excess_coolant_height,
                                                     self.ductOuterFlatToFlatMCNPEdge]], void_percent=self.voidPercent)

        self.update_global_identifiers(False)
        self.upperSodium = Uppersodium.UpperCoolant([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                      self.coolantMaterial, self.xcSet, upper_coolant_position,
                                                      self.materialNum],
                                                     [excess_coolant_height,
                                                     self.ductOuterFlatToFlatMCNPEdge]], void_percent=self.voidPercent)

        self.update_global_identifiers(False)
        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, bottom_coolant_position,
                                                     self.materialNum],
                                                    [self.assemblyHeight,  self.ductOuterFlatToFlat]])

        self.assemblyCellList = [self.fuel, self.bond, self.clad, self.coolant, self.blankCoolant, self.fuelUniverse,
                                 self.innerDuct, self.plenum, self.upperReflector, self.lowerReflector,
                                 self.duct, self. lowerSodium, self.upperSodium, self.assemblyShell]
        self.assemblySurfaceList = [self.fuel, self.bond, self.clad, self.coolant, self.blankCoolant, self.innerDuct,
                                    self.plenum, self.upperReflector, self.lowerReflector, self.duct, self. lowerSodium,
                                    self.upperSodium, self.assemblyShell]
        self.assemblyMaterialList = [self.fuel, self.bond, self.clad, self.coolant, self.blankCoolant, self.innerDuct,
                                     self.plenum, self.upperReflector, self.lowerReflector, self.duct,
                                     self. lowerSodium, self.upperSodium]

        if 'Single' in self.globalVars.input_type:
            self.update_global_identifiers(False)
            self.everythingElse = Everythingelse.EveryThingElse([self.cellNum, self.assemblyShell.surfaceNum])
            self.assemblyCellList.append(self.everythingElse)

    def read_fuel_region_data(self, inputs):
        """Reads in the fuel region data from the assembly yaml file."""
        self.position = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch, 0.0)
        self.cladOD = float(inputs['Pin Diameter'])
        self.cladID = self.cladOD - 2*float(inputs['Clad Thickness'])
        try:
            self.fuelDiameter = float(inputs["Fuel Diameter"])
        except KeyError:
            self.fuelDiameter = math.sqrt(float(inputs['Fuel Smear'])) * self.cladID
        self.fuelPitch = float(inputs['Pitch'])
        self.wireWrapDiameter = float(inputs['Wire Wrap Diameter'])
        self.wireWrapAxialPitch = float(inputs['Wire Wrap Axial Pitch'])
        self.fuelHeight = float(inputs['Fuel Height'])
        self.fuelMaterial = inputs['Fuel Material']
        self.cladMaterial = inputs['Clad Material']
        self.bondMaterial = inputs['Bond Material']
        self.bondAboveFuel = float(inputs["Bond Above Fuel"]) \
            if 'Bond Above Fuel' in inputs else 0.0

    def read_plenum_region_data(self, inputs):
        """Reads in the plenum region data from the assembly yaml file."""
        self.plenumHeight = float(inputs['Plenum Height'])
        self.plenumPosition = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                     self.fuelHeight + self.bondAboveFuel)
        self.plenumMaterial = inputs['Plenum Smear']

    def read_reflector_region_data(self, inputs):
        """Reads in the reflector region data form the assembly yaml file."""
        self.reflectorHeight = float(inputs['Reflector Height'])
        self.reflectorMaterial = inputs['Reflector Smear']
