from permissions.permits import *

class PermissionError(Exception):
    def __init__(self, msg):
        self.msg = msg

class add_permits(object):
    def __init__(self, *permit_list):
        self.permit_list = permit_list

    def __call__(self, fxn):
        def wrappee(*args, **kwargs):
            PermitFactory.add_permits(args[0], self.permit_list)
            try:
                r = fxn(*args, **kwargs)
                PermitFactory.find_and_remove_permits(args[0], self.permit_list)
                return r
            except Exception as e:  # always remove permits even if exception is raise
                PermitFactory.find_and_remove_permits(args[0], self.permit_list)
                raise e
            return r
        return wrappee

# def add_permits(*permit_list):
#     def permit_wrapper(fxn):
#         def wrapper(*args, **kwargs):
#             PermitFactory.add_permits(args[0], permit_list)
#             try:
#                 r = fxn(*args, **kwargs)
#                 PermitFactory.find_and_remove_permits(args[0], permit_list)
#                 return r
#             except Exception as e:  # always remove permits even if exception is raise
#                 PermitFactory.find_and_remove_permits(args[0], permit_list)
#                 raise e
#             return r
#
#         return wrapper
#
#     return permit_wrapper


def assign_permits(*permit_list):
    """ Wrapper that destroys and reassigns permits. Remembers old permit list and re-assigns after method call"""

    def permit_wrapper(fxn):
        def wrapper(*args, **kwargs):
            old_permits = PermitFactory.get_permit_names(args[0])

            def restore_old_permits():
                PermitFactory.destroy_all_permits(args[0])
                PermitFactory.add_permits(args[0], old_permits)

            PermitFactory.destroy_all_permits(args[0])
            PermitFactory.add_permits(args[0], permit_list)
            try:
                r = fxn(*args, **kwargs)
                restore_old_permits()
                return r
            except Exception as e:  # always remove permits even if exception is raise
                restore_old_permits()
                raise e

        return wrapper

    return permit_wrapper


def require_permits(*permit_list, method="all"):
    def permit_wrapper(fxn):
        def wrapper(*args, **kwargs):
            x = [PermitFactory.has_permit(args[0], permit) for permit in permit_list]
            p = False
            if method == "all":
                p = all(x)
            elif method == "any":
                p = any(x)
            if p:
                r = fxn(*args, **kwargs)
                return r
            else:
                raise PermissionError("Fxn {0} does not have the permits required to call. Requires {2} but has {1}."
                                      .format(fxn, PermitFactory.get_permit_names(args[0]), permit_list))

        return wrapper

    return permit_wrapper
