from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


def create_atom(variable: Variable, predicate: str, args: dict):
    numbered_args = []
    named_args = {}

    for key, value in args.items():
        if key.startswith("ARG"):
            numbered_args.append(value)
        else:
            named_args[key] = value

    return Atom(variable, predicate, *numbered_args, named_args)
