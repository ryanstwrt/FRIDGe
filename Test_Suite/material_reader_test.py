import FRIDGe.material_reader as mat_read
import os


def test_element_input():
    """This is a test for the element input reader. The input reader test three
     different cases. One with one isotope, one with two isotopes and one with
     four isotopes to check scalability."""

    # One isotope reader for Sodium
    cur_dir = os.path.dirname(__file__)
    elem_dir = os.path.join(cur_dir, '../CotN/Na.txt')
    elem = mat_read.element_input(elem_dir)
    na_elem_num = 23000
    na_zaid = 23023
    na_mass_num = 22.9897692820
    na_abun = 1.00
    na_density = 0.968
    assert na_elem_num == elem[0][0]
    assert na_zaid == elem[0][1]
    assert na_mass_num == elem[0][2]
    assert na_abun == elem[0][3]
    assert na_density == elem[0][4]

    # Two isotope reader for

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

test_element_input()
