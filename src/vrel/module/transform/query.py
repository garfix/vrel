from vrel.core.constants import ARG_DETERMINER, PRED_AND
from vrel.core.functions.terms import format_term
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


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

    extracted_atoms = []

    new_args = []
    for arg in atom.arguments:
        if isinstance(arg, list):
            new_args.append(create_query(arg))
        elif isinstance(arg, Atom):
            new_args.append(create_atom_query(arg))
        else:
            new_args.append(arg)

    new_atom = atom.copy()
    new_atom.arguments = new_args

    new_atom.modifiers = []
    determiners = {}
    for mod in atom.modifiers:
        if mod.atom.determiner is not None:
            determiners[mod.variable.name] = mod.atom
        else:
            extracted_atoms.append(mod.atom)

    for arg in reversed(atom.arguments):
        if isinstance(arg, Variable) and arg.name in determiners:
            new_atom = create_quantification(new_atom, determiners[arg.name])

    return [new_atom] + create_query(extracted_atoms)


def create_quantification(atom: Atom, determiner_modifier: Atom):
    # get the determiner atom from the argument
    det = determiner_modifier.determiner

    # the determiner atom should now be removed
    cleared_arg = determiner_modifier.with_determiner(None)
    # the scoping argument may itself contain scoping, so recurse into it
    range = create_atom_query(cleared_arg)

    if det.predicate == "all":
        # ('all', E1, [range-atoms], [body-atoms])
        q_atom = Atom(
            "all",
            cleared_arg.arguments[0],
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
