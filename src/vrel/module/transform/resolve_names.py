from vrel.core.constants import ARG_NAME
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.interface.SomeSolver import SomeSolver


def resolve_names(atom: Atom, solver: SomeSolver):
    if ARG_NAME in atom.arguments:
        id = resolve_name(atom.arguments[ARG_NAME], solver)
        if id is not None:
            return id

    new_args = {}
    for key, value in atom.arguments.items():
        if isinstance(value, Atom):
            new_args[key] = resolve_names(value, solver)
        else:
            new_args[key] = value

    return Atom(atom.predicate, new_args)


def resolve_name(name: str, solver: SomeSolver):
    result = solver.solve(Atom("resolve_name", name, Variable("Id")))
    if len(result) == 1:
        return result[0]["Id"]
    elif len(result) == 0:
        return None
    else:
        raise Exception(f"More than 1 entity found for name: {name}")
