from permissions import *

class Person(object):

    def __init__(self):
        self.has_head = True
        self.sick = False
        self.__knighthood = False

    @property
    def knighthood(self):
        return self.__knighthood

    @require_permits("Royalty")
    def knight(self):
        self.__knighthood = True

    @require_permits("King", "Executioner", method="all")
    def remove_head(self):
        self.has_head = False

    @require_permits("Royalty", "Executioner", method="any")
    def remove_head(self):
        self.has_head = False

class RoyalPerson(Person):

    def __init__(self):
        pass

    @add_permits("Royalty")
    def knight_peasant(self, p):
        x = PermitFactory.get_permit_names(self)
        y = 5
        p.knight()

    @add_permits("Executioner")
    def send_executioner(self, p):
        p.remove_head()

class King(RoyalPerson):

    def __init__(self):
        pass

    @assign_permits("King")
    def off_with_his_head(self, p):
        self.send_executioner(p)

    @add_permits("King")
    def grant_permission_to_behead(self, queen, p):
        queen.off_with_his_head(p)

class Queen(RoyalPerson):

    def __init__(self):
        pass

    @assign_permits("Queen")
    def off_with_his_head(self, p):
        self.send_executioner(p)

joe = Person() # Just some guy
jane = Person() # Just some gal
kermit = Person() # a friendly frog

king = King() # A Royal Person, with beheading abilities
queen = Queen() # A Royal Person, with behading abilities with permission from king

# Knighthood
king.knight_peasant(joe) # OK
queen.knight_peasant(jane) # OK
# try:
#     joe.knight # raises error, we nor joe can knight joe
# except PermissionError as e:
#     print(e)
# # Execution
# print("Sending Executioner")
# king.send_executioner(joe) # OK
# queen.send_executioner(jane) # not allowed
# king.grant_permission_to_behead(queen, jane) # is allowed
#
