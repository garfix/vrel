from vrel.core.constants import E1
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'OK'",
            "if": [Atom("last_output", "ok")],
        },
        {
            "syn": "s() -> 'True'",
            "if": [Atom("last_output", "true")],
        },
        {
            "syn": "s() -> 'False'",
            "if": [Atom("last_output", "false")],
        },
        {
            "syn": "s() -> 'Unable to answer'",
            "if": [Atom("last_output", "unknown")],
        },
    ]
