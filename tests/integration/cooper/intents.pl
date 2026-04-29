# intents condense the main objective of a sentence in a single predicate

# tell a fact
intent_tell(Fact, Truth) :-
    resolve_names(Fact, Resolved),
    (
        # check if the fact is known
        create_records(Resolved, Records),
        scoped(Records),
        not_equals(Truth, "unknown"),
        store(output_type(Truth))
    ;
        # add the fact as a truth
        let(Truth, "true"),
        # print(Truth),
        # print(Resolved),
        create_records_3v(Resolved, Records),
        # print(Records),
        store(Records),
        store(output_type('ok'))
    ).

# learn an induction rule
intent_learn(Head, Body) :-
    create_records_3v(Head, Head_r),
    create_records_3v(Body, Body_r),
    learn_rule(Head_r, Body_r),
    store(output_type('ok')).

intent_check(Fact, Truth) :-
    log(Fact),
    resolve_names(Fact, Resolved),
    create_records(Resolved, Records),
    # print(Records),
    # print(Truth),
    scoped(Records),
    # print(Truth),
    store(output_type(Truth)).
