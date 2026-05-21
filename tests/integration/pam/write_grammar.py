from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'OK'",
            "if": [Atom("output_type", "understood")],
        },
        {
            "syn": "s() -> 'Dunno'",
            "if": [Atom("output_type", "explanation")],
        },
    ]
