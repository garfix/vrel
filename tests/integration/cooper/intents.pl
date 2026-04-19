# intents condense the main objective of a sentence in a single predicate

# tell a fact
intent_tell(Fact, Truth) :-
    resolve_names(Fact, Resolved),
    (
        # check if the fact is known
        scoped(Resolved),
        store(output_type(Truth))
    ;
        # add the fact as a truth
        let(Truth, "true"),
        create_records(Resolved, Records),
        store(Records),
        store(output_type('ok'))
    ).

intent_learn(Head, Body) :-
    resolve_names(Atom, Resolved),
    learn_rule(Head, Body),
    store(output_type('ok')).

# check
intent_check(Truth) :- store(output_type(Truth)).

