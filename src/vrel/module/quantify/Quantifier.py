from vrel.core.constants import ARG_DETERMINER
from vrel.core.functions.atoms import create_atom
from vrel.entity.Atom import Atom


def quantify(atom: Atom):

    new_atom: Atom = atom
    extracted_atoms = []

    for arg_name, arg in reversed(atom.arguments.items()):

        if ARG_DETERMINER in arg.named_arguments:
            det = arg.named_arguments[ARG_DETERMINER]
            if not isinstance(det, Atom):
                raise Exception(f"A determiner must be an atom: {det}")

            new_atom = create_quantification(new_atom, arg_name, arg, det)
        else:
            new_atom, extracted_atom = extract_argument(new_atom, arg_name, arg)
            extracted_atoms.append(extracted_atom)

    return extracted_atoms + [new_atom]


def extract_argument(atom: Atom, arg_name: str, arg: Atom):
    new_args = atom.arguments | {arg_name: arg.variable}
    new_atom = create_atom(atom.variable, atom.predicate, new_args)

    extracted_atom = arg
    return new_atom, extracted_atom


def create_quantification(atom: Atom, arg_name: str, arg: Atom, det: Atom):

    if det.predicate == "all":
        q_arg = quantify(arg)
        new_args = atom.arguments | {arg_name: arg.variable}
        q_atom = create_atom(
            "det_all",
            arg.variable,
            q_arg,
            [create_atom(atom.variable, atom.predicate, new_args)],
        )
    elif det.predicate == "equals":
        q_arg = quantify(arg)
        new_args = atom.arguments | {arg_name: arg.variable}
        q_atom = create_atom(
            "det_equals",
            q_arg,
            det["ARG0"],
            [create_atom(atom.variable, atom.predicate, new_args)],
        )

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
