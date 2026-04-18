from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

RED = "\033[31m"
GREEN = "\033[32m"
BOLD = "\033[1m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

RESET = "\033[0m"


def format_term(value: any, indent: int = 0, index=0, pre="") -> str:
    """
    Formats nested lists, tuples and strings
    """
    space = "    " * indent

    color = ""
    if pre == "A":
        color = BLUE
    elif pre == "M":
        color = MAGENTA
    prefix = f"{color}{pre}{index}.{RESET} " if index > 0 else ""

    if isinstance(value, Atom):
        text = "\n" + space + f"{prefix}({YELLOW}{value.predicate}{RESET}"
        for i, arg in enumerate(value.arguments):
            text += format_term(arg, indent + 1, i + 1, "A")
        # if len(value.modifiers) > 0:
        #     text += "\n" + space + "  ---"
        for i, mod in enumerate(value.modifiers):
            text += format_term(mod, indent + 1, i + 1, "M")
        text += ")"

    elif isinstance(value, list):
        text = "\n" + space + f"{prefix}["
        for i, element in enumerate(value):
            text += format_term(element, indent + 1)
        text += "\n" + space + "]"
    elif isinstance(value, str):
        text = "\n" + space + f"{prefix}'{value}'"
    else:
        text = "\n" + space + f"{prefix}{value}"
    return text


def has_variables(term: any) -> bool:
    return len(get_variables(term)) > 0


def get_variables(term: any) -> list[str]:
    variables = set()
    if isinstance(term, Variable):
        variables.add(term.name)
    elif isinstance(term, list):
        for arg in term:
            for v in get_variables(arg):
                variables.add(v)
    elif isinstance(term, tuple):
        for arg in term:
            for v in get_variables(arg):
                variables.add(v)
    elif isinstance(term, Atom):
        for _, value in term.arguments.items():
            for v in get_variables(value):
                variables.add(v)

    return list(variables)


def bind_variables(term: any, binding: dict) -> any:
    """
    Binds all variables in term to their binding from bindings
    Note: bindings may in turn contain variables, and these are bound as well
    """
    # list
    if isinstance(term, list):
        return [bind_variables(e, binding) for e in term]
    # tuple
    elif isinstance(term, tuple):
        raise Exception("tuple found 2" + str(tuple[0]))
        return tuple([bind_variables(arg, binding) for arg in term])
    elif isinstance(term, Atom):
        return Atom(
            term.predicate,
            *[bind_variables(arg, binding) for arg in term.arguments],
        ).mod([bind_variables(mod, binding) for mod in term.modifiers])
    # variable
    elif isinstance(term, Variable):
        # bound?
        if term.name in binding:
            # return the value, and try to bind it even further
            return bind_variables(binding[term.name], binding)
        else:
            # non-bound variable
            return term
    else:
        # just the value
        return term


def reify_variables(term: any) -> any:
    """
    Returns a copy of construct with all variables it contains replaced by their names
    """
    # list
    if isinstance(term, list):
        return [reify_variables(arg) for arg in term]
    # tuple
    elif isinstance(term, tuple):
        raise Exception("tuple found")
        return tuple([reify_variables(arg) for arg in term])
    # atom
    elif isinstance(term, Atom):
        raise Exception("Todo1")
        return Atom(
            term.predicate,
            {k: reify_variables(v) for k, v in term.arguments.items()},
        )
    # variable
    elif isinstance(term, Variable):
        # return the name of the variable as an id
        return term.name
    else:
        # just the value
        return term


def flatten(term: any):
    if isinstance(term, Atom):
        flattened = [flatten(e) for e in term.arguments]
        return tuple([*flattened])
    elif isinstance(term, list):
        return [flatten(e) for e in term]
    elif isinstance(term, tuple):
        return tuple([flatten(e) for e in term])
    else:
        return term
