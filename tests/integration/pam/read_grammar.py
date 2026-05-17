from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

C1 = Variable("C1")
C2 = Variable("C2")
C3 = Variable("C3")


def get_read_grammar():
    return [
        # sentence
        {
            "syn": "s() -> question()+'?'",
            "sem": lambda question: None,
        },
        {
            "syn": "s() -> story()",
            "sem": lambda story: None,
        },
        # story of declarative sentences
        {
            "syn": "story() -> decl(C1) story()",
            "sem": lambda decl, story: None,
        },
        {
            "syn": "story() -> decl(C1)",
            "sem": lambda decl: None,
        },
        # question
        {
            "syn": "question() -> clause(C1)+'?'",
            "sem": lambda clause: Atom("intent_question", clause),
        },
        {
            "syn": "question() -> 'why' clause(C1)",
            "sem": lambda clause: Atom("intent_explanation", clause, C1),
        },
        # declarative
        {
            "syn": "decl(C1) -> np(E1) vp(C1, E1)+'.'",
            "sem": lambda np, vp: Atom("intent_understand", vp.mod(np)),
        },
        # verb phrase
        {"syn": "vp(C1, E1) -> copula() adjp(E1)", "sem": lambda copula, adjp: adjp},
        {"syn": "vp(C1, E1) -> vp(C1, E1, E2) np(E2)", "sem": lambda vp, np: vp.mod(np)},
        {"syn": "vp(C1, E1, E2) -> verb(C1, E1, E2)", "sem": lambda verb: verb},
        # verb
        {"syn": "verb(C1, E1, E2) -> 'picked' 'up'", "sem": lambda: Atom("pick_up", C1, E1, E2)},
        {"syn": "verb(C1, E1, E2) -> 'got' 'into'", "sem": lambda: Atom("get_into", C1, E1, E2)},
        # adjective phrase
        {"syn": "adjp(E1) -> adj(E1)", "sem": lambda adj: adj},
        {"syn": "adj(E1) -> 'hungry'", "sem": lambda: Atom("hungry", E1)},
        # copula
        {"syn": "copula() -> 'was'", "sem": lambda: None},
        # noun phrase
        {"syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: nbar},
        {"syn": "np(E1) -> pronoun(E2) nbar(E1)", "sem": lambda pronoun, nbar: nbar.mod(pronoun)},
        {"syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: nbar.with_determiner(det)},
        # nbar
        {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun},
        {"syn": "nbar(E1) -> pronoun(E1)", "sem": lambda pronoun: pronoun},
        # determiner
        {"syn": "det(E1) -> 'the'", "sem": lambda: None},
        # noun
        {"syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun},
        {"syn": "noun(E1) -> 'michelin' 'guide'", "sem": lambda: Atom("michelin_guide", E1)},
        {"syn": "noun(E1) -> 'car'", "sem": lambda: Atom("car", E1)},
        # pronoun
        {"syn": "pronoun(E1) -> 'she'", "sem": lambda: Atom("she", E1)},
        {"syn": "pronoun(E1) -> 'her'", "sem": lambda: Atom("her", E1)},
        # proper noun
        {"syn": "proper_noun(E1) -> /\\w+/", "sem": lambda token: Atom("name", E1, token)},
    ]
