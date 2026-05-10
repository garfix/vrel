from vrel.core.constants import E1, E2, E3, E4
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

Body = Variable("Body")
Size = Variable("Size")


def get_read_grammar():
    return [
        # sentence
        {
            # Does Afghanistan border China?
            "syn": "s(E1) -> 'does' np(E2) verb(E2, E3) np(E3) + '?'",
            "sem": lambda np1, verb, np2: Atom("intent_yn", [Atom(verb, E2, E3).mod(np1).mod(np2)]),
        },
        # {
        #     "syn": "s(E1) -> 'is' 'there' np(E1) + '?'",
        #     "sem": lambda np: [('intent_yn', apply(np, []))],
        # },
        # {
        #     "syn": "s(E2) -> 'is' 'there' np(E1) preposition(E1, E2) 'each' nbar(E2) + '?'",
        #     "sem": lambda np, preposition, nbar: [('intent_yn', [('all', E2, nbar, apply(np, preposition))])],
        # },
        {
            # What rivers are there?
            "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' + '?'",
            "sem": lambda nbar: Atom("intent_list", E1, [nbar]),
        },
        # {
        #     "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' pp(E1) + '?'",
        #     "sem": lambda nbar, pp: [('intent_list', e1, nbar + pp)],
        # },
        {
            # What is the capital of Upper_Volta?
            # What is the ocean that borders African countries?
            "syn": "s(E1) -> 'what' 'is' np(E1) + '?'",
            "sem": lambda np: Atom("intent_list", E1, [np]),
        },
        {
            # What are the countries south of the Equator and not in Australasia?
            "syn": "s(E1) -> 'what' 'are' np(E1) + '?'",
            "sem": lambda np: Atom("intent_list", E1, [np]),
        },
        # {
        #     "syn": "s(E1) -> 'what' 'are' np(E1) vp_noobj_sub_iob(E1) + '?'",
        #     "sem": lambda np, vp_noobj_sub_iob: [('intent_list', e1, apply(np, vp_noobj_sub_iob))],
        # },
        {
            # What are the capitals of the countries bordering the Baltic?
            "syn": "s(E1, E2) -> 'what' 'are' 'the' noun(E1) 'of' np(E2) + '?'",
            "sem": lambda noun, np: Atom("intent_table", [E2, E1], ["", ""], [noun, Atom("of", E1, E2), np]),
            "boost": 1,
        },
        # {
        #     "syn": "s(E1) -> 'what' 'is' 'the' 'total' 'area' 'of' np(E2) + '?'",
        #     "sem": lambda np: [('intent_value_with_unit', e1, 'ksqmiles', [("sum", E1, E3, apply(np, []) + [('size_of', E2, E3)])])],
        # },
        # {
        #     "syn": "s(E1, E3) -> 'what' 'is' 'the' 'average' 'area' 'of' np(E2) preposition(E2, E3) 'each' nbar(E3) + '?'",
        #     "sem": lambda np, preposition, nbar: [('intent_table', [e3, e1], ['', 'ksqmiles'], nbar + [('avg', E1, E4, apply(np, preposition) + [('size_of', E2, E4)])])],
        # },
        # {
        #     "syn": "s(E2, E3) -> 'what' 'percentage' 'of' np(E1) tv(E1, E2) 'each' nbar(E2) + '?'",
        #     "sem": lambda np, tv, nbar: [('intent_table', [e2, e3], ['', ''], nbar + [('percentage', E3, apply(np, tv), apply(np, []))])],
        # },
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
        # {
        #     "syn": "s(E1) -> 'which' np(E1) vp_nosub_obj(E1) + '?'",
        #     "sem": lambda np, vp_nosub_obj: [('intent_list', e1, apply(np, vp_nosub_obj))],
        # },
        {
            # How many countries does the Danube flow through?
            "syn": "s(E1) -> 'how' 'many' nbar(E1) vp(E1) + '?'",
            "sem": lambda nbar, vp: Atom("intent_value", E1, [Atom("count", E1, [nbar, vp])]),
        },
        # {
        #     "syn": "s(E1) -> 'bye' + '.'?",
        #     "sem": lambda: [('intent_close_conversation',)],
        # },
        # active transitive: sub obj
        # { "syn": "vp_nosub_obj(E1) -> tv(E1, E2) np(E2)", "sem": lambda tv, np: apply(np, tv) },
        {"syn": "vp(E1) -> verb(E1, E2) np(E2)", "sem": lambda verb, np: Atom(verb, E1, E2).mod(np)},
        # { "syn": "vp_nosub_obj(E1) -> 'does' 'not' vp_nosub_obj(E1)", "sem": lambda vp_nosub_obj: [('not', vp_nosub_obj)] },
        # { "syn": "vp_nosub_obj(E1) -> 'have' 'a' attr(E1, E2)", "sem": lambda attr: attr },
        # passive transitive
        # { "syn": "vp_noobj_sub(E1) -> tv(E2, E1) 'by' np(E2)", "sem": lambda tv, np: apply(np, tv) },
        {"syn": "vp(E1) -> verb(E2, E1) 'by' np(E2)", "sem": lambda verb, np: Atom(verb, E1, E2).mod(np)},
        {"syn": "vp(E1) -> 'does' np(E2) verb(E2, E1)", "sem": lambda np, verb: Atom(verb, E2, E1).mod(np)},
        # { "syn": "vp_noobj_sub(E1) -> 'is' tv(E2, E1) 'by' np(E2)", "sem": lambda tv, np: apply(np, tv) },
        # active transitive continuous
        # { "syn": "vp_nosub_obj_continuous(E1) -> tv_continuous(E1, E2) np(E2)", "sem": lambda tv_continuous, np: apply(np, tv_continuous) },
        {"syn": "vp(E1) -> verb(E1, E2) np(E2)", "sem": lambda verb, np: Atom(verb, E1, E2).mod(np)},
        # passive ditransitive: obj sub iob
        # { "syn": "vp_noobj_sub_iob(E1) -> 'from' 'which' np(E2) vp_noobj_nosub_iob(E1, E2)", "sem": lambda np, vp_noobj_nosub_iob: apply(np, vp_noobj_nosub_iob) },
        # { "syn": "vp_noobj_nosub_iob(E1, E2) -> dtv(E2, E1, E3) np(E3)", "sem": lambda dtv, np: apply(np, dtv) },
        # verbs
        {"syn": "verb(E1, E2) -> 'border'", "sem": lambda: "borders"},
        {"syn": "verb(E1, E2) -> 'borders'", "sem": lambda: "borders"},
        # transitive verbs
        {"syn": "verb(E1, E2) -> 'bordered'", "sem": lambda: "borders"},
        # { "syn": "tv(E1, E2) -> 'contains'", "sem": lambda: [('contains', E1, E2)] },
        {"syn": "verb(E1, E2) -> 'flow' 'through'", "sem": lambda: "flows_through"},
        # { "syn": "tv(E1, E2) -> 'exceeds'", "sem": lambda: [('greater_than', E1, E2)] },
        # { "syn": "tv_continuous(E1, E2) -> 'bordering'", "sem": lambda: [('borders', E1, E2)] },
        {"syn": "verb(E1, E2) -> 'bordering'", "sem": lambda: "borders"},
        # { "syn": "tv_continuous(E1, E2) -> 'exceeding'", "sem": lambda: [('greater_than', E1, E2)] },
        # ditransitive verbs
        # { "syn": "dtv(E1, E2, E3) -> 'flows' 'into'", "sem": lambda: [('flows_from_to', E1, E2, E3)] },
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
        # { "syn": "nbar(E1) -> nbar(E1) pp(E1)", "sem": lambda nbar, pp: nbar + pp },
        # { "syn": "nbar(E1) -> superlative(E1) nbar(E1)", "sem": lambda superlative, nbar: apply(superlative, nbar) },
        # relative clauses
        # { "syn": "relative_clause(E1) -> 'that' vp_nosub_obj(E1)", "sem": lambda vp_nosub_obj: vp_nosub_obj },
        {"syn": "relative_clause(E1) -> 'that' vp(E1)", "sem": lambda vp: vp},
        # { "syn": "relative_clause(E1) -> 'that' vp_noobj_sub(E1)", "sem": lambda vp_noobj_sub: vp_noobj_sub },
        {
            "syn": "relative_clause(E1) -> relative_clause(E1) 'and' relative_clause(E1)",
            "sem": lambda relative_clause1, relative_clause2: relative_clause1.mod(relative_clause2),
        },
        # { "syn": "relative_clause(E1) -> vp_nosub_obj_continuous(E1)", "sem": lambda vp_nosub_obj: vp_nosub_obj },
        {"syn": "relative_clause(E1) -> vp(E1)", "sem": lambda vp_nosub_obj: vp_nosub_obj},
        # { "syn": "relative_clause(E1) -> np(E2) preposition(E2, E1) 'which' vp_nosub_obj(E2)", "sem": lambda np, preposition, vp_nosub_obj: apply(np, preposition + vp_nosub_obj) },
        # { "syn": "relative_clause(E1) -> 'whose' attr(E1, E2) vp_nosub_obj(E2)", "sem": lambda attr, vp_nosub_obj: attr + vp_nosub_obj },
        # { "syn": "relative_clause(E1) -> 'with' 'a' attr(E1, E2) vp_nosub_obj_continuous(E2)", "sem": lambda attr, vp_nosub_obj: attr + vp_nosub_obj },
        # np
        # { "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar:
        #     SemanticFunction([Body], nbar + Body) },
        # { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar:
        #     SemanticFunction([Body], apply(det, nbar, Body)) },
        # { "syn": "np(E1) -> det(E1) attr(E2, E1) 'of' nbar(E2)", "sem": lambda det, attr, nbar:
        #     SemanticFunction([Body], apply(det, nbar + attr, Body)) },
        # { "syn": "np(E1) -> number(E1)", "sem": lambda number:
        #     SemanticFunction([Body], [('let', E1, number)] + Body) },
        # det
        {"syn": "det(E1) -> 'a'", "sem": lambda: Atom("a")},
        {"syn": "det(E1) -> 'the'", "sem": lambda: Atom("the")},
        # { "syn": "det(E1) -> 'a'", "sem": lambda:
        #     SemanticFunction([Range, Body], Range + Body) },
        # { "syn": "det(E1) -> 'the'", "sem": lambda:
        #     SemanticFunction([Range, Body], Range + Body) },
        # { "syn": "det(E1) -> 'some'", "sem": lambda:
        #     SemanticFunction([Range, Body], Range + Body) },
        # { "syn": "det(E1) -> 'any'", "sem": lambda:
        #     SemanticFunction([Range, Body], Range + Body) },
        # { "syn": "det(E1) -> 'no'", "sem": lambda:
        #     SemanticFunction([Range, Body], [('none', Range + Body)]) },
        # { "syn": "det(E1) -> number(E1)", "sem": lambda number:
        #     SemanticFunction([Range, Body], [('det_equals', Range + Body, number)]) },
        {
            "syn": "det(E1) -> number(E1)",
            "sem": lambda number: Atom("equals", number),
        },
        # {
        #     "syn": "det(E1) -> number(E1)",
        #     "sem": lambda number: SemanticFunction([Range, Body], [("det_equals", Range + Body, number)]),
        #     # "sem": lambda number: SemanticFunction([Range, Body], [("det_equals", Range + Body, number)]),
        # },
        # { "syn": "det(E1) -> 'more' 'than' number(E1)", "sem": lambda number:
        #     SemanticFunction([Range, Body], [('det_greater_than', Range + Body, number)]) },
        # { "syn": "superlative(E1) -> 'smallest'", "sem": lambda:
        #     SemanticFunction([Body], [('arg_min', E1, E2, Body + [('size_of', E1, E2)])]) },
        # attribute
        # { "syn": "attr(E1, E2) -> 'population'", "sem": lambda: [('has_population', E1, E2)] },
        # { "syn": "attr(E1, E2) -> attr(E1, E2) relative_clause(E2)", "sem": lambda attr, relative_clause: attr + relative_clause },
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
        # pp
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
        {"syn": "noun(E1) -> 'countries'", "sem": lambda: Atom("country", E1)},
        {"syn": "noun(E1) -> 'cities'", "sem": lambda: Atom("city", E1)},
        {"syn": "noun(E1) -> 'seas'", "sem": lambda: Atom("sea", E1)},
        # proper noun
        {
            "syn": "proper_noun(E1) -> /\\w+/",
            "sem": lambda token: Atom("name", E1, token),
        },
    ]
