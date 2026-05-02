from vrel.core.functions.terms import as_solver_string
from vrel.entity.Atom import Atom
from vrel.interface.SomeStackOverflowHandler import SomeStackOverflowHandler


class NoStackOverflowHandler(SomeStackOverflowHandler):

    def check_stack(self, atom: Atom) -> bool:
        return False

    def remove(self, atom: Atom):
        pass
