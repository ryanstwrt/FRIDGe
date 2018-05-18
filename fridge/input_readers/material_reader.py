import numpy as np
import glob
import os

AVOGADROS_NUMBER = 0.6022140857
# Requirements for the material reader
txt_ext = ".txt"
cur_dir = os.path.dirname(__file__)
element_dir = os.path.join(cur_dir, '../CotN/')
material_dir = os.path.join(cur_dir, '../Materials/')


def get_elem_string(material):
    """Returns a vector of strings with the elements for the given material.

    This is the first step in creating a material, we need the elements present
    the given material.

    args:
        material (str array): A string of the material name

    returns:
        element_vector (str array): An array with the number of elements
        required for the material

    """
    cur_material = glob.glob(os.path.join(material_dir, material[0] + '.*'))

    if cur_material == []:
        print('\n\033[1;37;31mFatal Error: The material %s is currently not supported.\n'
              'Either select a different material or create the material using the utilities.' % material)
        quit()
    with open(cur_material[0], "r") as mat_file:
        for i, line in enumerate(mat_file):
            if i == 1:
                line = line.strip()
                element_vector = [x for x in line.split(' ')]
    return element_vector

def element_input(element):
    """Returns an array with all isotopes present

    Second step in creating a material. This function obtains the physical
    properties of each isotope present in a material. Where the properties are:
    [0] = ZAID
    [1] = Mass Number
    [2] = Isotopic Abundnce
    [3] = Density
    [4] = Coefficient of Expansion
    Mass Number & Isotopic abundance are reference from IAEA Live Chart of the Nuclides
    Density is reference from 'Nuclides & Isotopes Chart of the Nuclides' 17th Edition

    args:
        element (str array): An array with the number of elements required
        for the particular material

    returns:
        isotopes (double array): Returns a # of isotopes by 6 array which contains
        the physical properties for each isotopes.

    """
    cur_element = glob.glob(os.path.join(element_dir, element[0] + '.*'))
    # Allocate space for elements being added
    num_elements = int(sum(1 for line in open(cur_element[0]) if line.rstrip()) - 3)
    isotopes = np.zeros((num_elements, 6))
    sum_wt = 0
    with open(cur_element[0], "r") as mat_file:
        iso_num = 0
        for i, line in enumerate(mat_file):
            mat_line = [x for x in line.split(' ')]
            if i == 1:
                isotope = mat_line[0]
            if i > 2:
                isotopes[iso_num][0] = isotope
                isotopes[iso_num][1] = mat_line[0]
                isotopes[iso_num][2] = mat_line[1]
                isotopes[iso_num][3] = mat_line[2]
                isotopes[iso_num][4] = mat_line[3]
                isotopes[iso_num][5] = mat_line[4]
                sum_wt += isotopes[iso_num][3]
                iso_num += 1
        if sum_wt == 0:
            pass
        elif round(sum_wt, 8) != 1.0000:
            print('\033[1;37;33mWARNING: The weight of %s was %f and not normalized to 1. '
                  'Check element to determine error' % (element, sum_wt))
    return isotopes


def elem_at2wt_per(at_per):
    """
    Converts the original elemental data (Chart of the Nuclides)
    from atom percent to weight percent.

    This is to ensure everything is on equal setting when working
    with wt% and enrichment.

    args:
        at_per (double array): The atom percent of a particular element

    returns:
        wt_per (double array): The weight percent for the element in question

    """
    num_elem = int(sum(1 for i in enumerate(at_per)))
    wt_per = np.copy(at_per)
    mol_wt = 0
    wt_by_mass = np.zeros(num_elem)
    for i, x in enumerate(at_per):
        wt_by_mass[i] = x[2]*x[3]
        mol_wt += wt_by_mass[i]
    for i, x in enumerate(at_per):
        # Pass for elements with no naturally occurring isotopes
        if mol_wt == 0:
            pass
        else:
            wt_per[i][3] = wt_by_mass[i] / mol_wt
    return wt_per


def material_creator(elements):
    """" Iterates over all materials in the string and appends them
    into one material vector which contains all isotopes present.

    args:
        material (str array): A string of the material name

    returns:
        material (double array): An array of all isotopes present in a material
        with all physical properties.
    """
    for i in range(len(elements)):
        cur_element = glob.glob(os.path.join(element_dir, elements[i] + '*'))
        # Determine if the element exists, if not kill the program and report message
        if not os.path.isfile(cur_element[0]):
            print('\n\033[1;37;31mFATAL ERROR: Element currently not supported. '
                  'Please create element or utilize a different material.'
                  'Element creator module can be found in /FRIDGE/Utilities')
            quit()
        # Obtain the first isotope from the file
        if i == 0:
            material = elem_at2wt_per(element_input([elements[i]]))
        # Obtain all other isotopes in the file
        else:
            material_2 = elem_at2wt_per(element_input([elements[i]]))
            material = np.concatenate((material, material_2))
    return material


