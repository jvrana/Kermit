class PermitError(Exception):
    """ Generic Permit error """
    def __init__(self, msg):
        self.msg = msg

class Permit(object):
    """ Designates a permission group """
    @classmethod
    def name(cls):
        return cls.__name__

    @classmethod
    def get_class(cls):
        """ Converts the type (cls) to a class """
        class Foo(object):
            def __init__(self):
                pass
        x = Foo()
        x.__class__ = cls
        return x.__class__

    @staticmethod
    def is_a_permit(other):
        return hasattr(other, "get_class") and other.get_class().__bases__[0] == Permit

class ClassMutator:
    """ Methods for adding and removing base classes """
    @staticmethod
    def add_base_classes(x, newclasses):
        """ Adds newclasses to list of base classes. Creates a new class for the instance. Original class is in
        bases[0] """
        bases = list(x.__class__.__bases__)
        if bases[0] is object:
            bases[0] = x.__class__
        if any(x in bases for x in newclasses):
            raise PermitError("Cannot insert duplicate classes.")
        bases = bases + newclasses
        x.__class__ = type(x.__class__.__name__, tuple(bases), x.__dict__)
        return newclasses

    @staticmethod
    def remove_base_class(x, cls):
        """ Removes base classes. If there are no more base classes, returns the original class slotted at bases[0] """
        bases = list(x.__class__.__bases__)
        original_class = bases[0]
        other_classes = bases[1:]
        if cls in other_classes:
            other_classes.remove(cls)
        else:
            raise PermitError("Class {0} not in list of base classes {1}".format(cls, bases))
        if len(other_classes) == 0:
            x.__class__ = original_class
        else:
            x.__class__ = type(x.__class__.__name__, tuple([original_class] + other_classes), x.__dict__)
        return cls

    @staticmethod
    def add_base_class(x, newclass):
        return ClassMutator.add_base_classes(x, [newclass])[0]

    @staticmethod
    def has_base_class(x, cls):
        return cls in x.__class__.__bases__

class PermitFactory(ClassMutator):
    """ Creates and manages permits """

    permits = {}

    @staticmethod
    def new(name):
        if name in PermitFactory.permits:
            return PermitFactory.permits[name]
        else:
            PermitFactory.permits[name] = type(name, (Permit,), {})
            # globals().update(PermitFactory.permits)
            return PermitFactory.permits[name]

    @staticmethod
    def get(name):
        if name not in PermitFactory.permits:
            raise PermitError("Permit \"{0}\" not in PermitFactory permit list".format(name))
        return PermitFactory.permits[name]

    @staticmethod
    def add_permits(instance, permit_names):
        permit_names = list(set(permit_names))
        permits_to_add = []
        for n in permit_names:
            if not PermitFactory.has_permit(instance, n):
                permits_to_add.append(n)
        permits = [PermitFactory.new(n) for n in permits_to_add]
        return PermitFactory.add_base_classes(instance, permits)

    @staticmethod
    def add_permit(instance, permit_name):
        return PermitFactory.add_permits(instance, [permit_name])[0]

    @staticmethod
    def has_permit(instance, permit_name):
        try:
            permit = PermitFactory.get(permit_name)
            return PermitFactory.has_base_class(instance, permit)
        except PermitError:
            return False

    @staticmethod
    def remove_permit(instance, permit_name):
        return PermitFactory.remove_base_class(instance, PermitFactory.get(permit_name))

    @staticmethod
    def find_and_remove_permits(instance, permit_names):
        permit_names = list(filter(lambda x: PermitFactory.has_permit(instance, x), permit_names))
        PermitFactory.remove_permits(instance, permit_names)

    @staticmethod
    def remove_permits(instance, permit_names):
        permit_names = list(set(permit_names))
        for p in permit_names:
            PermitFactory.remove_permit(instance, p)

    @staticmethod
    def destroy_all_permits(instance):
        permits = PermitFactory.get_permits(instance)
        for p in permits:
            PermitFactory.remove_base_class(instance, p)

    @staticmethod
    def get_permits(instance):
        return list(filter(lambda x: Permit.is_a_permit(x), instance.__class__.__bases__))

    @staticmethod
    def get_permit_names(instance):
        return [x.name() for x in PermitFactory.get_permits(instance)]