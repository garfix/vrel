from vrel.core.constants import ARG_DETERMINER
from vrel.core.functions.atoms import create_atom
from vrel.entity.Atom import Atom


def quantify(atom: Atom):

    extracted_atoms = []

    new_atom = atom
    for arg_name, arg in atom.arguments.items():
        if isinstance(arg, Atom):
            # arg = (p / parent)
            if not ARG_DETERMINER in arg.named_arguments:
                new_atom, extracted_atom = extract_argument(new_atom, arg_name, arg)
                extracted_atoms.append(extracted_atom)

    determiner_arguments, cleared_atom = extract_determiner_arguments(new_atom)

    new_atom = cleared_atom
    for determiner_argument in determiner_arguments:
        new_atom = create_quantification(new_atom, determiner_argument)

    return extracted_atoms + [new_atom]


def extract_determiner_arguments(atom: Atom):

    new_atom = atom
    determiner_arguments = []

    for arg_name, arg in reversed(atom.arguments.items()):
        if isinstance(arg, Atom):
            # arg = (p / parent)
            if ARG_DETERMINER in arg.named_arguments:
                det = arg.named_arguments[ARG_DETERMINER]
                if not isinstance(det, Atom):
                    raise Exception(f"A determiner must be an atom: {det}")

                # arg = (p / parent :determiner (d / all))
                new_atom = new_atom.add_arguments({arg_name: arg.variable})
                determiner_arguments.append(arg)

    return determiner_arguments, new_atom


def extract_argument(atom: Atom, arg_name: str, arg: Atom):
    new_args = atom.arguments | {arg_name: arg.variable}
    new_atom = create_atom(atom.variable, atom.predicate, new_args)

    extracted_atom = arg
    return new_atom, extracted_atom


def create_quantification(atom: Atom, determiner_argument: Atom):

    det = determiner_argument.arguments["determiner"]

    if det.predicate == "all":
        c_arg = determiner_argument.remove_argument("determiner")
        q_arg = quantify(c_arg)

        # ('all', E1, [range-atoms], [body-atoms])
        q_atom = Atom(
            "all",
            determiner_argument.variable,
            # Range
            q_arg,
            # Body
            [atom],
        )
    elif det.predicate == "equals":
        c_arg = determiner_argument.remove_argument("determiner")
        q_arg = quantify(c_arg)

        # ('det_equals', [body-atoms], Number)
        q_atom = Atom(
            "det_equals",
            # Range + Body
            q_arg + [atom],
            det.numbered_arguments[0],
        )
    else:
        raise Exception(f"Unknown determiner: {det.predicate}")

    return q_atom


# All parents with 3 degrees have 2 children

# ('all', E1, [range-atoms], [body-atoms])

# (s / have [A]
#     :ARG0 (p / parent [B]
#            :determiner (d / all)) [C]
#            :ARG1-of (h / have-degree-91 [D]
#                        (f / degree
#                           :determiner: (e / equals
#                                           : ARG0 3
#                                       ))
#                         )
#     :ARG1 (c / child
#            : determiner (d / equals
#                 :ARG0 2
#              ))
#            :modifier (m / mod)
# )

# (all [C], p, parent [B], (
#     number e, degree, 3 {       [D]
#         have_degree(p, e)
#     }
#     number, c, child, 2, {

#         have(p, c) [A]
#     }
# ))
