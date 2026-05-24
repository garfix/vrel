from vrel.core.constants import COMBINED, SEPARATE
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

"""
Turns a list of sentence molecules into a queryable list of atoms.
- Determiners are applied and removed from the atom
- Modifiers are added to the list and removed from the atom

    input (example):

    (have
        A1. $1
        A2. $2
        M1. (parent
            A1. $1
            M1. (determiner
                A1. (all)))
            M2. <modifier_clause_p>
        M2. (child
            A1. $2
            M1. (determiner
                A1. (equals
                    A1. 2))))
            M2. <modifier_clause_c>

    output:

    [
        (all
            A1. $1
            A2. [
                (parent
                    A1. $1
                    M2. <modifier_clause_p>))
            ]
            A3. [
                (det_equals
                    A1. [
                        (child
                            A1. $2
                            M2. <modifier_clause_c>)
                        (have
                            A1. $1
                            A2. $2)
                    ]
                    A2. 2)
            ])
        <modifier_clause_h>
    ]
"""


def make_query(term: any) -> list[Atom]:

    if isinstance(term, list):
        result = []
        for element in term:
            result.extend(make_query(element))
        return result

    elif isinstance(term, Atom):

        atom = term

        new_atom = atom.copy()
        new_atom.arguments = [make_query(arg) for arg in atom.arguments]
        new_atom.modifiers = []
        new_atom.determiner = None

        extracted_atoms = []
        for mod in atom.modifiers:
            if mod.atom.determiner is None:
                extracted_atoms.append(mod.atom)

        # quantifier precedence is here based on the reversed order of the arguments
        # this works most of the time, but not always: there are counter examples
        for arg in reversed(atom.arguments):
            if isinstance(arg, Variable):
                np_with_determiner = get_modifier_with_determiner(atom, arg)
                if np_with_determiner is not None:
                    new_atom = create_quantification(new_atom, np_with_determiner)

        return [new_atom] + make_query(extracted_atoms)

    else:
        return term


def get_modifier_with_determiner(atom: Atom, variable: Variable) -> Atom | None:
    """
    Returns the (first) modifier of `atom` that has `variable` as an argument, and that has a determiner
    The goal was to link each modifier to an argument, but it's dreary and error-prone for a developer to do that.
    The insight here is that each modifier can be linked only to a single argument, based on the variable in the modifier.
    """
    for mod in atom.modifiers:
        if mod.atom.determiner is not None:
            for arg in mod.atom.arguments:
                if arg == variable:
                    return mod.atom
    return None


def create_quantification(atom: Atom, np_with_determiner: Atom):
    # get the determiner atom from the argument
    det = np_with_determiner.determiner

    # the scoping argument may itself contain scoping, so recurse into it
    range = make_query(np_with_determiner)
    body = [atom]

    # bind the range and body
    q_atom = det.copy()

    if det.arguments[1] == COMBINED:
        q_atom.arguments = [det.arguments[0], range + body, *det.arguments[2:]]
    elif det.arguments[1] == SEPARATE:
        q_atom.arguments = [det.arguments[0], range, body, *det.arguments[2:]]
    else:
        raise Exception(f"Unknown sentinel: {det.arguments[1]}")

    return q_atom
