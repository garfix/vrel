from vrel.core.constants import E1, NO_SENTENCE, NOT_UNDERSTOOD, UNKNOWN_WORD
from vrel.entity.Atom import Atom


def get_en_us_write_grammar():
    return [
        {"syn": "s() -> 'Sorry, I don\\'t understand'", "if": [Atom("output_type", NOT_UNDERSTOOD)]},
        {"syn": "s() -> 'No sentence given'", "if": [Atom("output_type", NO_SENTENCE)]},
        {
            "syn": "s() -> 'Could not understand:' text(E1)",
            "if": [Atom("output_type", UNKNOWN_WORD), Atom("output_unknown_word", E1)],
        },
    ]
