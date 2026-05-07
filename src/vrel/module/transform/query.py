from vrel.core.constants import ARG_DETERMINER, PRED_AND
from vrel.core.functions.terms import format_term
from vrel.entity.Atom import Atom


def create_query(atoms: list[Atom]) -> list[Atom]:
    result = []
    for atom in atoms:
        result.extend(create_atom_query(atom))
    return result


def create_atom_query(atom: Atom) -> list[Atom]:
    """
    Transforms an atom based on its determiners.
    Each argument holding a determiner modifier is replaced by its entity variable,
    and for each determiner a specific transformation is available that creates a scoped version of the atom.

    input (example):

    (have
        A1. (parent
            A1. $1
            M1. (determiner
                A1. (all)))
            M2. <modifier_clause_p>
        A2. (child
            A1. $2
            M1. (determiner
                A1. (equals
                    A1. 2))))
            M2. <modifier_clause_c>
        M1. <modifier_clause_h>

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

    if atom.predicate == PRED_AND:
        result = []
        for mod in atom.arguments:
            result.extend(create_query(mod))
        return result

    extracted_atoms = []  # create_query(atom.modifiers)

    # - extract scoping arguments (the ones with determiners)
    # - replace scoping arguments with their variables
    determiner_modifiers = []
    determiner_arguments = []
    for i, mod in enumerate(atom.modifiers):
        # if isinstance(mod, Atom):
        det = mod.determiner
        if det is not None:
            determiner_modifiers.append(mod)
        else:
            extracted_atoms.append(mod)

    # new_atom = Atom(atom.predicate, *new_args)
    new_atom = atom.copy()

    # add a scoping layer around the simplified atom for each determiner
    for determiner_modifier in reversed(determiner_modifiers):
        new_atom = create_quantification(new_atom, determiner_modifier)

    return [new_atom] + extracted_atoms


def create_quantification(atom: Atom, scoping_argument: Atom):
    # get the determiner atom from the argument
    det = scoping_argument.determiner

    # the determiner atom should now be removed
    cleared_arg = scoping_argument.with_determiner(None)
    # the scoping argument may itself contain scoping, so recurse into it
    range = create_atom_query(cleared_arg)

    if det.predicate == "all":
        # ('all', E1, [range-atoms], [body-atoms])
        q_atom = Atom(
            "all",
            scoping_argument.arguments[0],
            # Range
            range,
            # Body
            [atom],
        )
    elif det.predicate == "equals":
        # ('det_equals', [body-atoms], Number)
        n = det.arguments[0]
        q_atom = Atom(
            "det_equals",
            # Range + Body
            range + [atom],
            n,
        )
    else:
        raise Exception(f"Unknown determiner: {det.predicate}")

    return q_atom
