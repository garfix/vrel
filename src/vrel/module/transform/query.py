from vrel.core.constants import ARG_DETERMINER
from vrel.core.functions.terms import format_term
from vrel.entity.Atom import Atom


def create_query(atom: Atom) -> list[Atom]:
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

    extracted_atoms = atom.modifiers

    # - extract scoping arguments (the ones with determiners)
    # - replace scoping arguments with their variables
    new_args = []
    scoping_arguments = []
    for arg in atom.arguments:
        if isinstance(arg, Atom):
            det = arg.determiner
            if det is not None:
                scoping_arguments.append(arg)
                # replace the scoping argument with its entity variable
                new_args.append(arg.arguments[0])
            else:
                new_args.append(arg)
        else:
            new_args.append(arg)

    new_atom = Atom(atom.predicate, *new_args)

    # add a scoping layer around the simplified atom for each determiner
    for scoping_argument in reversed(scoping_arguments):
        new_atom = create_quantification(new_atom, scoping_argument)

    return [new_atom] + extracted_atoms


def create_quantification(atom: Atom, scoping_argument: Atom):
    # get the determiner atom from the argument
    det = scoping_argument.determiner

    # the determiner atom should now be removed
    cleared_arg = scoping_argument.with_determiner(None)
    # the scoping argument may itself contain scoping, so recurse into it
    range = create_query(cleared_arg)

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
