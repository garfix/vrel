# sentence-level predicates

# teach
intent_tell(Atom, Var) :-
    resolve_names(Atom, Resolved),
    (
        scoped(Resolved), store(output_type(Var))
    ;
        let(Var, "true"),
        create_records(Resolved, Records),
        store(Records),
        store(output_type('ok'))
    ).

intent_learn(Head, Body) :- resolve_names(Atom, Resolved), learn_rule(Head, Body), store(output_type('ok')).

# check
intent_check(Truth) :- store(output_type(Truth)).

