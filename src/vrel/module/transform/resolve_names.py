from vrel.core.constants import ARG_NAME
from vrel.core.functions.terms import bind_variables
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.interface.SomeSolver import SomeSolver


def resolve_names(atoms: list[Atom], solver: SomeSolver):

    # find all variables associated with names
    named_variables = find_named_variables(atoms)
    # print(atom)
    # print(named_variables)

    # create ids for all variables
    variable_to_id = {variable: resolve_name(name, solver) for variable, name in named_variables.items()}
    # print(variable_to_id)

    # remove the names
    removed = remove_names_from_atoms(atoms)
    # print(result)

    # create a new atom with bound named variables
    new_atoms = bind_variables(removed, variable_to_id)
    # print(new_atoms)

    return new_atoms


def find_named_variables(term: any) -> dict:
    variables = {}
    if isinstance(term, list):
        for element in term:
            variables |= find_named_variables(element)
    elif isinstance(term, Atom):
        variables |= find_named_variables(term.arguments)
        variables |= find_named_variables(term.modifiers)

        if term.predicate == ARG_NAME:
            variable, name = term.arguments
            variables[variable.name] = name

    return variables


def resolve_name(name: str, solver: SomeSolver):
    # print("x")
    result = solver.solve([Atom("resolve_name", Variable("Id"), name)])
    # print("x", result)
    if len(result) == 1:
        return result[0]["Id"]
    elif len(result) == 0:
        return None
    else:
        raise Exception(f"More than 1 entity found for name: {name}")


def remove_names_from_atoms(atoms: list[Atom]) -> list[Atom]:
    new_atoms = []
    for atom in atoms:
        if atom.predicate != ARG_NAME:
            new_atoms.append(remove_names_from_atom(atom))

    return new_atoms


def remove_names_from_arguments(args: list[any]) -> list[any]:
    print(args)
    new_atoms = []
    for arg in args:
        if isinstance(arg, list):
            new_atoms.append(remove_names_from_atoms(arg))
        elif isinstance(arg, Atom):
            if arg.predicate == ARG_NAME:
                new_atoms.append(arg.arguments[0])
            else:
                new_atoms.append(remove_names_from_atom(arg))
        else:
            new_atoms.append(arg)

    return new_atoms


def remove_names_from_atom(atom: Atom) -> Atom:
    return Atom(atom.predicate, *remove_names_from_arguments(atom.arguments)).mod(
        remove_names_from_atoms(atom.modifiers)
    )
