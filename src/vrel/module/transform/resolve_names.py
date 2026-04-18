from vrel.core.constants import ARG_NAME
from vrel.core.functions.terms import bind_variables
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.interface.SomeSolver import SomeSolver


def resolve_names(atom: Atom, solver: SomeSolver):

    # find all variables associated with names
    named_variables = find_named_variables(atom)
    # print(atom)
    # print(named_variables)

    # create ids for all variables
    variable_to_id = {variable: resolve_name(name, solver) for variable, name in named_variables.items()}
    # print(variable_to_id)

    # create a new atom with bound named variables
    new_atom = bind_variables(atom, variable_to_id)
    # print(new_atom)

    # remove the names
    result = remove_names(new_atom)
    # print(result)

    return result


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
    result = solver.solve([Atom("resolve_name", Variable("Id"), name)])
    if len(result) == 1:
        return result[0]["Id"]
    elif len(result) == 0:
        return None
    else:
        raise Exception(f"More than 1 entity found for name: {name}")


def remove_names(term: any) -> any:
    new_term = term
    if isinstance(term, list):
        new_term = [cleared for e in term if (cleared := remove_names(e)) is not None]

    elif isinstance(term, Atom):
        if new_term.predicate == ARG_NAME:
            new_term = None
        else:
            new_term = Atom(term.predicate, *remove_names(term.arguments)).mod(remove_names(term.modifiers))

    return new_term
