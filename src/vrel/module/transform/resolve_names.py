import copy

from vrel.core.constants import PRED_NAME
from vrel.core.functions.terms import bind_variables
from vrel.entity.Atom import Atom, Modifier
from vrel.entity.Variable import Variable
from vrel.interface.SomeSolver import SomeSolver
from vrel.module.transform.exec_code import exec_code


def resolve_names(atoms: list[Atom], solver: SomeSolver):

    # find all variables associated with names
    named_variables = find_named_variables(atoms)

    # create ids for all variables
    variable_to_id = {variable: resolve_name(name, solver) for variable, name in named_variables.items()}

    # create a new atom with bound named variables
    atoms1 = bind_variables(atoms, variable_to_id)

    exec_code(atoms1, solver)

    # remove the names
    atoms2 = remove_names_from_atoms(atoms1)

    return atoms2


def find_named_variables(term: any) -> dict:
    variables = {}
    if isinstance(term, list):
        for element in term:
            variables |= find_named_variables(element)
    elif isinstance(term, Atom):
        variables |= find_named_variables(term.arguments)
        variables |= find_named_variables(term.get_modifier_atoms())

        if term.predicate == PRED_NAME:
            variable, name = term.arguments
            variables[variable.name] = name

    return variables


def resolve_name(name: str, solver: SomeSolver):
    result = solver.solve([Atom("resolve_name", Variable("Id"), name)])
    if len(result) == 1:
        return result[0]["Id"]
    elif len(result) == 0:
        return None
    else:
        raise Exception(f"More than 1 entity found for name: {name}")


def remove_names_from_atoms(atoms: list[Atom]) -> list[Atom]:
    new_atoms = []
    for atom in atoms:
        if atom.predicate != PRED_NAME:
            new_atoms.append(remove_names_from_atom(atom))

    return new_atoms


def remove_names_from_modifiers(modifiers: list[Modifier]) -> list[Atom]:
    new_modifiers = []
    for mod in modifiers:
        if mod.atom.predicate != PRED_NAME:
            new_modifiers.append(Modifier(atom=remove_names_from_atom(mod.atom), position=mod.position))

    return new_modifiers


def remove_names_from_arguments(args: list[any]) -> list[any]:
    new_atoms = []
    for arg in args:
        if isinstance(arg, list):
            new_atoms.append(remove_names_from_atoms(arg))
        elif isinstance(arg, Atom):
            if arg.predicate == PRED_NAME:
                new_atoms.append(arg.arguments[0])
            else:
                new_atoms.append(remove_names_from_atom(arg))
        else:
            new_atoms.append(arg)

    return new_atoms


def remove_names_from_atom(atom: Atom) -> Atom:
    a = atom.copy()
    a.arguments = remove_names_from_arguments(atom.arguments)
    a.modifiers = remove_names_from_modifiers(atom.modifiers)
    return a
