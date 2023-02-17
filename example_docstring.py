"""
a dog that will bark.
"""
from typing import List


global_var = None
"""
some global variable
"""

def some_random_method(param_1,param_2, kw_param_1=None) -> None:
    """_just a random method_

    Args:
        param_1 (_str_): _parameter at position 1_
        param_2 (_str_): _parameter at position 2_
        kw_param_1 (_Any_, optional): _keyword parameter 1_. Defaults to None.
    
    Return:
        Nothing returned.
    """

class Dog:
    """🐕"""
    name: str
    """The name of our dog."""
    friends: List["Dog"]
    """The friends of our dog."""

    def __init__(self, name: str):
        """Make a Dog without any friends (yet)."""
        self.name = name
        self.friends = []

    def bark(self, loud: bool = True):
        """*woof*"""

if __name__ == "__main__":
    """main job goes here"""
    var_1 = None
    """variable 1 set to None"""
    var_2 = 1
    """var 2 set to 1"""
    print("finished")
    """denote we are finished"""