def get_ZAID_row(mat, ZAID):
    """ Finds and returns the column of the ZAID from the given material

    args:
        mat (double array): The material array with all known isotopes present
        ZAID (double): The ZAID number that we are looking to find what column it is in

    returns:
        elem_col_temp[0] (int): The column number of our ZAID in question.
    """
    elem_col_temp = np.where(np.isin(mat, ZAID))
    if not elem_col_temp[1]:
        print('\n\033[1;37;31mFATAL ERROR: Element could not be found in material. '
              'Check material input and element files to determine if %s is missing' % ZAID)
        quit()
    else:
        return elem_col_temp[0]


def get_wt_per(material):
    """Determine the weight percent of each element in a material and return a vector

    args:
        material (str array): A string of the material name

    returns:
        wt_per_vec_temp (double array): get the weight percent for each
        element in the material (if applicable)

    """
    cur_material = glob.glob(os.path.join(material_dir, material[0] + '.*'))
    # Determine how many elements are in the material,
    with open(cur_material[0], "r") as mat_file:
        for i, line in enumerate(mat_file):
            if i == 2:
                num_mat_elem = sum(1 for x in line.split())
        wt_per_vec_temp = np.zeros((2, num_mat_elem))
    # Create the variables for the wt_per_vec
    with open(cur_material[0], "r") as mat_file:
        for i, line in enumerate(mat_file):
            # Calculate the wt% for each element
            if 1 < i < 4:
                temp = [x for x in line.split(' ')]
                # To Do: Figure out a way to check for a blank space as this trips it up
                for x in range(len(temp)):
                    wt_per_vec_temp[i-2][x] = temp[x]
            # Calculate the enrichment for unique isotopes
    return wt_per_vec_temp


def get_enr_per(material):
    """Determine the enrich percent of each element in a material and
       return a vector.

    args:
        material (str array): A string of the material name

    returns:
        enr_per_vec (double array): An array of the enriched isotopes that are present

    """
    cur_material = glob.glob(os.path.join(material_dir, material[0] + '.*'))
    # Determine how many isotopes are enriched
    with open(cur_material[0], "r") as mat_file:
        for i, line in enumerate(mat_file):
            if i == 4:
                num_enr_iso = sum(1 for x in line.split())
        enr_per_vec = np.zeros((2, num_enr_iso))
    if enr_per_vec != []:
        # Create the variables for the wt_per_vec
        with open(cur_material[0], "r") as mat_file:
            for i, line in enumerate(mat_file):
                # Calculate the enrichment for unique isotopes
                if 3 < i < 6:
                    temp = [x for x in line.split(' ')]
                    for x in range(len(temp)):
                        enr_per_vec[i-4][x] = temp[x]
    return enr_per_vec


def get_mat_attr(material):
    """Get the physical attributes associated with the material (which may be
    different than the constituent elements.

    This is the third step in the creating a material. It currently returns a 2x1 vector
    [0] = Density
    [1] = Linear Coefficient of Expansion

    args:
        material (str array): A string of the material name

    returns:
        att_vec (double array): Array with the known attributes for a material
    """
    cur_material = glob.glob(os.path.join(material_dir, material[0] + '.*'))
    # Determine the number of attr
    with open(cur_material[0], "r") as mat_file:
        for i, line in enumerate(mat_file):
            if i == 7:
                num_attr = sum(1 for x in line.split())
        attr_vec = np.zeros(num_attr)
    # Creates the vector of material properties
    with open(cur_material[0], "r") as mat_file:
        for i, line in enumerate(mat_file):
            if i == 7:
                temp = [x for x in line.split(' ')]
                for x in range(len(temp)):
                    attr_vec[x] = temp[x]
    return attr_vec


