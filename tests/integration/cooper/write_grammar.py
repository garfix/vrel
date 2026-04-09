from vrel.core.constants import E1
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'OK'",
            "if": [Atom("output_type", "ok")],
        },
        {
            "syn": "s() -> 'True'",
            "if": [Atom("output_type", "true")],
        },
        {
            "syn": "s() -> 'False'",
            "if": [Atom("output_type", "false")],
        },
        {
            "syn": "s() -> 'Unable to answer'",
            "if": [Atom("output_type", "unknown")],
        },
    ]
