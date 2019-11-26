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
        self.smearUniverse = None
        self.smearCoolant = None
        self.latticeUniverse = None
        self.fuelUniverse = None
        self.innerDuct = None
        self.duct = None
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
        self.fuel_region = 0
        self.fuel_volume = 0
        self.region_height = 0
        self.z_below_fuel = 0
        self.z_below_fuel_pos = []
        self.fuelMaterial = ''
        self.cladMaterial = ''
        self.bondMaterial = ''
        self.axialRegionsInput = {}
        self.axialRegions = {}
        self.axialRegionDict = {}

        self.get_fuel_assembly_data()
        self.build_fuel_assembly()

    def get_fuel_assembly_data(self):
        """Assign assembly data for the fuel assembly."""
        self.get_assembly_data(self.inputs)
        self.axialRegionsInput = self.inputs['Axial Regions']
        self.axialRegionDict = {}
        for region in self.axialRegionsInput:
            try:
                self.axialRegionDict[region] = self.inputs['Axial Region {}'.format(region)]
                if 'Fuel Height' in self.axialRegionDict[region]:
                    self.fuel_region = region
            except:
                print("Failed to create axial region {} for assembly {}, "
                      "ensure this region is defined".format(region, self.assembly_file_name))
        self.read_fuel_region_data(self.inputs)

        # Update for perturbations
        if bool(self.globalVars.assembly_perturbations):
            self.update_perturbations()

    def build_fuel_assembly(self):
        """Create the cell, surface, and material cards for the fuel assembly."""
        self.assemblyUniverse = self.universe

        #The fuel is always at z=0, so we need to find the start of the first axial position
        self.z_below_fuel = sum(region_dict['Smear Height'] for region, region_dict in self.axialRegionDict.items()
                                if region < self.fuel_region)
        self.z_below_fuel_pos = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                       -self.z_below_fuel)
        zPosition = 0
        for region, region_dict in self.axialRegionDict.items():
            self.region_height = region_dict['Smear Height'] if 'Smear Height' in region_dict.keys() else self.fuelHeight

            # TODO create a way to ensure we don't accidentally add height to fuel if it is region 1
            if region == 1:
                self.region_height += 0.1
                zPosition = -(self.z_below_fuel+0.1)

            cur_position = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                  zPosition)
            try:
                self.axialRegions[region] = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                          region_dict['Smear Materials'], self.xcSet,
                                                          cur_position, self.materialNum],
                                                          [self.ductOuterFlatToFlatMCNPEdge, self.region_height],
                                                          region_dict['Smear Name']],
                                                          void_material=self.coolantMaterial,
                                                          void_percent=self.voidPercent)
                self.assemblyCellList.append(self.axialRegions[region])
                self.assemblySurfaceList.append(self.axialRegions[region])
                self.assemblyMaterialList.append(self.axialRegions[region])
                self.update_global_identifiers(False)
            except (AttributeError, KeyError):
                fuel_lists = self.create_fuel_cell(cur_position)
                self.region_height += self.bondAboveFuel
                self.assemblyCellList.extend(fuel_lists[0])
                self.assemblySurfaceList.extend(fuel_lists[1])
                self.assemblyMaterialList.extend(fuel_lists[2])

            zPosition += self.region_height

        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, self.z_below_fuel_pos,
                                                     self.materialNum],
                                                    [self.assemblyHeight,  self.ductOuterFlatToFlat]])

        self.assemblyCellList.append(self.assemblyShell)
        self.assemblySurfaceList.append(self.assemblyShell)
        self.assemblyMaterialList.append(self.assemblyShell)

        if 'Single' in self.globalVars.input_type:
            self.update_global_identifiers(False)
            self.everythingElse = Everythingelse.EveryThingElse([self.cellNum, self.assemblyShell.surfaceNum])
            self.assemblyCellList.append(self.everythingElse)

    def read_fuel_region_data(self, inputs):
        """Reads in the fuel region data from the assembly yaml file."""
        self.position = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                               self.zPosition)
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
        self.fuel_height_with_bond = self.fuelHeight + self.bondAboveFuel

    def create_fuel_cell(self, cur_position):
        self.universe += 1
        self.pinUniverse = self.universe
        fuelCoolantHeight = self.region_height + self.bondAboveFuel
        self.fuel = Fuelpin.FuelPin([[self.universe, self.cellNum, self.surfaceNum, self.fuelMaterial, self.xcSet,
                                      cur_position, self.materialNum], [self.fuelDiameter, self.region_height,
                                                                        self.pinsPerAssembly]])
        self.fuel_volume = self.fuel.volume

        self.update_global_identifiers(False)
        self.bond = Fuelbond.FuelBond([[self.universe, self.cellNum, self.surfaceNum, self.bondMaterial, self.xcSet,
                                        cur_position, self.materialNum],
                                       [self.cladID, fuelCoolantHeight, self.fuel.surfaceNum]])

        self.update_global_identifiers(False)
        self.clad = Fuelclad.FuelClad([[self.universe, self.cellNum, self.surfaceNum, self.cladMaterial, self.xcSet,
                                        cur_position, self.materialNum],
                                       [self.cladOD, fuelCoolantHeight, self.bond.surfaceNum]])

        self.update_global_identifiers(False)
        smeared_coolant_info = [self.fuel_height_with_bond, self.cladOD, self.wireWrapDiameter,
                                self.wireWrapAxialPitch, self.fuelPitch, self.coolantMaterial, self.cladMaterial]

        smeared_coolant_material = Material.smear_coolant_wirewrap(smeared_coolant_info)
        self.coolant = Fuelcoolant.FuelCoolant([[self.universe, self.cellNum, self.surfaceNum, smeared_coolant_material,
                                                 self.xcSet, cur_position, self.materialNum],
                                                [self.fuelPitch, fuelCoolantHeight, self.clad.surfaceNum],
                                                'Wire Wrap + Coolant'], void_material=self.coolantMaterial,
                                               void_percent=self.voidPercent)
        self.update_global_identifiers(True)
        self.blankUniverse = self.universe
        self.blankCoolant = Blankcoolant.BlankCoolant([[self.universe, self.cellNum, self.surfaceNum,
                                                        self.coolantMaterial, self.xcSet, cur_position,
                                                        self.materialNum],
                                                       [self.fuelPitch, fuelCoolantHeight,
                                                        self.coolant.surfaceNum]], void_percent=self.voidPercent)
        self.update_global_identifiers(True)
        self.latticeUniverse = self.universe
        self.fuelUniverse = Fueluniverse.FuelUniverse([self.pinUniverse, self.blankUniverse, self.pinsPerAssembly,
                                                       self.cellNum, self.blankCoolant.cellNum, self.latticeUniverse])

        self.update_global_identifiers(True)
        self.innerDuct = Innerduct.InnerDuct([[self.universe, self.cellNum, self.surfaceNum, '', self.xcSet,
                                               cur_position, self.materialNum],
                                              [self.assemblyUniverse, self.latticeUniverse, self.ductInnerFlatToFlat,
                                               fuelCoolantHeight]])

        self.update_global_identifiers(False)
        self.duct = Outerduct.Duct([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.assemblyMaterial,
                                     self.xcSet, cur_position, self.materialNum],
                                    [self.ductOuterFlatToFlatMCNPEdge, fuelCoolantHeight, self.innerDuct.surfaceNum]])
        self.update_global_identifiers(False)

        cell_list = [self.fuel, self.bond, self.clad, self.coolant, self.blankCoolant, self.fuelUniverse, self.innerDuct, self.duct]
        surface_list = [self.fuel, self.bond, self.clad, self.coolant, self.blankCoolant, self.innerDuct, self.duct]
        mat_list = [self.fuel, self.bond, self.clad, self.coolant, self.blankCoolant, self.innerDuct, self.duct]
        return [cell_list, surface_list, mat_list]