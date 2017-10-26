<h1> Status: Dead  </h1>

It was a programming experiment. Modules ended up not being usefull.

<h1> Kermit </h1>

Kermit is one cool repo. Strict and firm, but flexible when needed. He doesn't always let you
do what you want, but when he does, you must always ask for a `KermitPermit`. Kermit is a very small package extends class methods to give methods various permissions (inside class, outside class, super class, sub class, etc.)

<h3> Why "Kermit"? </h3>
It rhymes with permit. It's fun to call `Kermit.Permit`

<h3> Why Python permissions? </h3>
I know, its not pythonic. It may send shivers down some spines. I was recently working on a project with a few a classes in which I did not want to allow certain methods to be accessible at certain times. Dealing with alot of mixins was getting sloppy. The concept of permissions cleaned up the code.

<h3> Features </h3>

 * multiple permits
 * AND logic permits
 * OR logic permits
 * permit inheritance
 * different scopes
 * string permits
 * class accessor permits
 * method permits

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

        @kermit.req(FrogStates.ok_to_jump)
        def jump(self):
            print("Jump!")

        @kermit.req(hop_permit)
        def hop(self):
            print("Hop!")

        @kermit.req(tipsy)
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

kermit.permits.add(permit1, permit2, ...) # add permits for this call stack. Removes added permits after call stack completes.
kermit.permits.set(permit1, permit2, ...) # set permits for this call stack. Returns to original permits after call stack completes.
kermit.req.all(permit1, permit2, ...) # requires prescences of all permits
kermit.req.any(permit1, permit2, ...) # requires prescences of any permits

Require all permits
```python
# require permits x and y
@kermit.req.all("x", "y")
def foo():
    pass
```
    
Require any permit
```python
# require permits x or y
@kermit.req.any("x", "y")
def foo():
    pass
```

More complex logic if you need it. Multiple decorators can be chained with implicit AND logic
```python
# (x | y) & (z & w)
@kermit.req.any("x", "y")
@kermit.req.all("z", "w")
def foo():
    pass
```

Kermit.OR decorator can be used to chain with OR logic
```python
# (x & y) | (z & w)
@kermit.req.all("x", "y").or  # adds OR logic
@kermit.req.all("z", "w")
def foo():
    pass
```

Inherit permits
```python
@kermit.permit.add("x")
def foo():
    # has permits "y" and "x" if called from bar()
    # else has just permit "x" if called from elsewhere
    
@kermit.permit.add("y")
def bar():
    foo() # gets called with "x" and "y" permit
    ```

**Feature Requests?**
