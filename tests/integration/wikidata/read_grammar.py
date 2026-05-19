from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom


def get_read_grammar():
    return [
        # sentence
        {
            "syn": "s(E2) -> 'where' 'was' np(E1) 'born'+'?'",
            "sem": lambda np: Atom("intent_report", E2, [Atom("place_of_birth", np, E2)]),
        },
        # np
        {"syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: nbar},
        # nbar
        {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun},
        # noun
        {"syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun},
        # proper noun
        {
            "syn": "proper_noun(E1) -> /\\w+/",
            "sem": lambda token: Atom("name", E1, token),
        },
    ]
