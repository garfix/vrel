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


def format_term(term: any, indent: int = 0, index=0, pre="") -> str:
    """
    Formats nested lists, tuples and strings
    """
    space = "    " * indent

    color = ""
    start = ""
    if pre == "A":
        color = BLUE
        start = f"{index}."
    elif pre == "M":
        color = MAGENTA
        start = f"{index}."
    elif pre == "D":
        color = CYAN
        start = "DT"
    elif pre == "T":
        color = CYAN
        start = "MD"
    elif pre == "E":
        color = CYAN
        start = "EX"

    prefix = f"{color}{start}{RESET} "

    if isinstance(term, Atom):
        text = "\n" + space + f"{prefix}({YELLOW}{term.predicate}{RESET}"
        if term.determiner is not None:
            text += format_term(term.determiner, indent + 1, None, "D")
        for i, arg in enumerate(term.arguments):
            text += format_term(arg, indent + 1, i + 1, "A")
        if len(term.modifiers) > 0:
            text += format_term(term.type, indent + 1, None, "T")
        for i, mod in enumerate(term.modifiers):
            text += format_term(mod, indent + 1, i + 1, "M")
        if len(term.exec) > 0:
            text += format_term(term.exec, indent + 1, None, "E")
        text += ")"

    elif isinstance(term, list):
        text = "\n" + space + f"{prefix}["
        for i, element in enumerate(term):
            text += format_term(element, indent + 1)
        text += "\n" + space + "]"
    elif isinstance(term, str):
        text = "\n" + space + f"{prefix}'{term}'"
    else:
        text = "\n" + space + f"{prefix}{term}"
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
        return term.apply_to_each_atom(lambda arg: bind_variables(arg, binding))
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
