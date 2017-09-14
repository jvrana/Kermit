from permissions.permits import *

import pytest

@pytest.fixture(scope="function")
def example_class():
    class Thing(object):

        def __init__(self, name):
            self.__name = name

        @property
        def name(self):
            return self.__name
    return Thing

def test_permit():
    Permit.name == "Permit"

def test_permit_factory():
    permit_name = "KermitThePermit"
    p1 = PermitFactory.new(permit_name)
    p2 = PermitFactory.new(permit_name)
    assert p1 is p2
    assert permit_name in PermitFactory.permits
    assert p1.name() == permit_name
    assert(p1.get_class().__bases__[0] == Permit)
    assert Permit.is_a_permit(p1)
    assert not Permit.is_a_permit(5.0)

def test_class_mutator(example_class):
    pf = PermitFactory
    g = PermitFactory.new("Global")
    l = PermitFactory.new("Local")

    # Testing for adding and removing base classes
    t = example_class("Thing1")
    assert not pf.has_base_class(t, g)
    assert not pf.has_base_class(t, l)
    assert example_class == t.__class__

    # Add classes
    pf.add_base_class(t, g)
    pf.add_base_class(t, l)
    assert pf.has_base_class(t, g)
    assert pf.has_base_class(t, l)
    assert not example_class == t.__class__

    # Confirm methods exist
    print(t.name)

    # Remove Classes
    pf.remove_base_class(t, l)
    assert not pf.has_base_class(t, l)
    pf.remove_base_class(t, g)
    assert not pf.has_base_class(t, g)
    assert t.__class__ == example_class

    pf.add_base_class(t, g)
    pf.add_base_class(t, l)
    print(t.__class__.__name__)

def test_add_permits(example_class):
    pf = PermitFactory
    t = example_class("SomeName")
    g = pf.add_permit(t, "Global")
    pf.has_base_class(t, pf.permits["Global"])
    pf.has_permit(t, "Global")

    # has new permit
    l = pf.add_permit(t, "Local")
    pf.has_base_class(t, pf.permits["Local"])
    pf.has_permit(t, "Local")

    # has old permit
    pf.has_base_class(t, pf.permits["Global"])
    pf.has_permit(t, "Global")

    permits = pf.get_permits(t)
    assert g in permits
    assert l in permits
    assert len(permits) == 2

    permit_names = pf.get_permit_names(t)
    assert "Global" in permit_names
    assert "Local" in permit_names
    assert len(permit_names) == 2

def test_destroy_permits(example_class):
    pf = PermitFactory
    t = example_class("SomeName")
    pf.add_permit(t, "Global")
    pf.add_permit(t, "Local")
    pf.add_permit(t, "WithinClass")
    pf.destroy_all_permits(t)
    assert len(pf.get_permits(t)) == 0

def test_remove_permits(example_class):
    pf = PermitFactory
    t = example_class("GitFurMit4MiPermit")
    pf.add_permit(t, "Global")
    pf.add_permit(t, "Local")
    pf.add_permit(t, "WithinClass")
    pf.remove_permits(t, ["Global", "Local"])
    assert len(pf.get_permits(t)) == 1
    assert pf.has_permit(t, "WithinClass")

    with pytest.raises(PermitError):
        pf.remove_permit(t, "SomePermitThatDoesntExist")

def test_add_multiple_premits(example_class):
    pf = PermitFactory
    t = example_class("SirGermitTheFlermigermitThe3rd")
    pf.add_permits(t, ["Global", "Global", "Local", "Local"])
    pf.remove_permits(t, ["Local", "Local"])
