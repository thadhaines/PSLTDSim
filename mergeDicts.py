"""Function to merge a variable number of dictionaries into one. 
Script adds function to builtins
Python 2 Compatible"""
global ver

if ver:
    import builtins
    builtins.ver = ver
else:
    import __builtin__

def mergeDicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


if ver:
    builtins.mergeDicts = mergeDicts
else:
   __builtin__.mergeDicts = mergeDicts