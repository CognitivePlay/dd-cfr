from dd_cfr.nestedmodule import nestedfile


def test_all():
    nestedfile.nestedfunc()

    nc = nestedfile.NestedClass(1)
    assert nc.get_x() == 1

    nchild = nestedfile.NestedChild()
    assert nchild.get_x() == 123
    nchild.derived()
    nchild.derived_static()
    nestedfile.NestedChild.derived_static()
