<h1> Kermit </h1>

Kermit is one cool repo. Strict and firm, but easy-going when needed. He doesn't always let you
do what you want, but when he does, you must always ask for a `KermitPermit`. Kermit is a very small package extends class methods to give methods various permissions (inside class, outside class, super class, sub class, etc.)

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
    import kermit

    class FrogStates(object):
        ok_to_jump = 0

        @classmethod
        def jump_permit(cls):
            if FrogStates.ok_to_jump == 0:
                return True
            else:
                return False

    class Frog(object):
        hop_permit = False
        tipsy = False

        def __init__(self, name):
            self.name = name

        @kermit.add(FrogStates.ok_to_jump)
        def jump(self):
            print("Jump!")

        @kermit.add(hop_permit)
        def hop(self):
            print("Hop!")

        @kermit.add(tipsy)
        def secret(self):
            return "I like Ms. Piggy"

        @kermit.permits(tipsy)
        def tell_secret(self):
            print(self.secret())

    # Kermit does not have permission to jump
    f = Frog("Kermit")
    f.jump() # nope
    f.hop() # nope

    # Allow Kermit to jump but not hop
    FrogStates.ok_to_jump = 1
    f.jump() # yup
    f.hop() # nope

    # Allow Kermit to hop
    Frog.hop_permit = True
    f.hop() # yup

    # Allow Kermit to tell secret
    f.secret() # nope
    f.tell_secret() # nope
    f.tipsy = True
    f.secret() # nope
    f.tell_secret() # yup
```
