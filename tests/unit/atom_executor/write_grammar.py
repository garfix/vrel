from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'Name not found:' literal(E1)",
            "if": [Atom("last_output", "name_not_found", E1)],
        }
    ]
