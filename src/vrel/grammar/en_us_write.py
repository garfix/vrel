from vrel.core.constants import E1, NO_SENTENCE, NOT_UNDERSTOOD, UNKNOWN_WORD, DUMMY
from vrel.entity.Atom import Atom


def get_en_us_write_grammar():
    return [
        {"syn": "s() -> 'Sorry, I don\\'t understand'", "if": [Atom(DUMMY, "output_type", NOT_UNDERSTOOD)]},
        {"syn": "s() -> 'No sentence given'", "if": [Atom(DUMMY, "output_type", NO_SENTENCE)]},
        {
            "syn": "s() -> 'Could not understand:' text(E1)",
            "if": [Atom(DUMMY, "output_type", UNKNOWN_WORD), Atom(DUMMY, "output_unknown_word", E1)],
        },
    ]
