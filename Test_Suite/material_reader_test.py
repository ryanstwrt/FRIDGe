import FRIDGe.material_reader as mat_read
import numpy as np
import os


def test_get_element_string():
    """Tests the ability to get the element string from the material file."""
    # Test a single element material
    element_string = mat_read.get_elem_string(["Liquid_Na"])
    assert element_string[0] == "Na"

    # Test a multi element material
    element_string = mat_read.get_elem_string(["20Pu_10U_10Zr"])

    assert element_string[0] == "U"
    assert element_string[1] == "Pu"
    assert element_string[2] == "Zr"


def test_element_input():
    """This is a test for the element input reader. The input reader test three
     different cases. One with one isotope, one with two isotopes and one with
     four isotopes to check scalability."""

    # One isotope reader for Sodium
    elem = mat_read.element_input(["Na"])
    na_elem_num = 11000
    na_zaid = 11023
    na_mass_num = 22.9897692820
    na_abun = 1.00
    na_density = 0.968
    assert na_elem_num == elem[0][0]
    assert na_zaid == elem[0][1]
    assert na_mass_num == elem[0][2]
    assert na_abun == elem[0][3]
    assert na_density == elem[0][4]

    # Two isotope reader for Vanadium
    elem = mat_read.element_input(["V"])

    # Check element number
    assert elem[0][0] == 23000
    # Check ZAID number
    assert elem[0][1] == 23050
    assert elem[1][1] == 23051
    # Check mass number
    assert elem[0][2] == 49.9471558
    assert elem[1][2] == 50.9439569
    # Check natural abundance
    assert elem[0][3] == 0.0025
    assert elem[1][3] == 0.9975
    # Check element density
    assert elem[0][4] == 6.11


    # Multi isotope reader for Uranium
    elem = mat_read.element_input(["U"])

    # Check element number
    assert elem[0][0] == 92000
    # Check ZAID number
    assert elem[0][1] == 92234
    assert elem[1][1] == 92235
    assert elem[2][1] == 92236
    assert elem[3][1] == 92238
    # Check mass number
    assert elem[0][2] == 234.0409504
    assert elem[1][2] == 235.0439282
    assert elem[2][2] == 236.0455662
    assert elem[3][2] == 238.0507870
    # Check natural abundance
    assert elem[0][3] == 0.000054
    assert elem[1][3] == 0.007204
    assert elem[2][3] == 0.000000
    assert elem[3][3] == 0.992742
    # Check element density
    assert elem[0][4] == 18.95

    return


def test_elem_at2wt_per():
    """ This is a test for the atom percent to weight percent function for
    individual element. The same elements from the previous test will be used
    for this test. In addition to those, Pu is also tested to determine
    the functions ability to process elements with no naturally occurring
    isotopes. For sodium and uranium, the values were varified against the
    'Compendium of Material Composition Data for Radiation Transport Modeling'
    PNNL-15870 REV. 1' """
    # One isotope reader for Sodium, note that no values should change
    # since we only have one isotope present.
    na_at_per = mat_read.element_input(["Na"])
    na_wt_per = mat_read.elem_at2wt_per(na_at_per)
    assert na_wt_per[0][0] == 11000
    assert na_wt_per[0][1] == 11023
    assert na_wt_per[0][2] == 22.9897692820
    assert na_wt_per[0][3] == 1.00
    assert na_wt_per[0][4] == 0.968

    # Two isotope test for Vanadium.
    v_at_per = mat_read.element_input(["V"])
    v_wt_per = mat_read.elem_at2wt_per(v_at_per)
    assert np.allclose(v_wt_per[0][3], 0.0024512)
    assert np.allclose(v_wt_per[1][3], 0.9975487)

    # Four isotope test for Uranium, where one isotope is not naturally occurring.
    u_at_per = mat_read.element_input(["U"])
    u_wt_per = mat_read.elem_at2wt_per(u_at_per)
    assert np.allclose(u_wt_per[0][3], 0.0000531)
    assert np.allclose(u_wt_per[1][3], 0.0071137)
    assert np.allclose(u_wt_per[2][3], 0.0000000)
    assert np.allclose(u_wt_per[3][3], 0.9928332)

    # No naturally occuring isotope check for Pu.
    pu_at_per = mat_read.element_input(["Pu"])
    pu_wt_per = mat_read.elem_at2wt_per(pu_at_per)
    assert np.allclose(pu_wt_per[0][3], 0.000)
    assert np.allclose(pu_wt_per[1][3], 0.000)
    assert np.allclose(pu_wt_per[2][3], 0.000)
    assert np.allclose(pu_wt_per[3][3], 0.000)
    assert np.allclose(pu_wt_per[4][3], 0.000)
    return


