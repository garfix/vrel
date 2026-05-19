from vrel.core.constants import E1
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> text(E1)",
            "if": [Atom("output_type", "report"), Atom("output_report", E1)],
        }
    ]
