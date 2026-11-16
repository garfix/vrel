from vrel.entity.Sentinel import Sentinel
from vrel.entity.Atom import Atom, Modifier
from vrel.entity.GrammarRule import GrammarRule
from vrel.entity.Id import Id
from vrel.entity.ParseTreeNode import ParseTreeNode
from vrel.entity.Reference import Reference
from vrel.entity.RuleConstituent import RuleConstituent
from vrel.entity.Variable import Variable

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

BOLD = "\033[1m"

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
        start = "  "
    elif pre == "D":
        color = CYAN
        start = "DT"
    elif pre == "T":
        color = CYAN
        start = "MD"
    elif pre == "MA":
        color = CYAN
        start = ""
    elif pre == "E":
        color = CYAN
        start = "EX"

    prefix = f"{color}{start}{RESET} "

    if isinstance(term, Modifier):
        text = "\n" + space + f"{prefix}{MAGENTA}{term.position}{RESET}"
        text += format_term(term.atom, indent + 1, 0, "MA")
        return text

    if isinstance(term, Atom):
        text = "\n" + space + f"{prefix}({YELLOW}{term.predicate}{RESET}"
        if term.determiner is not None:
            text += format_term(term.determiner, indent + 1, None, "D")

        remaining_modifiers = term.modifiers[:]
        for i, arg in enumerate(term.arguments):
            text += format_term(arg, indent + 1, i + 1, "A")
            for mod in term.get_modifiers_by_term(arg):
                text += format_term(mod, indent + 1, None, "M")
                # a modifier can be attached to multiple arguments (rare)
                if mod in remaining_modifiers:
                    remaining_modifiers.remove(mod)
        if len(remaining_modifiers) > 0:
            text += "\n" + space + "    " + f"{RED}non-bound modifiers{RESET}"
            for mod in remaining_modifiers:
                text += format_term(mod, indent + 1, None, "M")

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


def as_solver_string(term: any):
    if isinstance(term, list):
        return ",".join([as_solver_string(element) for element in term])
    elif isinstance(term, Atom):
        return term.predicate + "/" + as_solver_string(term.arguments)
    else:
        return str(term)


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
        for arg in term.arguments:
            for v in get_variables(arg):
                variables.add(v)

    return list(variables)


def contains(term: any, needle: any) -> bool:
    if isinstance(term, Variable):
        return term == needle
    elif isinstance(term, Id):
        return term == needle
    elif isinstance(term, list):
        for arg in term:
            if contains(arg, needle):
                return True
    elif isinstance(term, tuple):
        for arg in term:
            if contains(arg, needle):
                return True
    elif isinstance(term, Atom):
        return contains(term.arguments, needle)

    return False


def bind_variables(term: any, binding: dict) -> any:
    """
    Binds all variables in term to their binding from bindings
    Note: bindings may in turn contain variables, and these are bound as well
    """
    # list
    if isinstance(term, list):
        return [bind_variables(e, binding) for e in term]
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


def unify_variables(term: any, var_map: dict[str, str]) -> any:
    if term is None:
        return None
    elif isinstance(term, list):
        return [unify_variables(element, var_map) for element in term]
    elif isinstance(term, str) or isinstance(term, int) or isinstance(term, float) or isinstance(term, Sentinel):
        return term
    elif isinstance(term, Atom):
        return term.apply_to_each_atom(lambda arg: unify_variables(arg, var_map))
    elif isinstance(term, Variable):
        if term.name in var_map:
            return Variable(var_map[term.name])
        else:
            return term
    elif isinstance(term, ParseTreeNode):
        # note: children are deliverately left out, so as no to do them twice
        return ParseTreeNode(
            term.category,
            term.children,
            term.form,
            unify_variables(term.rule, var_map),
            term.reg_exp_count,
        )
    elif isinstance(term, Reference):
        return Reference(unify_variables(term.variable, var_map), term.features)
    elif isinstance(term, GrammarRule):
        r = term.copy()
        r.antecedent = unify_variables(r.antecedent, var_map)
        r.consequents = unify_variables(r.consequents, var_map)
        r.ref = unify_variables(r.ref, var_map)
        return r
    elif isinstance(term, RuleConstituent):
        mapped_arguments = [var_map[arg] if arg in var_map else arg for arg in term.arguments]
        return RuleConstituent(
            term.predicate,
            mapped_arguments,
            term.position_type,
            optional=term.optional,
            separator=term.separator,
            function=term.function,
        )
    else:
        raise Exception(f"Unknown type for unification: {type(term)}")


def flatten(term: any):
    if isinstance(term, Atom):
        flattened = term.arguments
        return tuple([*flattened])
    elif isinstance(term, list):
        return [flatten(e) for e in term]
    elif isinstance(term, tuple):
        return tuple([flatten(e) for e in term])
    else:
        return term
