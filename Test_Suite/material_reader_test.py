import FRIDGe.material_reader as mat_read
import os


def test_element_input():
    """This is a test for the element input reader. The input reader test three
     different cases. One with one isotope, one with two isotopes and one with
     four isotopes to check scalability."""

    # One element reader for Sodium
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
    return

test_element_input()