def wt_per_calc(elem_vec, wt_per_vec, enr_vec):
    """Calculates a final wt% from the enrichment vector and the weight percent
    vector.

    This is the fourth step in creating a material. If desired, the resulting
    vector is the weight percent of each isotope, which can be put directly
    into MCNP.

    args:
        elem_vec (double array): array with all elements in the material
        and their physical properties
        wt_per_vec (double array): array with all elements that need to be
        adjusted due to different weight percents than isotopic abundance
        enr_vec (double array): array with all isotopes that have some
        type of enrichment (typically fuel or CR material)

    returns:
        mat_elem_vec (double array): array with all isotopes present in
        the material (removes any isotopes that have 0 wt%) and their
        associated weight percent
    """
    # Checks to see if we have any materials that are enriched
    # If so, we create a temporary vector to hold them and all
    # of the elements data before we make a full vector with all
    # elements combined
    if enr_vec != []:
        enr_iso = len(enr_vec[0])
        temp_mat_elem_vec = np.zeros((enr_iso, 6))
        i = 0
        for x in enr_vec[i]:
            zaid_row = get_ZAID_row(elem_vec, x)
            for j, y in enumerate(elem_vec[zaid_row][0]):
                if j == 3:
                    temp_mat_elem_vec[i][j] = enr_vec[1][i]
                else:
                    temp_mat_elem_vec[i][j] = y
            i += 1
        # Creates a vector denoting which elements have already been created
        # with the enrichment vector
        z_enr_iso = np.zeros(len(enr_vec[0]))
        for y in range(len(enr_vec[0])):
            z_enr_iso_temp = str(enr_vec[0][y])
            z_enr_iso[y] = z_enr_iso_temp[:2] + "000"
        z_enr_iso = np.unique(z_enr_iso)

    # Loop over the element vector and determine what isotopes to keep
    # and what isotopes (the enriched) to leave out.
        mat_elem_vec = np.zeros((1, 6))
        for i in range(len(z_enr_iso)):
            for j in range(len(elem_vec)):
                if z_enr_iso[i] == elem_vec[j][0] or elem_vec[j][3] == 0:
                    pass
                elif i == 0:
                    vec_temp = [elem_vec[j][:]]
                    mat_elem_vec = np.concatenate((mat_elem_vec, vec_temp))
        mat_elem_vec = np.delete(mat_elem_vec, 0, 0)
        mat_elem_vec = np.concatenate((temp_mat_elem_vec, mat_elem_vec))
    else:
        mat_elem_vec = np.copy(elem_vec)
    # Multiplies the wt% of each element in the material by the
    # wt% of each isotope in the element to yield a total weight percent
    # which should sum to 1
    sum_wt = 0
    for i in range(len(wt_per_vec[0])):
        for j in range(len(mat_elem_vec)):
            if wt_per_vec[0][i] == mat_elem_vec[j][0]:
                mat_elem_vec[j][3] = mat_elem_vec[j][3] * wt_per_vec[1][i]
                sum_wt += mat_elem_vec[j][3]
    if round(sum_wt, 15) != 1.0:
        print('\033[1;37:33mWarning: Material with %s had a weight fraction of %f and was not normlized to 1. '
              'Check to make sure the material or element card is correct' % ([wt_per_vec[0][:]], sum_wt))

    return mat_elem_vec


def wt2at_per(wt_per, attr):
    """Converts the array of wt % to atom % and returns the atom density for use
       in the cell cards.

    The fifth step in getting a material.

    args:
        wt_per (double array): array with all isotopes present in
        the material in weight percent
        attr (double array): Array with the known attributes for a material

    returns:
        at_per (double array): array with all isotopes present in
        the material in atom percent
        atom_density (double): the total atom density for the material
    """
    at_den = np.zeros(len(wt_per))
    at_per = np.copy(wt_per)
    at_den_sum = 0
    at_per_sum = 0
    # Get the total atom density (to be used in the cell card and for the
    # atom percent)
    for i, isotope in enumerate(wt_per):
        at_den[i] = isotope[3] * attr[0] * AVOGADROS_NUMBER / isotope[2]
        at_den_sum += at_den[i]
    for i, isotope in enumerate(wt_per):
        at_per[i][3] = at_den[i] / at_den_sum
        at_per_sum += at_per[i][3]
    if round(at_per_sum, 15) != 1:
        print('\033[1;37;33mWARNING: The atom percent of %s was %f and not normalized to 1. '
              'Check element to determine error' % (at_per[:, 1], at_per_sum))
    return at_per, at_den_sum

def material_reader(material_input):
    """This function will be called from the driver and will create a data
    series for a material that is called.

    This combines all the other steps and will be the only function called
    from the main program.

    args:
        material_input (str array): An array of a known material

    returns:
        at_per (double array): array with all isotopes present in
        the material in atom percent
        atom_density (double): the total atom density for the material
    """
    material_elements = get_elem_string(material_input)
    material_base = material_creator(material_elements)
    material_attr = get_mat_attr(material_input)
    material_wt_per = get_wt_per(material_input)
    material_enr_per = get_enr_per(material_input)
    material_vector = wt_per_calc(material_base, material_wt_per,  material_enr_per)
    atom_percent, atom_density = wt2at_per(material_vector, material_attr)

    return atom_percent, atom_density


def get_final_wt_per(material_input):
    """This function will be called from the driver and will create a data
    series with weight percents for a material that is called.

    This combines all the other steps and will be the only function called
    from the main program.

    args:
        material_input (str array): An array of a known material

    returns:
        at_per (double array): array with all isotopes present in
        the material in atom percent
        atom_density (double): the total atom density for the material
    """
    material_elements = get_elem_string(material_input)
    material_base = material_creator(material_elements)
    material_attr = get_mat_attr(material_input)
    material_wt_per = get_wt_per(material_input)
    material_enr_per = get_enr_per(material_input)
    weight_percent = wt_per_calc(material_base, material_wt_per,  material_enr_per)

    return weight_percent, material_attr[0]

# Create a class for fuel/cladding/coolant/etc.
# it shoulid look something like
# class fuel:
#      isotopes
#      atom density
#      etc.
