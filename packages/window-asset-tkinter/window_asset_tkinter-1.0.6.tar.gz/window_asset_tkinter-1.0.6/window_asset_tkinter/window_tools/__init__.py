"""
File in charge of grouping the elements of the window tools class
"""

from .add import Add
from .get import Get
from .set import Set
from .unsorted import Unsorted


class WindowTools(Add, Get, Set, Unsorted):
    """ The class in charge of grouping the window tools """

    def __init__(self) -> None:
        super(WindowTools, self).__init__()
        self.success = 0
        self.error = 84
        self._add = Add()
        self._get = Get()
        self._set = Set()
        self._unsorted = Unsorted()

    def test_window_tools(self) -> None:
        """ Test the window tools """
        print("Testing window tools")
        print(f"success = {self.success}")
        print(f"error = {self.error}")
        print(f"add = {dir(self.add)}")
        print(f"get = {dir(self.get)}")
        print(f"set = {dir(self.set)}")
        print(f"unsorted = {dir(self.unsorted)}")
