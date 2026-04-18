# sentence-level predicates

# teach
intent_tell(Atom) :-
    resolve_names(Atom, Resolved),
    create_records(Resolved, Records),
    print(Records),
    store(Records),
    store(output_type('ok')).

intent_learn(Head, Body) :- resolve_names(Atom, Resolved), learn_rule(Head, Body), store(output_type('ok')).

# check
intent_check(Truth) :- store(output_type(Truth)).

