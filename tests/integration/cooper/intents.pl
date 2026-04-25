# intents condense the main objective of a sentence in a single predicate

# tell a fact
intent_tell(Fact, Truth) :-
    resolve_names(Fact, Resolved),
    (
        # check if the fact is known
        create_records(Resolved, Records),
        # print(Records),
        scoped(Records),
        store(output_type(Truth))
    ;
        # add the fact as a truth
        let(Truth, "true"),
        create_records_3v(Resolved, Records),
        store(Records),
        store(output_type('ok'))
    ).

# learn an induction rule
intent_learn(Head, Body) :-
    create_records_3v(Head, Head_r),
    create_records_3v(Body, Body_r),
    learn_rule(Head_r, Body_r),
    store(output_type('ok')).
