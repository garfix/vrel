from vrel.entity.Atom import Atom
from vrel.interface.SomeSolver import SomeSolver


def exec_code(atoms: list[Atom], solver: SomeSolver):
    for atom in atoms:
        exec_atom(atom, solver)


def exec_atom(atom: Atom, solver: SomeSolver):
    if len(atom.exec) > 0:
        solver.solve(atom.exec)

    for arg in atom.arguments:
        if isinstance(arg, Atom):
            exec_atom(arg, solver)

    for mod in atom.modifiers:
        exec_atom(mod, solver)
