from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

C1 = Variable("C1")
C2 = Variable("C2")
C3 = Variable("C3")
Sub = Variable("Sub")
Obj = Variable("Obj")
Obj2 = Variable("Obj2")
X = Variable("X")


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
            "syn": "decl(E1) -> np(E1) vp(E1)+'.'",
            "sem": lambda np, vp: Atom("intent_understand", vp.mod(np)),
        },
        # verb phrase
        {"syn": "vp(E1) -> copula() adjp(E1)", "sem": lambda copula, adjp: adjp},
        {"syn": "adjp(E1) -> adj(E1)", "sem": lambda adj: adj},
        {"syn": "adj(E1) -> 'hungry'", "sem": lambda: Atom("hungry", E1)},
        {"syn": "copula() -> 'was'", "sem": lambda: None},
        # noun phrase
        {"syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: nbar},
        {
            "syn": "np(E1) -> det(E1) nbar(E1)",
            "sem": lambda det, nbar: nbar.with_determiner(det),
        },
        # nbar
        {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun},
        # noun
        {
            "syn": "noun(E1) -> proper_noun(E1)",
            "sem": lambda proper_noun: proper_noun,
        },
        # proper noun
        {
            "syn": "proper_noun(E1) -> /\\w+/",
            "sem": lambda token: Atom("name", E1, token),
        },
    ]
