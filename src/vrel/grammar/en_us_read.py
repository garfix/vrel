from vrel.core.constants import E1
from vrel.entity.Atom import Atom


def get_en_us_read_grammar():
    return [
        # noun
        {
            "syn": "noun(E1) -> /\\w+/+'s'",
            "sem": lambda token: Atom(token, E1),
            "boost": -1,
        },
        {
            "syn": "noun(E1) -> /\\w+/+'ies'",
            "sem": lambda token: lambda: Atom(
                token + "y",
                E1,
            ),
            "boost": -1,
        },
        {
            "syn": "noun(E1) -> proper_noun(E1)",
            "sem": lambda proper_noun: Atom("name", E1, proper_noun),
            "boost": -2,
        },
        # proper noun
        {
            "syn": "proper_noun(E1) -> /\\w+/",
            "sem": lambda token: token,
        },
    ]
