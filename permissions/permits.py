class PermitFactory(object):
    """ Creates and manages permits """

    permits = []
    active = []

    @staticmethod
    def new(name):
        if name not in PermitFactory.permits:
            PermitFactory.permits.append(name)

    @staticmethod
    def activate(name):
        if name not in PermitFactory.active:
            PermitFactory.active.append(name)
            return name
        return None

    @staticmethod
    def deactivate(name):
        if name in PermitFactory.active:
            PermitFactory.active.remove(name)
            return name
        return None

class add_permits(object):
    def __init__(self, *permit_list):
        self.permit_list = permit_list[:]

    def __call__(self, fxn):
        def wrapper(*args, **kwargs):
            # activate permits
            for p in self.permit_list:
                PermitFactory.new(p)
            activated_permits = list(filter(None, [PermitFactory.activate(name) for name in self.permit_list]))

            try:
                r = fxn(*args, **kwargs)
            except PermissionError as e:
                # deactivate permits
                for d in activated_permits:
                    PermitFactory.deactivate(d)
                raise e
            # deactivate permits
            for d in activated_permits:
                PermitFactory.deactivate(d)
            return r
        return wrapper


class assign_permits(object):
    def __init__(self, *permit_list):
        self.permit_list = permit_list[:]

    def __call__(self, fxn):
        def wrapper(*args, **kwargs):
            # activate permits
            activated_permits = PermitFactory.active[:]
            PermitFactory.active = self.permit_list[:]

            try:
                r = fxn(*args, **kwargs)
            except PermissionError as e:
                # deactivate permits
                for d in activated_permits:
                    PermitFactory.deactivate(d)
                raise e

            # reactivate permits
            PermitFactory.active = activated_permits
        return wrapper

class require_permits(object):
    def __init__(self, *permit_list, method="all"):
        self.permit_list = permit_list[:]
        self.method = method

    def __call__(self, fxn):
        def wrapper(*args, **kwargs):
            x = [permit in PermitFactory.active for permit in self.permit_list]
            p = False
            if self.method == "all":
                p = all(x)
            elif self.method == "any":
                p = any(x)
            if p:
                r = fxn(*args, **kwargs)
                return r
            else:
                raise PermissionError("Fxn {0} does not have the permits required to call. Requires {2} but has {1}."
                                      .format(fxn, PermitFactory.active, self.permit_list))

        return wrapper

class Foo(object):

    def __init__(self):
        pass

    @require_permits("1", "2")
    def r12(self):
        pass

    @require_permits("bar")
    def rbar(self):
        pass

    @add_permits("1")
    def foo1(self):
        self.foo2()

    @add_permits("2")
    def foo2(self):
         self.r12()

class Bar(object):

    def __init__(self):
        pass

    @add_permits("bar")
    def callrbar(self, foo):
        foo.rbar()

f = Foo()
b = Bar()

print(PermitFactory.active)
f.foo1()
print(PermitFactory.active)
import pytest
with pytest.raises(PermissionError):
    f.foo2()
with pytest.raises(PermissionError):
    f.r12()
b.callrbar(f)
print(PermitFactory.active)
with pytest.raises(PermissionError):
    f.rbar()
print(PermitFactory.active)
