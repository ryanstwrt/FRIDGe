import numpy as np
import os

avgdro_num = 0.60221409


# This function obtains the physical properties of each isotope present in a material
# Where the properties are as such
# [0] = ZAID; [1] = Mass Number; [2] = Isotopic Abundance; [3] = Density
# [4] = Coefficient of Expansion
# Mass Number & Isotopic abundance are reference from IAEA Live Chart of the Nuclides
# Density is reference from 'Nuclides & Isotopes Chart of the Nuclides' 17th Edition
def element_input(elem_path):
    """returns an array with the elements present"""
    # Allocate space for elements being added
    num_elements = int(sum(1 for line in open(elem_path) if line.rstrip()) - 3)
    element = np.zeros((num_elements, 6))
    sum_wt = 0
    with open(elem_path, "r") as mat_file:
        for i, line in enumerate(mat_file):
            mat_line = [x for x in line.split(' ')]
            if i == 1:
                isotope = mat_line[0]
            if i > 2:
                element[i-3][0] = isotope
                element[i-3][1] = mat_line[0]
                element[i-3][2] = mat_line[1]
                element[i-3][3] = mat_line[2]
                element[i-3][4] = mat_line[3]
                element[i-3][5] = mat_line[4]
            sum_wt += element[i-3][3]
        if sum_wt == 0:
            pass
        elif sum_wt != 1:
            print('WARNING: The weight of %s was %f and not normalized to 1. '
                  'Check element to determine error' % (elem_path[-6:], sum_wt))
    return element


# The material creator function iterates over all materials in the string
# and appends then into one material vector which will then be passed on to
# the atom density calculator
def material_creator(mat_str):
    """" Iterate over all isotopes from the material string """
    for i in range(len(mat_str)):
        elem_path = os.path.join(elem_dir, mat_str[i] + txt_ext)
        # Determine if the element exists, if not kill the program and report message
        if not os.path.isfile(elem_path):
            print('FATAL ERROR: Element currently not supported. '
                  'Please create element or utilize a different material.'
                  'Element creator module can be found in *********')
            quit()
        # Obtain the first isotope from the file
        if i == 0:
            material = elem_at2wt_per(element_input(elem_path))
        # Obtain all other isotopes in the file
        else:
            material_2 = elem_at2wt_per(element_input(elem_path))
            material = np.concatenate((material, material_2))
    return material


# Finds and returns the column of the ZAID from the given material
def get_ZAID_row(mat, ZAID):
    elem_col_temp = np.where(np.isin(mat, ZAID))
    if not elem_col_temp[1]:
        print('FATAL ERROR: Element could not be found in material. '
              'Check material input and element files to determine if %s is missing' % ZAID)
        quit()
    else:
        return elem_col_temp[0]


# Determine the weight percent of each element in a material and return a vector
def get_wt_per(path):
    # Determine how many elements are in the material,
    with open(path, "r") as mat_file:
        for i, line in enumerate(mat_file):
            if i == 2:
                num_mat_elem = sum(1 for x in line.split())
        wt_per_vec_temp = np.zeros((2, num_mat_elem))
    # Create the variables for the wt_per_vec
    with open(path, "r") as mat_file:
        for i, line in enumerate(mat_file):
            # Calculate the wt% for each element
            if 1 < i < 4:
                temp = [x for x in line.split(' ')]
                # To Do: Figure out a way to check for a blank space as this trips it up
                for x in range(len(temp)):
                    wt_per_vec_temp[i-2][x] = temp[x]
            # Calculate the enrichment for unique isotopes
    return wt_per_vec_temp


# Determine the enrich percent of each element in a material and return a vector
def get_enr_per(path):
    # Determine how many isotopes are enriched
    with open(path, "r") as mat_file:
        for i, line in enumerate(mat_file):
            if i == 4:
                num_enr_iso = sum(1 for x in line.split())
        enr_per_vec = np.zeros((2, num_enr_iso))
    # Create the variables for the wt_per_vec
    with open(path, "r") as mat_file:
        for i, line in enumerate(mat_file):
            # Calculate the enrichment for unique isotopes
            if 3 < i < 6:
                temp = [x for x in line.split(' ')]
                for x in range(len(temp)):
                    enr_per_vec[i-4][x] = temp[x]
    return enr_per_vec


