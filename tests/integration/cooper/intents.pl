# sentence-level predicates

# teach
intent_tell(Atom) :- print(Atom), create_records(Atom, Records), print(Records), store(Records), store(output_type('ok')).
intent_learn(Head, Body) :- learn_rule(Head, Body), store(output_type('ok')).

# check
intent_check(Truth) :- store(output_type(Truth)).

