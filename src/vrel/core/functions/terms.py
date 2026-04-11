from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


def format_term(value: any, indent: str = "\n") -> str:

    from vrel.entity.Atom import Atom

    """
    Formats nested lists, tuples and strings
    """
    if isinstance(value, tuple):
        raise Exception("tuple found")
        text = indent + "("
        sep = ""
        for element in value:
            text += sep + format_term(element, indent + "    ")
            sep = ", "
        text += ")"
    elif isinstance(value, Atom):
        s = ""
        for k, v in value.arguments.items():
            sub = format_term(v, indent + "          ")
            s += "\n" + indent + "    " + f":{k} {sub}"
        text = f"A({value.predicate}{s})"

    elif isinstance(value, list):
        text = indent + "["
        for element in value:
            text += format_term(element, indent + "    ")
        text += indent + "]"
    elif isinstance(value, str):
        text = "'" + value + "'"
    else:
        text = str(value)
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
        return [bind_variables(arg, binding) for arg in term]
    # tuple
    elif isinstance(term, tuple):
        raise Exception("tuple found 2" + str(tuple[0]))
        return tuple([bind_variables(arg, binding) for arg in term])
    elif isinstance(term, Atom):
        return Atom(
            term.predicate,
            {k: bind_variables(v, binding) for k, v in term.arguments.items()},
        )
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
        flattened = [flatten(e) for e in term.numbered_arguments]
        return tuple([*flattened])
    elif isinstance(term, list):
        return [flatten(e) for e in term]
    elif isinstance(term, tuple):
        return tuple([flatten(e) for e in term])
    else:
        return term