# Get the physical attributes related to a material (if known)
def get_mat_attr(path):
    # Determine the number of attr
    with open(path, "r") as mat_file:
        for i, line in enumerate(mat_file):
            if i == 4:
                num_attr = sum(1 for x in line.split())
        attr_vec = np.zeros(num_attr)
    # Create the variables for the wt_per_vec
    with open(path, "r") as mat_file:
        for i, line in enumerate(mat_file):
            # Calculate the enrichment for unique isotopes
            if i == 7:
                temp = [x for x in line.split(' ')]
                for x in range(len(temp)):
                    attr_vec[x] = temp[x]
    return attr_vec


# Calculates a final wt% from the enrichment vector and the weight percent
# vector. The resulting vector is the weight percent of each isotope.
# This can be put directly into MCNP.
def wt_per_calc(elem_vec, wt_per_vec, enr_vec):
    # Checks to see if we have any materials that are enriched
    # If so, we create a temporary vector to hold them and all
    # of the elements data before we make a full vector with all
    # elements combined
    if enr_vec.size != 0:
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

    #print(mat_elem_vec)
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
        print('Warning: Material with %s had a weight fraction of %f and was not normlized to 1. '
              'Check to make sure the material or element card is correct' % (wt_per_vec[0][:], sum_wt))
    return mat_elem_vec


# Converts the original elemental data (which is from the Chart of the Nuclides)
# from atom percent to weight percent. This is to ensure everything is on =
# equal setting when working with wt% and enrichment.
def elem_at2wt_per(at_per):
    num_elem = int(sum(1 for i in enumerate(at_per)))
    wt_per = at_per
    mol_wt = 0
    wt_by_mass = np.zeros(num_elem)
    for i, x in enumerate(at_per):
        wt_by_mass[i] = x[2]*x[3]
        mol_wt += wt_by_mass[i]
    for i, x in enumerate(at_per):
        if mol_wt == 0:
            pass
        else:
            wt_per[i][3] = wt_by_mass[i] / mol_wt
    return at_per


# Converts the array of wt % to atom % and returns the atom density for use
# in the cell cards
def wt2at_per(wt_per, attr):
    at_den = np.zeros(len(wt_per))
    at_per = wt_per
    at_den_sum = 0
    at_per_sum = 0
    # Get the total atom density (to be used in the cell card and for the
    # atom percent)
    for i, x in enumerate(wt_per):
        at_den[i] = x[3] * attr[0] * avgdro_num / x[2]
        at_den_sum += at_den[i]
    for i, x in enumerate(wt_per):
        at_per[i][3] = at_den[i] / at_den_sum
        at_per_sum += at_per[i][3]
    if round(at_per_sum, 15) != 1:
        print('WARNING: The atom percent of %s was %f and not normalized to 1. '
              'Check element to determine error' % (at_per[:, 1], at_per_sum))
    return at_per, at_den_sum


# Requirements for the material reader
txt_ext = ".txt"
fuel_str = ["U", "Pu", "Zr"]

# Get the current working directory
cur_dir = os.path.dirname(__file__)
# Find the Material director, and the path to the specific element
elem_dir = os.path.join(cur_dir, 'CotN')
mat_dir = os.path.join(cur_dir, 'Materials')
mat_path = os.path.join(mat_dir, '20Pu_10U_10Zr.txt')

# Order in which material reader should be read
fuel = material_creator(fuel_str)
fuel_wt_per = get_wt_per(mat_path)
fuel_enr = get_enr_per(mat_path)
fuel_attr = get_mat_attr(mat_path)
mat_wt_per = wt_per_calc(fuel, fuel_wt_per, fuel_enr)
mat_at_per, mat_at_den = wt2at_per(mat_wt_per, fuel_attr)

#print(mat_wt_per)
print(mat_at_per)
#print(mat_at_den)

# Create a class for fuel/cladding/coolant/etc.
# it shoulid look something like
# class fuel:
#      isotopes
#      atom density
#      etc.
