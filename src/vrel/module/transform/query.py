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


def create_query(atoms: list[Atom]) -> list[Atom]:
    result = []
    for atom in atoms:
        result.extend(create_atom_query(atom))
    return result


def create_atom_query(atom: Atom) -> list[Atom]:

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
    new_atom.determiner = None

    extracted_atoms = []
    for mod in atom.modifiers:
        if mod.atom.determiner is None:
            extracted_atoms.append(mod.atom)

    for arg in reversed(atom.arguments):
        if isinstance(arg, Variable):
            np_with_determiner = atom.get_determiner_np(arg)
            if np_with_determiner is not None:
                new_atom = create_quantification(new_atom, np_with_determiner)

    return [new_atom] + create_query(extracted_atoms)


def create_quantification(atom: Atom, determiner_with_np: Atom):
    # get the determiner atom from the argument
    det = determiner_with_np.determiner

    # the scoping argument may itself contain scoping, so recurse into it
    range = create_atom_query(determiner_with_np)

    if det.predicate == "all":
        # ('all', E1, [range-atoms], [body-atoms])
        q_atom = Atom(
            "all",
            determiner_with_np.arguments[0],
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