def test_material_creator():
    """ This is a test of the material creator function which reads in
    elements from the CotN, performs a atom percent to weight percent
    calculation and creates an array of them. The test will test
    a material with 1, 2 and 3 elements present. This test accumulates the
    previous two test functions and ensures they work together and create
    one material file."""
    # Material with 1 element (Sodium)
    na_material = mat_read.material_creator(["Na"])
    assert na_material[0][0] == 11000
    assert na_material[0][1] == 11023
    assert na_material[0][2] == 22.9897692820
    assert na_material[0][3] == 1.00
    assert na_material[0][4] == 0.968

    # Material with 2 elements (Uranium and Plutonium)
    u_pu_material = mat_read.material_creator(["U", "Pu"])
    assert u_pu_material[1][0] == 92000
    assert u_pu_material[1][1] == 92235
    assert u_pu_material[1][2] == 235.0439282
    assert np.allclose(u_pu_material[1][3], 0.0071137)
    assert u_pu_material[1][4] == 18.95
    assert u_pu_material[2][3] == 0.00
    assert np.allclose(u_pu_material[3][3], 0.9928332)
    assert u_pu_material[4][3] == 0.00
    assert u_pu_material[5][3] == 0.00
    assert u_pu_material[6][3] == 0.00
    assert u_pu_material[7][3] == 0.00
    assert u_pu_material[8][3] == 0.00

    # Material with 3 elements (Uranium, Plutonium and Vanadium)
    u_pu_material = mat_read.material_creator(["U", "Pu", "V"])
    assert u_pu_material[1][0] == 92000
    assert u_pu_material[1][1] == 92235
    assert u_pu_material[1][2] == 235.0439282
    assert np.allclose(u_pu_material[1][3], 0.0071137)
    assert u_pu_material[1][4] == 18.95
    assert u_pu_material[2][3] == 0.00
    assert np.allclose(u_pu_material[3][3], 0.9928332)
    assert u_pu_material[4][0] == 94000
    assert u_pu_material[4][3] == 0.00
    assert u_pu_material[5][3] == 0.00
    assert u_pu_material[6][3] == 0.00
    assert u_pu_material[7][3] == 0.00
    assert u_pu_material[8][3] == 0.00
    assert u_pu_material[8][4] == 19.84
    assert u_pu_material[9][0] == 23000
    assert np.allclose(u_pu_material[9][3], 0.0024512)
    assert np.allclose(u_pu_material[10][3], 0.9975487)
    assert u_pu_material[9][4] == 6.11
    return


def test_get_enr_per():
    """Test of the get enrichment percent function, which looks a given
    material card and determines the enrichment which will be applied
    to the materials at a later point."""

    # Find the enrichment percent for 27% Enriched Urranium
    u27 = mat_read.get_enr_per(["27U"])
    assert u27[0][0] == 92235
    assert u27[0][1] == 92238
    assert u27[1][0] == 0.270
    assert u27[1][1] == 0.730

    # Find the enrichment percent for 20% Pu (94% 94239, 6% 94240)
    # 10% U (10% 92235, 90% 92238) 10%Zr
    puuzr_enr = mat_read.get_enr_per(["20Pu_10U_10Zr"])
    assert puuzr_enr[0][0] == 92235
    assert puuzr_enr[0][1] == 92238
    assert puuzr_enr[0][2] == 94239
    assert puuzr_enr[0][3] == 94240
    assert puuzr_enr[1][0] == 0.100
    assert puuzr_enr[1][1] == 0.900
    assert puuzr_enr[1][2] == 0.940
    assert puuzr_enr[1][3] == 0.060

    return


