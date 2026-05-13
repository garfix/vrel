from vrel.core.constants import CONSTANT, E1, E2, E3, E4, COMBINED, SEPARATE
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

Body = Variable("Body")
Range = Variable("Range")
Size = Variable("Size")


def get_read_grammar():
    return [
        # sentence
        {
            # Does Afghanistan border China?
            "syn": "s(E1) -> 'does' np(E1) vp(E1) + '?'",
            "sem": lambda np, vp: Atom("intent_yn", [vp.mod(np)]),
        },
        {
            # Is there some ocean that does not border any country?
            "syn": "s(E1) -> 'is' 'there' np(E1) + '?'",
            "sem": lambda np: Atom("intent_yn", [np]),
        },
        {
            # Is there more than one country in each continent?
            "syn": "s(E2) -> 'is' 'there' np(E1) preposition(E1, E2) 'each' nbar(E2) + '?'",
            "sem": lambda np, preposition, nbar: Atom("intent_yn", [Atom("det_all", E2, nbar, [np, preposition])]),
        },
        {
            # What rivers are there?
            "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' + '?'",
            "sem": lambda nbar: Atom("intent_list", E1, [nbar]),
        },
        {
            # What countries are there in Europe?
            "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' pp(E1) + '?'",
            "sem": lambda nbar, pp: Atom("intent_list", E1, [nbar.mod(pp)]),
        },
        {
            # What is the capital of Upper_Volta?
            # What is the ocean that borders African countries?
            "syn": "s(E1) -> 'what' 'is' np(E1) + '?'",
            "sem": lambda np: Atom("intent_list", E1, [np]),
        },
        {
            # What are the countries south of the Equator and not in Australasia?
            # What are the continents no country in which contains more than two cities whose population exceeds 1 million?
            "syn": "s(E1) -> 'what' 'are' np(E1) + '?'",
            "sem": lambda np: Atom("intent_list", E1, [np]),
        },
        {
            # What are the countries from which a river flows into the Black_Sea?
            "syn": "s(E1) -> 'what' 'are' np(E1) vp(E1) + '?'",
            "sem": lambda np, vp: Atom("intent_list", E1, [np, vp]),
        },
        {
            # What are the capitals of the countries bordering the Baltic?
            "syn": "s(E1, E2) -> 'what' 'are' 'the' noun(E1) 'of' np(E2) + '?'",
            "sem": lambda noun, np: Atom("intent_table", [E2, E1], ["", ""], [noun, Atom("of", E1, E2), np]),
            "boost": 1,
        },
        {
            # What is the total area of countries south of the Equator and not in Australasia?
            "syn": "s(E1) -> 'what' 'is' aggregate(E1) + '?'",
            "sem": lambda aggregate: Atom("intent_value_with_unit", E1, "ksqmiles", [aggregate]),
        },
        {
            # What is the average area of the countries in each continent?
            "syn": "s(E1, E3) -> 'what' 'is' group_by(E1, E3) 'each' nbar(E3) + '?'",
            "sem": lambda group_by, nbar: Atom(
                "intent_table",
                [E3, E1],
                ["", "ksqmiles"],
                [nbar, group_by],
            ),
        },
        {
            # What percentage of countries border each ocean?
            "syn": "s(E2, E1) -> 'what' group_by(E1, E2) 'each' nbar(E2) + '?'",
            "sem": lambda group_by, nbar: Atom("intent_table", [E2, E1], ["", ""], [nbar, group_by]),
        },
        {
            # Where is the largest country?
            "syn": "s(E2) -> 'where' 'is' np(E1) + '?'",
            "sem": lambda np: Atom("intent_list", E2, [np, Atom("where", E1, E2)]),
        },
        {
            # How large is the smallest american country?
            "syn": "s(E2) -> 'how' 'large' 'is' np(E1) + '?'",
            "sem": lambda np: Atom("intent_value_with_unit", E2, "ksqmiles", [np, Atom("size_of", E1, E2)]),
        },
        {
            # Which countries are bordered by two seas?
            "syn": "s(E1) -> 'which' nbar(E1) 'are' adjp(E1) + '?'",
            "sem": lambda nbar, adjp: Atom("intent_list", E1, [nbar, adjp]),
        },
        {
            # Which countries are bordered by two seas?
            "syn": "s(E1) -> 'which' nbar(E1) 'are' vp(E1) + '?'",
            "sem": lambda nbar, vp: Atom("intent_list", E1, [nbar, vp]),
        },
        {
            # Which is the largest african country?
            "syn": "s(E1) -> 'which' 'is' np(E1) + '?'",
            "sem": lambda np: Atom("intent_list", E1, [np]),
        },
        {
            # Which country's capital is London?
            "syn": "s(E1) -> 'which' nbar(E1, E2) 'is' np(E2) + '?'",
            "sem": lambda nbar, np: Atom("intent_list", E1, [nbar, np]),  # , Atom("equals", E2, E3)
        },
        {
            # Which country bordering the Mediterranean borders a country that is bordered by a country whose population exceeds the population of India?
            # Which countries have a population exceeding 10 million?
            # Which countries with a population exceeding 10 million border the Atlantic?
            "syn": "s(E1) -> 'which' np(E1) vp(E1) + '?'",
            "sem": lambda np, vp: Atom("intent_list", E1, [np, vp]),
        },
        {
            # How many countries does the Danube flow through?
            "syn": "s(E1) -> 'how' 'many' nbar(E1) vp(E1) + '?'",
            "sem": lambda nbar, vp: Atom("intent_value", E1, [Atom("count", E1, [nbar, vp])]),
        },
        {
            # Bye.
            "syn": "s(E1) -> 'bye' + '.'?",
            "sem": lambda: Atom(
                "intent_close_conversation",
            ),
        },
        # verb phrase
        {"syn": "vp(E1) -> verb(E1, E2) np(E2)", "sem": lambda verb, np: verb.mod(np)},
        {"syn": "vp(E1) -> verb(E2, E1) 'by' np(E2)", "sem": lambda verb, np: verb.mod(np)},
        {"syn": "vp(E1) -> 'is' verb(E2, E1) 'by' np(E2)", "sem": lambda verb, np: verb.mod(np)},
        {"syn": "vp(E1) -> 'does' np(E2) verb(E2, E1)", "sem": lambda np, verb: verb.mod(np)},
        {"syn": "vp(E1) -> 'does' 'not' vp(E1)", "sem": lambda vp: Atom("not", vp)},
        {"syn": "vp(E1) -> 'have' 'a' attr(E1, E2)", "sem": lambda attr: attr},
        {"syn": "vp(E1) -> 'from' 'which' np(E2) vp(E1, E2)", "sem": lambda np, vp: vp.mod(np)},
        {
            "syn": "vp_continuous(E1) -> verb_continuous(E1, E2) np(E2)",
            "sem": lambda verb_continuous, np: verb_continuous.mod(np),
        },
        {"syn": "vp(E1, E2) -> verb(E2, E1, E3) np(E3)", "sem": lambda verb, np: verb.mod(np)},
        # verb
        {"syn": "verb(E1, E2) -> 'border'", "sem": lambda: Atom("borders", E1, E2)},
        {"syn": "verb(E1, E2) -> 'borders'", "sem": lambda: Atom("borders", E1, E2)},
        {"syn": "verb(E1, E2) -> 'bordered'", "sem": lambda: Atom("borders", E1, E2)},
        {"syn": "verb(E1, E2) -> 'contains'", "sem": lambda: Atom("contains", E1, E2)},
        {"syn": "verb(E1, E2) -> 'flow' 'through'", "sem": lambda: Atom("flows_through", E1, E2)},
        {"syn": "verb(E1, E2) -> 'exceeds'", "sem": lambda: Atom("exceeds", E1, E2)},
        # continuous verb
        {"syn": "verb_continuous(E1, E2) -> 'bordering'", "sem": lambda: Atom("borders", E1, E2)},
        {"syn": "verb_continuous(E1, E2) -> 'exceeding'", "sem": lambda: Atom("exceeds", E1, E2)},
        # ditransitive verb
        {"syn": "verb(E1, E2, E3) -> 'flows' 'into'", "sem": lambda: Atom("flows_from_to", E1, E2, E3)},
        # np
        {"syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: nbar},
        {
            "syn": "np(E1) -> det(E1) nbar(E1)",
            "sem": lambda det, nbar: nbar.with_determiner(det),
        },
        {
            "syn": "np(E1) -> 'the' 'largest' nbar(E1)",
            "sem": lambda nbar: Atom("arg_max", E1, Size, [nbar], [Atom("size_of", E1, Size)]),
        },
        {
            "syn": "np(E1) -> 'the' 'smallest' nbar(E1)",
            "sem": lambda nbar: Atom("arg_min", E1, Size, [nbar], [Atom("size_of", E1, Size)]),
        },
        {
            "syn": "np(E1) -> np(E1) relative_clause(E1)",
            "sem": lambda nbar, relative_clause: nbar.mod(relative_clause),
        },
        # nbar
        {"syn": "nbar(E1) -> adjp(E1) nbar(E1)", "sem": lambda adjp, nbar: nbar.mod(adjp)},
        {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun},
        {
            "syn": "nbar(E1, E2) -> nbar(E1)+'\\''+'s' np(E2)",
            "sem": lambda nbar, np: nbar.mod(Atom("of", E2, E1).mod(np)),
        },
        {"syn": "nbar(E1) -> nbar(E1) pp(E1)", "sem": lambda nbar, pp: nbar.mod(pp)},
        # relative clauses
        {"syn": "relative_clause(E1) -> 'that' vp(E1)", "sem": lambda vp: vp},
        {
            "syn": "relative_clause(E1) -> relative_clause(E1) 'and' relative_clause(E1)",
            "sem": lambda rel1, rel2: rel1.mod(rel2),
        },
        {"syn": "relative_clause(E1) -> vp_continuous(E1)", "sem": lambda vp_continuous: vp_continuous},
        {"syn": "relative_clause(E1) -> vp(E1)", "sem": lambda vp: vp},
        {
            "syn": "relative_clause(E1) -> np(E2) preposition(E2, E1) 'which' vp(E2)",
            "sem": lambda np, preposition, vp: vp.mod(np.mod(preposition)),
        },
        {"syn": "relative_clause(E1) -> 'whose' attr(E1, E2) vp(E2)", "sem": lambda attr, vp: attr.mod(vp)},
        {
            "syn": "relative_clause(E1) -> 'with' 'a' attr(E1, E2) vp_continuous(E2)",
            "sem": lambda attr, vp_continuous: attr.mod(vp_continuous),
        },
        {"syn": "np(E1) -> 'the' attr(E2, E1) 'of' nbar(E2)", "sem": lambda attr, nbar: attr.mod(nbar)},
        {"syn": "np(E1) -> number(E1)", "sem": lambda number: Atom(CONSTANT, E1, number)},
        # determiner
        {"syn": "det(E1) -> 'a'", "sem": lambda: None},
        {"syn": "det(E1) -> 'the'", "sem": lambda: None},
        {"syn": "det(E1) -> 'some'", "sem": lambda: None},
        {"syn": "det(E1) -> 'any'", "sem": lambda: None},
        {"syn": "det(E1) -> 'no'", "sem": lambda: Atom("det_none", E1, COMBINED)},
        {
            "syn": "det(E1) -> number(E1)",
            "sem": lambda number: Atom("det_equals", E1, COMBINED, number),
        },
        {
            "syn": "det(E1) -> 'more' 'than' number(E1)",
            "sem": lambda number: Atom("det_greater_than", E1, COMBINED, number),
        },
        # attribute
        {"syn": "attr(E1, E2) -> 'population'", "sem": lambda: Atom("has_population", E1, E2)},
        {
            "syn": "attr(E1, E2) -> attr(E1, E2) relative_clause(E2)",
            "sem": lambda attr, relative_clause: attr.mod(relative_clause),
        },
        # number
        {"syn": "number(E1) -> 'one'", "sem": lambda: 1},
        {"syn": "number(E1) -> 'two'", "sem": lambda: 2},
        {"syn": "number(E1) -> 'three'", "sem": lambda: 3},
        {"syn": "number(E1) -> 'four'", "sem": lambda: 4},
        {"syn": "number(E1) -> 'five'", "sem": lambda: 5},
        {"syn": "number(E1) -> 'six'", "sem": lambda: 6},
        {"syn": "number(E1) -> 'seven'", "sem": lambda: 7},
        {"syn": "number(E1) -> 'eight'", "sem": lambda: 8},
        {"syn": "number(E1) -> 'nine'", "sem": lambda: 9},
        {"syn": "number(E1) -> 'ten'", "sem": lambda: 10},
        {"syn": "number(E1) -> /\\d+/", "sem": lambda token: int(token)},
        {"syn": "number(E1) -> number(E1) 'million'", "sem": lambda number: number * 1000000},
        # prepositional phrases
        {"syn": "pp(E1) -> 'not' pp(E1)", "sem": lambda pp: Atom("not", [pp])},
        {"syn": "pp(E1) -> preposition(E1, E2) np(E2)", "sem": lambda preposition, np: preposition.mod(np)},
        {"syn": "pp(E1) -> 'south' 'of' np(E2)", "sem": lambda np: Atom("south_of", E1, E2).mod(np)},
        {"syn": "pp(E1) -> pp(E1) 'and' pp(E1)", "sem": lambda pp1, pp2: pp1.mod(pp2)},
        {"syn": "preposition(E1, E2) -> 'in'", "sem": lambda: Atom("in", E1, E2)},
        {"syn": "preposition(E1, E2) -> 'of'", "sem": lambda: Atom("of", E1, E2)},
        # adjective phrases
        {"syn": "adjp(E1) -> adj(E1)", "sem": lambda adj: adj},
        {"syn": "adj(E1) -> 'european'", "sem": lambda: Atom("european", E1)},
        {"syn": "adj(E1) -> 'african'", "sem": lambda: Atom("african", E1)},
        {"syn": "adj(E1) -> 'american'", "sem": lambda: Atom("american", E1)},
        {"syn": "adj(E1) -> 'asian'", "sem": lambda: Atom("asian", E1)},
        # noun
        {"syn": "noun(E1) -> singular_noun(E1)", "sem": lambda singular_noun: singular_noun},
        {
            "syn": "noun(E1) -> singular_noun(E1)+'s'",
            "sem": lambda singular_noun: singular_noun,
            "boost": -1,
        },
        {
            "syn": "noun(E1) -> proper_noun(E1)",
            "sem": lambda proper_noun: proper_noun,
            "boost": -2,
        },
        {"syn": "singular_noun(E1) -> 'river'", "sem": lambda: Atom("river", E1)},
        {"syn": "singular_noun(E1) -> 'capital'", "sem": lambda: Atom("capital", E1)},
        {"syn": "singular_noun(E1) -> 'ocean'", "sem": lambda: Atom("ocean", E1)},
        {"syn": "singular_noun(E1) -> 'country'", "sem": lambda: Atom("country", E1)},
        {"syn": "singular_noun(E1) -> 'sea'", "sem": lambda: Atom("sea", E1)},
        {"syn": "singular_noun(E1) -> 'city'", "sem": lambda: Atom("city", E1)},
        {"syn": "singular_noun(E1) -> 'continent'", "sem": lambda: Atom("continent", E1)},
        {"syn": "noun(E1) -> 'continents'", "sem": lambda: Atom("continent", E1)},
        {"syn": "noun(E1) -> 'countries'", "sem": lambda: Atom("country", E1)},
        {"syn": "noun(E1) -> 'cities'", "sem": lambda: Atom("city", E1)},
        {"syn": "noun(E1) -> 'seas'", "sem": lambda: Atom("sea", E1)},
        # proper noun
        {
            "syn": "proper_noun(E1) -> /\\w+/",
            "sem": lambda token: Atom("name", E1, token),
        },
        # aggregates
        {
            "syn": "aggregate(E1) -> 'the' 'total' 'area' 'of' np(E2)",
            "sem": lambda np: Atom("sum", E1, E3, [np, Atom("size_of", E2, E3)]),
        },
        {
            "syn": "group_by(E1, E3) -> 'the' 'average' 'area' 'of' np(E2) preposition(E2, E3)",
            "sem": lambda np, preposition: Atom("avg", E1, E4, [np, preposition, Atom("size_of", E2, E4)]),
        },
        {
            "syn": "group_by(E3, E2) -> 'percentage' 'of' np(E1) verb(E1, E2)",
            "sem": lambda np, verb: Atom("percentage", E3, [verb.mod(np)], np),
        },
    ]
