from vrel.entity.Atom import Atom
from vrel.entity.Id import Id


def id_unification(term1: any, term2: any, binding: list) -> list[list[Atom, Atom]] | None:
    if binding is None:
        return None

    # list: matches if either all atoms of term1 match with term2, or all atoms of term2 match with term1 (or both)
    if isinstance(term1, list) and isinstance(term2, list):
        binding = unify_id_lists(term1, term2, binding)
    # tuple
    elif isinstance(term1, tuple) and isinstance(term2, tuple):
        binding = unify_id_tuples(term1, term2, binding)
    # atom
    elif isinstance(term1, Atom) and isinstance(term2, Atom):
        binding = unify_id_atoms(term1, term2, binding)
    # ids
    elif isinstance(term1, Id) and isinstance(term2, Id):
        binding = unify_ids(term1, term2, binding)
    # single id
    elif isinstance(term2, Id):
        binding = unify_id_with_nonid(term2, term1, binding)
    elif isinstance(term1, Id):
        binding = unify_id_with_nonid(term1, term2, binding)
    # other
    elif term1 != term2:
        binding = None

    return binding


def unify_id_lists(term1: list, term2: list, binding: list):
    if all(isinstance(x, Atom) for x in term1) and all(isinstance(x, Atom) for x in term2):
        return unify_atom_lists(term1, term2, binding)
    else:
        if len(term1) != len(term2):
            binding = None
        else:
            for arg1, arg2 in zip(term1, term2):
                binding = unify_bindings(binding, id_unification(arg1, arg2, binding))

    return binding


def unify_atom_lists(term1: list, term2: list, binding: list):
    matches1 = {}
    matches2 = {}
    for i2, a2 in enumerate(term2):
        for i1, a1 in enumerate(term1):
            sub = id_unification(a1, a2, binding)
            if sub is not None:
                matches1[i1] = True
                matches2[i2] = True
                binding = unify_bindings(binding, sub)
    if len(matches1) != len(term1) and len(matches2) != len(term2):
        binding = None

    return binding


def unify_id_tuples(term1: tuple, term2: tuple, binding: list):
    if len(term1) != len(term2):
        binding = None
    else:
        for arg1, arg2 in zip(term1, term2):
            binding = unify_bindings(binding, id_unification(arg1, arg2, binding))

    return binding


def unify_id_atoms(term1: Atom, term2: Atom, binding: list):
    if term1.predicate != term2.predicate:
        binding = None
    elif len(term1.arguments) != len(term2.arguments):
        binding = None
    else:
        for arg1, arg2 in zip(term1.arguments, term2.arguments):
            binding = unify_bindings(binding, id_unification(arg1, arg2, binding))

    return binding


def unify_ids(term1: Id, term2: Id, binding: list):
    if term1 == term2:
        return []
    return [[term1, term2]]


def unify_id_with_nonid(term1: Id, term2: any, binding: dict):
    # no new identities
    return []


def unify_bindings(old_binding: list, new_binding: list) -> list | None:
    if old_binding is None:
        return None
    if new_binding is None:
        return None

    return old_binding + new_binding