def test_get_mat_attr():
    """This is a test of the get material attributes function which
    scans the material card and pulls out information such as the density
    """
    # Material with 1 element (Uranium)
    u27_mat_attr = mat_read.get_mat_attr(["27U"])
    assert u27_mat_attr[0] == 18.95

    # Material with 2 elements (Uranium/Zirconium)
    u27z_mat_attr = mat_read.get_mat_attr(["27U_10Zr"])
    assert u27z_mat_attr[0] == 15.47

    # Material with 3 elements (Uranium/Zirconium)
    pu20u10z_mat_attr = mat_read.get_mat_attr(["20Pu_10U_10Zr"])
    assert pu20u10z_mat_attr[0] == 15.77

    return


def test_wt_per_cal():
    cur_dir = os.path.dirname(__file__)

    # Material with 1 element (Sodium)
    na_material = mat_read.material_creator(["Na"])
    liquid_na_mat_attr = mat_read.get_wt_per(["Liquid_Na"])
    liquid_na_mat_vector = mat_read.wt_per_calc(na_material, liquid_na_mat_attr)

    # Check sodiums new material vector (should be the same)
    assert liquid_na_mat_vector[0][0] == 11000
    assert liquid_na_mat_vector[0][1] == 11023
    assert liquid_na_mat_vector[0][2] == 22.989769282
    assert liquid_na_mat_vector[0][3] == 1.00
    assert liquid_na_mat_vector[0][4] == 0.968

    # Material with 1 element (enriched)
    u27_material = mat_read.material_creator(["U"])
    u27_mat_attr = mat_read.get_wt_per(["27U"])
    u27_enr = mat_read.get_enr_per(["27U"])
    u27_mat_vector = mat_read.wt_per_calc(u27_material, u27_mat_attr, enr_vec=u27_enr)

    # Check for U-235
    assert u27_mat_vector[0][0] == 92000
    assert u27_mat_vector[0][1] == 92235
    assert u27_mat_vector[0][2] == 235.0439282
    assert u27_mat_vector[0][3] == 0.2700
    assert u27_mat_vector[0][4] == 18.95
    # Check for U-238
    assert u27_mat_vector[1][0] == 92000
    assert u27_mat_vector[1][1] == 92238
    assert u27_mat_vector[1][2] == 238.0507870
    assert u27_mat_vector[1][3] == 0.73
    assert u27_mat_vector[1][4] == 18.95

    # Material with 1 element (enriched)
    pu10_10u_material = mat_read.material_creator(["U", "Pu", "Zr"])
    pu10_10u_mat_attr = mat_read.get_wt_per(["20Pu_10U_10Zr"])
    pu10_10u_enr = mat_read.get_enr_per(["20Pu_10U_10Zr"])
    pu10_10u_mat_vector = mat_read.wt_per_calc(pu10_10u_material, pu10_10u_mat_attr, enr_vec=pu10_10u_enr)

    # Check for U-235
    assert pu10_10u_mat_vector[0][0] == 92000
    assert pu10_10u_mat_vector[0][1] == 92235
    assert pu10_10u_mat_vector[0][2] == 235.0439282
    assert np.allclose(pu10_10u_mat_vector[0][3], 0.07)
    assert pu10_10u_mat_vector[0][4] == 18.95
    # Check for U-238
    assert pu10_10u_mat_vector[1][0] == 92000
    assert pu10_10u_mat_vector[1][1] == 92238
    assert pu10_10u_mat_vector[1][2] == 238.0507870
    assert pu10_10u_mat_vector[1][3] == 0.63
    assert pu10_10u_mat_vector[1][4] == 18.95
    # Check for Pu-239
    assert pu10_10u_mat_vector[2][0] == 94000
    assert pu10_10u_mat_vector[2][1] == 94239
    assert pu10_10u_mat_vector[2][2] == 239.0521617
    assert pu10_10u_mat_vector[2][3] == 0.188
    assert pu10_10u_mat_vector[2][4] == 19.84
    # Check for Pu-240
    assert pu10_10u_mat_vector[3][0] == 94000
    assert pu10_10u_mat_vector[3][1] == 94240
    assert pu10_10u_mat_vector[3][2] == 240.0538118
    assert pu10_10u_mat_vector[3][3] == 0.012
    assert pu10_10u_mat_vector[3][4] == 19.84
    # Check all Zr isotopes are present
    zr_zaid = 40090
    for i, x in enumerate(pu10_10u_mat_vector[:, 1]):
        if i > 3 and i != 7:
            assert pu10_10u_mat_vector[3][1] == 94240
    # Check one Zr isotope's weight percent
    assert np.allclose(pu10_10u_mat_vector[4][3], 0.050706)
    return


