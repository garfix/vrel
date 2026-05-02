from vrel.core.functions.terms import as_solver_string
from vrel.entity.Atom import Atom
from vrel.interface.SomeStackOverflowHandler import SomeStackOverflowHandler


class StackOverflowHandler(SomeStackOverflowHandler):

    calls: dict

    def __init__(self):
        self.calls = {}

    def check_stack(self, atom: Atom) -> bool:
        key = as_solver_string(atom)
        if key in self.calls:
            return True

        self.calls[key] = True
        return False

    def remove(self, atom: Atom):
        key = as_solver_string(atom)
        del self.calls[key]
