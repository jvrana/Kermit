# from permissions.permits import *
from permissions.permission_wrappers import *
import pytest


# requires_any_permits(*permit_list)

def test_simple_permission():
    class Foo(object):
        def __init__(self, name):
            self.__name = name

        @add_permits("Global")
        def single_permit(self):
            print("single_permit called!")
            self.needs_single_permit()

        @require_permits("Global")
        def needs_single_permit(self):
            print("needs_single_permit called!")

        @add_permits("Global", "Local", "Extra")
        def multi_permits(self):
            print("multi_permits called!")
            self.needs_multi_permits()

        @require_permits("Local", "Extra", "Global")
        def needs_multi_permits(self):
            print("needs_multi_permits called!")

        def cant_call_single_permit(self):
            print("cant_call_single_permit called!")
            self.needs_single_permit()

        def cant_call_multi_permit(self):
            print("cant_call_multi_permit called!")
            self.needs_multi_permits()

    f = Foo("example")

    # Calling instance methods with permits is OK
    f.single_permit()
    f.multi_permits()

    # Cannot globally call needs_single_permit
    with pytest.raises(PermissionError):
        f.needs_single_permit()

    # Cannot globally call needs_multi_permit
    with pytest.raises(PermissionError):
        f.needs_multi_permits()

    # instance method cannot call single permit
    with pytest.raises(PermissionError):
        f.cant_call_single_permit()

    # instance method cannot call multi permit
    with pytest.raises(PermissionError):
        f.cant_call_multi_permit()

    # Assert instance is returned to normal
    assert len(PermitFactory.get_permits(f)) == 0

    # Assert instance class is returned to normal
    methods = [f.cant_call_single_permit, f.cant_call_multi_permit, f.needs_multi_permits, f.needs_single_permit]
    for i, m in enumerate(methods):
        try:
            m()
        except PermissionError as e:
            # print(e)
            pass
        assert len(PermitFactory.get_permits(f)) == 0


def test_for_remenant_permits_after_errors():
    class Foo(object):
        def __init__(self):
            pass

        @require_permits("Global")
        def needs_permit_but_raises_error(self):
            raise ValueError("needs_permit_but_raises_error error was raised")

        @add_permits("Global")
        def calls_errored_method(self):
            self.needs_permit_but_raises_error()

        @add_permits("Global")
        def calls_errored_method_but_itself_errors(self):
            raise ValueError("calls_errored_method_but_itself_errors error was raised")
            self.needs_permit_but_raises_error

        @add_permits("Global")
        def simply_reference_function(self):
            self.needs_permit_but_raises_error

    f = Foo()
    methods = [f.calls_errored_method, f.calls_errored_method_but_itself_errors, f.simply_reference_function]
    for i, m in enumerate(methods):
        try:
            m()
        except ValueError as e:
            print(e)
            # pass
        assert len(PermitFactory.get_permits(f)) == 0


def test_not_enough_permits():
    class Foo(object):
        def __init__(self):
            pass

        @require_permits("Local", "Extra", "Global")
        def needs_multi_permits(self):
            print("needs_multi_permits called!")

        @add_permits("Global", "Local")
        def not_enough_permits(self):
            self.needs_multi_permits()

    f = Foo()
    # Test if method does not have enough permits
    with pytest.raises(PermissionError):
        f.not_enough_permits()

def test_any():
    class Foo(object):
        def __init__(self):
            pass

        @require_permits("Local", "Global", method="any")
        def require_any(self):
            pass

        @add_permits("Global")
        def has_global(self):
            self.require_any()

        @add_permits("Local")
        def has_local(self):
            self.require_any()

        @add_permits("Extra")
        def isnt_allowed_for_any(self):
            self.require_any()

    f = Foo()
    # Require any permits
    f.has_local()
    f.has_global()
    with pytest.raises(PermissionError):
        f.isnt_allowed_for_any()

def test_inheritance():
    class Foo(object):
        def __init__(self):
            pass

        def get_permits(self):
            return PermitFactory.get_permit_names(self)

        @add_permits("1")
        def foo1(self):
            assert self.get_permits() == ["1"]
            self.r1()
            self.foo12()

        @add_permits("2")
        def foo12(self):
            assert self.get_permits() == ["1", "2"]
            self.r1()
            self.r2()
            self.r12()
            self.foo123()

        @add_permits("3")
        def foo123(self):
            assert self.get_permits() == ["1", "2", "3"]
            self.r123()

        @require_permits("1")
        def r1(self):
            pass

        @require_permits("2")
        def r2(self):
            pass

        @require_permits("1", "2")
        def r12(self):
            pass

        @require_permits("1", "2", "3")
        def r123(self):
            pass

    f = Foo()
    f.foo1()

def test_assign_inheritance():
    class Foo(object):
        def __init__(self):
            pass

        def foo(self):
            pass

        def get_permits(self):
            return PermitFactory.get_permit_names(self)

        @assign_permits("1")
        def foo1(self):
            assert self.get_permits() == ["1"]
            self.r1()
            self.foo2()

        @assign_permits("2")
        def foo2(self):
            assert self.get_permits() == ["2"]
            self.r2()
            self.foo3()

        @assign_permits("3")
        def foo3(self):
            assert self.get_permits() == ["3"]
            self.r3()

        @assign_permits("4")
        def foo4_will_error(self):
            self.foo5()

        @assign_permits("5")
        def foo5(self):
            self.r4()

        @require_permits("1")
        def r1(self):
            pass

        @require_permits("2")
        def r2(self):
            pass

        @require_permits("3")
        def r3(self):
            pass

        @require_permits("4")
        def r4(self):
            pass

    f = Foo()
    f.foo1()
    with pytest.raises(PermissionError):
        f.foo4_will_error()