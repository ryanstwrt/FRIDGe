from FRIDGe.fridge.driver import pin_maker as pm

def test_mcnp_macro_RCC():
    output, warning = pm.mcnp_make_macro_RCC(1, [0,0,0], [0,0,10], 0.5, 'Testing to make sure')
    assert len(output) < 80
    assert warning == False
    output, warning = pm.mcnp_make_macro_RCC(1, [0,0,0], [0,0,10], 0.5, 'Testing to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True


def test_mcnp_macro_RHP():
    output, warning = pm.mcnp_make_macro_RCC(1, [0,0,0], [0,0,10], [0, 0.5, 0], 'Testing to make sure')
    assert len(output) < 80
    assert warning == False
    output, warning = pm.mcnp_make_macro_RCC(1, [0,0,0], [0,0,10], [0, 0.5, 0], 'Testing to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True

def test_mcnp_make_concentric_cell():
    output, warning = pm.mcnp_make_concentric_cell(1, 10, 0.95, 10, 11, 1, 1, 'Test to make sure')
    assert len(output) < 80
    assert warning == False

    output, warning = pm.mcnp_make_concentric_cell(1, 10, 0.95, 10, 11, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True

def test_mcnp_make_cell():
    output, warning = pm.mcnp_make_cell(1, 10, 0.95, 10, 1, 1, 'Test to make sure')
    assert len(output) < 80
    assert warning == False

    output, warning = pm.mcnp_make_cell(1, 10, 0.95, 10, 1, 1, 'Test to make sure it will be longer than 80 characters so it will fail the test')
    assert warning == True

test_mcnp_macro_RCC()
test_mcnp_macro_RHP()