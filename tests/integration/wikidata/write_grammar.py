from vrel.core.constants import E1
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> literal(E1)",
            "if": [Atom("last_output", "report", E1)],
        }
    ]
