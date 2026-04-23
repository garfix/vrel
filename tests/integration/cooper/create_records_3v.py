from vrel.core.functions.terms import bind_variables
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


def create_records_3v(atoms: list[Atom], binding: dict = {}):
    new_atoms = []
    for atom in atoms:
        new_atoms.extend(create_records_atom(atom, binding))
    return new_atoms


def create_records_atom(atom: Atom, binding: dict):
    records = []

    # bind all argument of and_3v to 'true', but don't create a record
    if atom.predicate == "and_3v":
        for arg in atom.arguments:
            if isinstance(arg, Variable):
                binding[arg.name] = "true"
    else:
        # other atoms: create a record, and bind the variables to `true`
        new_atom = bind_variables(atom, binding)
        records.append(new_atom)

    records.extend(create_records_3v(atom.modifiers, binding))

    return records
