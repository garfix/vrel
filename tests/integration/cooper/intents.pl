# intents condense the main objective of a sentence in a single predicate

# tell a fact
intent_tell(Fact, Truth) :-
    resolve_names(Fact, Resolved),
    (
        # check if the fact is known
        scoped(Resolved),
        not_equals(Truth, "unknown"),
        store(output_type(Truth))
    ;
        # add the fact as a truth
        let(Truth, "true"),
        create_records_3v(Resolved, Records),
        store(Records),
        store(output_type('ok'))
    ).

# learn an induction rule
intent_learn(Head, Body, T1, T2, Truth1, Truth2) :-
    (
        # try to find a counter example: Body AND NOT(Head)
        and_3v(
            Body,
            not_3v(Head, T1, T4),
            T2,
            T4,
            T3),
        equals(T3, 'true'),
        store(output_type('false'))
    ;
        # add the rule
        let(T1, Truth1),
        let(T2, Truth2),
        create_records_3v(Head, Head_r),
        create_records_3v(Body, Body_r),
        learn_rule(Head_r, Body_r),
        store(output_type('ok'))
    ).

intent_check(Fact, Truth) :-
    resolve_names(Fact, Resolved),
    scoped(Resolved),
    store(output_type(Truth)).
