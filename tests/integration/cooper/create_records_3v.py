from vrel.core.functions.terms import bind_variables
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


def create_records_3v(input: list[Atom], binding: dict = {}):
    if isinstance(input, list):
        return create_records_list(input, binding)
    else:
        result = create_records_atom(input, binding)
        if len(result) == 1:
            return result[0]
        else:
            raise Exception("Create records results in a list for an atom")


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
    elif atom.predicate == "not_3v":
        arg_in, arg_out = atom.arguments
        if isinstance(arg_out, Variable) and arg_out.name in binding:
            value_in = binding[arg_out.name]
        else:
            value_in = "true"
        value_out = "false" if value_in == "true" else "true"
        binding[arg_in.name] = value_out
    else:
        # other atoms: create a record, and bind the variables to `true`
        new_atom = bind_variables(atom, binding)
        records.append(new_atom)

    records.extend(create_records_3v(atom.modifiers, binding))

    return records
