import FRIDGe.material_reader as mat_read
import numpy as np
import os


def test_element_input():
    """This is a test for the element input reader. The input reader test three
     different cases. One with one isotope, one with two isotopes and one with
     four isotopes to check scalability."""

    # One isotope reader for Sodium
    cur_dir = os.path.dirname(__file__)
    elem_dir = os.path.join(cur_dir, '../CotN/Na.txt')
    elem = mat_read.element_input(elem_dir)
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
    elem_dir = os.path.join(cur_dir, '../CotN/V.txt')
    elem = mat_read.element_input(elem_dir)

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
    elem_dir = os.path.join(cur_dir, '../CotN/U.txt')
    elem = mat_read.element_input(elem_dir)

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
    PNNL-15870 REV. 1"""
    # One isotope reader for Sodium, note that no values should change
    # since we only have one isotope present.
    cur_dir = os.path.dirname(__file__)
    elem_dir = os.path.join(cur_dir, '../CotN/Na.txt')
    na_wt_per = mat_read.element_input(elem_dir)
    na_at_per = mat_read.elem_at2wt_per(na_wt_per)
    assert na_at_per[0][0] == 11000
    assert na_at_per[0][1] == 11023
    assert na_at_per[0][2] == 22.9897692820
    assert na_at_per[0][3] == 1.00
    assert na_at_per[0][4] == 0.968

    # Two isotope test for Vanadium.
    cur_dir = os.path.dirname(__file__)
    elem_dir = os.path.join(cur_dir, '../CotN/V.txt')
    v_at_per = mat_read.element_input(elem_dir)
    v_wt_per = mat_read.elem_at2wt_per(v_at_per)
    assert np.allclose(v_wt_per[0][3], 0.0024512)
    assert np.allclose(v_wt_per[1][3], 0.9975487)

    # Four isotope test for Uranium, where one isotope is not naturally occurring.
    cur_dir = os.path.dirname(__file__)
    elem_dir = os.path.join(cur_dir, '../CotN/U.txt')
    u_at_per = mat_read.element_input(elem_dir)
    u_wt_per = mat_read.elem_at2wt_per(u_at_per)
    assert np.allclose(u_wt_per[0][3], 0.0000531)
    assert np.allclose(u_wt_per[1][3], 0.0071137)
    assert np.allclose(u_wt_per[2][3], 0.0000000)
    assert np.allclose(u_wt_per[3][3], 0.9928332)

    # No naturally occuring isotope check for Pu.
    cur_dir = os.path.dirname(__file__)
    elem_dir = os.path.join(cur_dir, '../CotN/Pu.txt')
    pu_at_per = mat_read.element_input(elem_dir)
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
    cur_dir = os.path.dirname(__file__)

    # Material with 1 element (Sodium)
    elem_dir = os.path.join(cur_dir, '../CotN/')
    na_material = mat_read.material_creator(elem_dir, ["Na"])
    assert na_material[0][0] == 11000
    assert na_material[0][1] == 11023
    assert na_material[0][2] == 22.9897692820
    assert na_material[0][3] == 1.00
    assert na_material[0][4] == 0.968

    # Material with 2 elements (Uranium and Plutonium)
    elem_dir = os.path.join(cur_dir, '../CotN/')
    u_pu_material = mat_read.material_creator(elem_dir, ["U", "Pu"])
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
    elem_dir = os.path.join(cur_dir, '../CotN/')
    u_pu_material = mat_read.material_creator(elem_dir, ["U", "Pu", "V"])
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
    cur_dir = os.path.dirname(__file__)
    mat_u27 = os.path.join(cur_dir, '../Materials/27U.txt')
    u27 = mat_read.get_enr_per(mat_u27)
    assert u27[0][0] == 92235
    assert u27[0][1] == 92238
    assert u27[1][0] == 0.270
    assert u27[1][1] == 0.730

    # Find the enrichment percent for 20% Pu (94% 94239, 6% 94240)
    # 10% U (10% 92235, 90% 92238) 10%Zr
    pu20_10u_zr = os.path.join(cur_dir, '../Materials/20Pu_10U_10Zr.txt')
    puuzr_enr = mat_read.get_enr_per(pu20_10u_zr)
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
    cur_dir = os.path.dirname(__file__)

    # Material with 1 element (Uranium)
    mat_dir = os.path.join(cur_dir, '../Materials/27U.txt')
    u27_mat_attr = mat_read.get_mat_attr(mat_dir)
    assert u27_mat_attr[0] == 18.95

    # Material with 2 elements (Uranium/Zirconium)
    mat_dir = os.path.join(cur_dir, '../Materials/27U_10Zr.txt')
    u27z_mat_attr = mat_read.get_mat_attr(mat_dir)
    assert u27z_mat_attr[0] == 15.47

    # Material with 3 elements (Uranium/Zirconium)
    mat_dir = os.path.join(cur_dir, '../Materials/20Pu_10U_10Zr.txt')
    pu20u10z_mat_attr = mat_read.get_mat_attr(mat_dir)
    assert pu20u10z_mat_attr[0] == 15.77

    return

test_element_input()
test_elem_at2wt_per()
test_material_creator()
test_get_enr_per()
test_get_mat_attr()