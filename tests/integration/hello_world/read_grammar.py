from vrel.core.constants import E1
from vrel.entity.Atom import Atom


def get_read_grammar():
    return [
        # sentence
        {
            "syn": "s(E1) -> 'hello' 'world'",
            "sem": lambda: Atom(
                "intent_hello",
            ),
        },
        {
            "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' + '?'",
            "sem": lambda nbar: Atom("intent_list", E1, [nbar]),
        },
        # nbar
        {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun},
        # noun
        {"syn": "noun(E1) -> 'river'", "sem": lambda: Atom("river", E1)},
        # plurals
        {"syn": "noun(E1) -> plural_noun(E1)'", "sem": lambda plural_noun: plural_noun},
        {"syn": "plural_noun(E1) -> /\\w+/+'s'", "sem": lambda token: Atom(token, E1)},
    ]
