from permissions import *

class Person(object):

    def __init__(self, name, email):
        self.__name = name
        self.__email = email

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @name.setter
    def name(self):
        return self.__name

    @email.setter
    def email(self):
        return self.__email


class PrivatePerson(Person):

    def __init__(self, *args, **kwargs):
        super(PrivatePerson, self).__init__(*args, **kwargs)

    @property
    @require_permits("friend")
    def name(self):
        return self.__name

    @property
    @require_permits("friend")
    def email(self):
        return self.__email

    @name.setter
    @require_permits("parents")
    def name(self):
        return self.__name

    @email.setter
    @require_permits("friend", "married")
    def email(self):
        return self.__email

    @assign_permits("parents")
    def have_parents_name(self, name):
        self.name = name

piggy = Person("Piggy", "Pig@ILoveTheFrog.org")
kermit = PrivatePerson("Kermit", "Kermit@thefrog.org")

piggy.name
piggy.email

try:
    kermit.name # errors out
except PermissionError as e:
    print(e)

try:
    kermit.name = "Kermit the II"# errors out
except PermissionError as e:
    print(e)