def test_wt2at_per():
    """Test the weight percent to atom percent function for three different
    materials; sodium, LEU, and 20% Pu 80% U and 10% Zr. LEU was verified
    against the 'Compendium of Material Composition Data for Radiation
    Transport Modeling PNNL-15870 REV. 1' """
    cur_dir = os.path.dirname(__file__)

    # Material with 1 element (Sodium)
    elem_dir = os.path.join(cur_dir, '../CotN/')
    liquid_na_path = os.path.join(cur_dir, '../Materials/Liquid_Na.txt')

    na_material = mat_read.material_creator(["Na"])
    liquid_na_mat_wt_per = mat_read.get_wt_per(["Liquid_Na"])
    liquid_na_mat_attr = mat_read.get_mat_attr(["Liquid_Na"])
    liquid_na_mat_vector = mat_read.wt_per_calc(na_material, liquid_na_mat_wt_per)
    na_atom_vec, na_atom_density = mat_read.wt2at_per(liquid_na_mat_vector, liquid_na_mat_attr)

    assert np.allclose(na_atom_density, 0.024282647)
    assert na_atom_vec[0][3] == 1.0

    # Material with 1 element (enriched)
    elem_dir = os.path.join(cur_dir, '../CotN/')
    leu_material = mat_read.material_creator(["U"])
    leu_path = os.path.join(cur_dir, '../Materials/LEU.txt')
    leu_wt_per = mat_read.get_wt_per(["LEU"])
    leu_mat_attr = mat_read.get_mat_attr(["LEU"])
    leu_enr = mat_read.get_enr_per(["LEU"])
    leu_mat_vector = mat_read.wt_per_calc(leu_material, leu_wt_per, enr_vec=leu_enr)
    leu_atom_vector, leu_atom_density = mat_read.wt2at_per(leu_mat_vector, leu_mat_attr)

    assert np.allclose(leu_atom_density, 0.047944)
    assert np.isclose(leu_atom_vector[0][3], 0.000271, atol=0.000001)
    assert np.allclose(leu_atom_vector[1][3], 0.030372)
    assert np.allclose(leu_atom_vector[2][3], 0.000139, atol=0.000001)
    assert np.allclose(leu_atom_vector[3][3], 0.969217)

    # Material with 3 elements (two enriched)
    elem_dir = os.path.join(cur_dir, '../CotN/')
    upuzr_material = mat_read.material_creator(["U", "Pu", "Zr"])
    upuzr_path = os.path.join(cur_dir, '../Materials/20Pu_10U_10Zr.txt')
    upuzr_wt_per = mat_read.get_wt_per(["20Pu_10U_10Zr"])
    upuzr_mat_attr = mat_read.get_mat_attr(["20Pu_10U_10Zr"])
    upuzr_enr = mat_read.get_enr_per(["20Pu_10U_10Zr"])
    upuzr_mat_vector = mat_read.wt_per_calc(upuzr_material, upuzr_wt_per, enr_vec=upuzr_enr)
    upuzr_atom_vector, upuzr_atom_density = mat_read.wt2at_per(upuzr_mat_vector, upuzr_mat_attr)

    assert np.allclose(upuzr_atom_density, 0.0463159)
    assert np.isclose(upuzr_atom_vector[0][3], 0.061066, atol=0.000001)
    assert np.allclose(upuzr_atom_vector[1][3], 0.542654, atol=0.000001)
    assert np.allclose(upuzr_atom_vector[2][3], 0.161257, atol=0.000001)
    assert np.allclose(upuzr_atom_vector[3][3], 0.010250, atol=0.000001)
    assert np.allclose(upuzr_atom_vector[4][3], 0.115646, atol=0.000001)

    return


test_get_element_string()
test_element_input()
test_elem_at2wt_per()
test_material_creator()
test_get_enr_per()
test_get_mat_attr()
test_wt_per_cal()
test_wt2at_per()
