<h1> Kermit </h1>

Kermit is a very small package extends class methods to give methods various permissions (inside class, outside class, super class, sub class, etc.)

Kermit is one cool repo. Strict and firm, but easy-going when needed. He doesn't always let you
do what you want, but when he does, you must always ask for **permission**. PyPermissions may not be considered
your *conventional* repo, but its *your* PyPermissions and you love him all the same.

<h3> Why "Kermit"? </h3>
It rhymes with permit. It's fun to call `Kermit.Permit`

<h3> Why Python permissions? </h3>
I know, its not pythonic. It may send shivers down some spins. I was recently working on a project with a few a classes in which I did not want to allow certain methods to be accessible at certain times. Dealing with alot of mixins was getting sloppy. The concept of permissions cleaned up the code.

<h3> Things you can do </h3>
* inherit permissions in a call stack
* set scopes for certain methods
* set different permission states in which sets of methods are accessible/restricted
* fire special methods when a method was called in a particular call stack
* make private class methods (methods that can only be called within the class)

<h3> Status </h3>
I just published it. Its probably not ready yet (2017/09/13).

<h3> Code </h3>
Very minimal. No requirements.

<h3> Example </h3>
```python
    class Foo(object):
        def __init__(self):
            pass

        @add_permits("1")
        def foo1(self):
            self.r1()
            self.foo2()

        @add_permits("2")
        def foo2(self):
            """ Can only be called if its called from foo1 """
            assert self.get_permits() == ["1", "2"]
            self.r1() # ok, if called from foo1
            self.r2() # ok
            foo3()

        @add_permits("3")
        def foo3(self):
            assert self.get_permits() == ["1", "2", "3"]
            try:
                self.r123() # only ok if called from a foo1, foo2 chain
            except PermissionError as e:
                print("r123 must be called from methods with permissions 1, 2 and 3"!)
                raise e

        @require_permits("1")
        def r1(self):
            pass

        @require_permits("2")
        def r2(self):
            pass

        @require_permits("1", "2", "3", method="all", callback=None)
        def r123(self):
            pass
```
