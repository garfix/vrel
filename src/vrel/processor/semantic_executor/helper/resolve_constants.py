from vrel.core.constants import CONSTANT
from vrel.core.functions.terms import bind_variables
from vrel.entity.Atom import Atom, Modifier


def resolve_constants(atoms: list[Atom]):

    # find all variables associated with constants
    variable_to_id = find_constants(atoms)

    # create a new atom with bound named variables
    atoms1 = bind_variables(atoms, variable_to_id)

    # remove the constants
    atoms2 = remove_constants_from_list(atoms1)

    return atoms2


def find_constants(term: any) -> dict:
    variables = {}
    if isinstance(term, list):
        for element in term:
            variables |= find_constants(element)
    elif isinstance(term, Atom):
        variables |= find_constants(term.arguments)
        variables |= find_constants(term.get_modifier_atoms())

        if term.predicate == CONSTANT:
            variable, value = term.arguments
            variables[variable.name] = value

    return variables


def remove_constants_from_list(terms: list) -> list[Atom]:
    new_terms = []
    for term in terms:
        if isinstance(term, Atom):
            if term.predicate != CONSTANT:
                new_terms.append(remove_constants_from_atom(term))
        else:
            new_terms.append(term)

    return new_terms


def remove_constants_from_modifiers(modifiers: list[Modifier]) -> list[Atom]:
    new_modifiers = []
    for mod in modifiers:
        if mod.atom.predicate != CONSTANT:
            new_modifiers.append(Modifier(atom=remove_constants_from_atom(mod.atom), position=mod.position))

    return new_modifiers


def remove_constants_from_arguments(args: list[any]) -> list[any]:
    new_atoms = []
    for arg in args:
        if isinstance(arg, list):
            new_atoms.append(remove_constants_from_list(arg))
        elif isinstance(arg, Atom):
            if arg.predicate == CONSTANT:
                new_atoms.append(arg.arguments[0])
            else:
                new_atoms.append(remove_constants_from_atom(arg))
        else:
            new_atoms.append(arg)

    return new_atoms


def remove_constants_from_atom(atom: Atom) -> Atom:
    a = atom.copy()
    a.arguments = remove_constants_from_arguments(atom.arguments)
    a.modifiers = remove_constants_from_modifiers(atom.modifiers)
    return a
