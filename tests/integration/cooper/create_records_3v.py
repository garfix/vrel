from vrel.core.functions.terms import bind_variables
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


def create_records_3v(input: list[Atom], binding: dict = {}):
    """
    Remove AND and NOT from the input, and bind all the truth values
    in preparation for storage in the database
    """
    if isinstance(input, list):
        return create_records_list(input, binding)
    elif isinstance(input, Atom):
        result = create_records_atom(input, binding)
        if len(result) == 1:
            return result[0]
        else:
            raise Exception("Create records results in a list for an atom")
    else:
        return []


def create_records_list(atoms: list[Atom], binding: dict = {}):
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
        for arg in atom.arguments:
            if not isinstance(arg, Variable):
                records.extend(create_records_3v(arg, binding))
    elif atom.predicate == "not_3v":
        atoms, arg_in, arg_out = atom.arguments
        if isinstance(arg_out, Variable):
            value_out = "true"
        else:
            value_out = arg_out

        value_in = "false" if value_out == "true" else "true"
        binding[arg_in.name] = value_in
        records.extend(create_records_3v(atoms, binding))

    else:
        new_atom = bind_variables(atom, binding)
        records.append(new_atom)

    return records
