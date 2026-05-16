from vrel.core.constants import PRED_NAME
from vrel.entity.Atom import Atom
from vrel.interface.SomeSolver import SomeSolver


def exec_code(term: any, solver: SomeSolver):
    if isinstance(term, Atom):
        if len(term.exec) > 0:
            if term.predicate != PRED_NAME:
                raise Exception("Exec atoms should be attacheched to `name` atoms")

            solver.solve(term.exec)

        for arg in term.arguments:
            exec_code(arg, solver)
        for mod in term.modifiers:
            exec_code(mod, solver)

    elif isinstance(term, list):
        for element in term:
            exec_code(element, solver)
