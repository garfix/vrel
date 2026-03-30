from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'Name not found:' text(E1)",
            "if": [Atom("output_type", "name_not_found"), Atom("output_name_not_found", E1)],
        }
    ]
