from vrel.core.constants import E1, E2, E3
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
            "syn": "question() -> 'why' 'did' np(E1) vp(C1, E1)",
            "sem": lambda np, vp: Atom("intent_explanation", [vp.mod(np)], C1),
        },
        # declarative
        {
            "syn": "decl(C1) -> np(E1) vp(C1, E1)+'.'",
            "sem": lambda np, vp: Atom("intent_understand", [vp.mod(np)]),
        },
        {
            "syn": "decl_clause(C1) -> nominal(E1) vp(C1, E1)",
            "sem": lambda np, vp: vp.mod(np),
        },
        # verb phrase
        #  modifiers
        {"syn": "vp(C1, E1) -> vp(C1, E1) pp(C1)", "sem": lambda vp, pp: vp.mod(pp)},
        {"syn": "vp(C1, E1) -> copula() adjp(E1)", "sem": lambda copula, adjp: adjp},
        #  variants
        {"syn": "vp(C1, E1) -> vp(C1, E1, E2) nominal(E2)", "sem": lambda vp, np: vp.mod(np)},
        {
            "syn": "vp(C1, E1) -> vp(C1, E1, E2, E3) nominal(E2) nominal(E3)",
            "sem": lambda vp, np1, np2: vp.mod(np1).mod(np2),
        },
        #  implementations
        {"syn": "vp(C1, E1) -> verb(C1, E1)", "sem": lambda verb: verb},
        {"syn": "vp(C1, E1, E2) -> verb(C1, E1, E2)", "sem": lambda verb: verb},
        {"syn": "vp(C1, E1, E2, E3) -> verb(C1, E1, E2, E3)", "sem": lambda verb: verb},
        #  continuous
        {
            "syn": "vp_continuous(C1, E1) -> verb_continuous(C1, E1) pp(C1)",
            "sem": lambda verb_continuous, pp: verb_continuous.mod(pp),
        },
        # verb
        {"syn": "verb(C1, E1) -> 'pulled' 'over'", "sem": lambda: Atom("pull_over", C1, E1)},
        {"syn": "verb(C1, E1) -> 'was'", "sem": lambda: Atom("be", C1, E1)},
        {"syn": "verb(C1, E1, E2) -> 'picked' 'up'", "sem": lambda: Atom("pick_up", C1, E1, E2)},
        {"syn": "verb(C1, E1, E2) -> 'pick' 'up'", "sem": lambda: Atom("pick_up", C1, E1, E2)},
        {"syn": "verb(C1, E1, E2) -> 'got' 'into'", "sem": lambda: Atom("get_into", C1, E1, E2)},
        {"syn": "verb(C1, E1, E2, E3) -> 'asked'", "sem": lambda: Atom("ask", C1, E1, E2, E3)},
        # verb continuous
        {"syn": "verb_continuous(C1, E1) -> 'standing'", "sem": lambda: Atom("stand", C1, E1)},
        # adjective phrase
        {"syn": "adjp(E1) -> adj(E1)", "sem": lambda adj: adj},
        {"syn": "adj(E1) -> 'hungry'", "sem": lambda: Atom("hungry", E1)},
        {"syn": "adj(E1) -> 'lost'", "sem": lambda: Atom("lost", E1)},
        # copula
        {"syn": "copula() -> 'was'", "sem": lambda: None},
        # nominal
        {"syn": "nominal(E1) -> np(E1)", "sem": lambda np: np},
        {"syn": "nominal(E1) -> noun_clause(E1)", "sem": lambda noun_clause: noun_clause},
        # noun phrase
        {"syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: nbar},
        {"syn": "np(E1) -> np(E1) pp(E1)", "sem": lambda np, pp: np.mod(pp)},
        {"syn": "np(E1) -> pronoun(E1)", "sem": lambda pronoun: pronoun},
        {"syn": "np(E1) -> pronoun(E2) nbar(E1)", "sem": lambda pronoun, nbar: nbar.mod(pronoun)},
        {"syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: nbar.with_determiner(det)},
        {
            "syn": "np(E1) -> np(E1) relative_clause(E1)",
            "sem": lambda nbar, relative_clause: nbar.mod(relative_clause),
        },
        # prepositional phase
        {"syn": "pp(E1) -> preposition(E1, E2) np(E2)", "sem": lambda preposition, np: preposition.mod(np)},
        # preposition
        {"syn": "preposition(E1, E2) -> 'to'", "sem": lambda: Atom("to", E1, E2)},
        {"syn": "preposition(E1, E2) -> 'by'", "sem": lambda: Atom("by", E1, E2)},
        {"syn": "preposition(E1, E2) -> 'of'", "sem": lambda: Atom("of", E1, E2)},
        # nbar
        {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun},
        # relative clause
        {"syn": "relative_clause(E1) -> vp_continuous(C1, E1)", "sem": lambda vp_continuous: vp_continuous},
        # noun clause
        {
            "syn": "noun_clause(E1) -> 'where' decl_clause(C1)",
            "sem": lambda decl_clause: Atom("where", E1, C1).mod(decl_clause),
        },
        # determiner
        {"syn": "det(E1) -> 'the'", "sem": lambda: None},
        {"syn": "det(E1) -> 'a'", "sem": lambda: None},
        {"syn": "det(E1) -> 'an'", "sem": lambda: None},
        # noun
        {"syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: proper_noun},
        {"syn": "noun(E1) -> 'michelin' 'guide'", "sem": lambda: Atom("michelin_guide", E1)},
        {"syn": "noun(E1) -> 'car'", "sem": lambda: Atom("car", E1)},
        {"syn": "noun(E1) -> 'farmer'", "sem": lambda: Atom("farmer", E1)},
        {"syn": "noun(E1) -> 'side'", "sem": lambda: Atom("side", E1)},
        {"syn": "noun(E1) -> 'road'", "sem": lambda: Atom("road", E1)},
        # pronoun
        {"syn": "pronoun(E1) -> 'she'", "sem": lambda: Atom("she", E1)},
        {"syn": "pronoun(E1) -> 'he'", "sem": lambda: Atom("he", E1)},
        {"syn": "pronoun(E1) -> 'her'", "sem": lambda: Atom("her", E1)},
        {"syn": "pronoun(E1) -> 'him'", "sem": lambda: Atom("him", E1)},
        # proper noun
        {"syn": "proper_noun(E1) -> /\\w+/", "sem": lambda token: Atom("name", E1, token)},
    ]
