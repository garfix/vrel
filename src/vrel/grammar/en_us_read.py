from vrel.core.constants import E1
from vrel.entity.Atom import Atom


def get_en_us_read_grammar():
    return [
        # np
        {"syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: nbar},
        # nbar
        {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun},
        {
            "syn": "np(E1) -> det(E1) nbar(E1)",
            "sem": lambda det, nbar: nbar.add_arguments(det),
        },
        # det
        {"syn": "det(E1) -> 'a'", "sem": lambda: {"determiner": "a"}},
        # noun
        {
            "syn": "noun(E1) -> /\\w+/+'s'",
            "sem": lambda token: Atom(E1, token),
            "boost": -1,
        },
        {
            "syn": "noun(E1) -> /\\w+/+'ies'",
            "sem": lambda token: lambda: Atom(E1, token + "y"),
            "boost": -1,
        },
        # proper noun
        {
            "syn": "noun(E1) -> proper_noun(E1)",
            "sem": lambda proper_noun: proper_noun,
            "boost": -2,
        },
        {
            "syn": "proper_noun(E1) -> /\\w+/",
            "sem": lambda token: Atom(E1, "<unknown>", {"name": token}),
        },
    ]
