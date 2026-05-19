from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'Hi there!'",
            "if": [Atom("output_type", "hi")],
        },
        {
            "syn": "s() -> format(E1)",
            "if": [Atom("output_type", "list"), Atom("output_list", E1)],
            "format": lambda elements: format_list(elements),
        },
    ]


def format_list(elements):
    elements.sort()
    return ", ".join(elements)
