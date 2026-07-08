from vrel.core.constants import E1, NO_SENTENCE, NOT_UNDERSTOOD, UNKNOWN_WORD
from vrel.entity.Atom import Atom


def get_en_us_write_grammar():
    return [
        {"syn": "s() -> 'Sorry, I don\\'t understand'", "if": [Atom("last_output", NOT_UNDERSTOOD)]},
        {"syn": "s() -> 'No sentence given'", "if": [Atom("last_output", NO_SENTENCE)]},
        {
            "syn": "s() -> 'Could not understand:' literal(E1)",
            "if": [Atom("last_output", UNKNOWN_WORD, E1)],
        },
    ]
