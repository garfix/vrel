# intent predicates

intent_list(E1, Sem) :-
    find_all(E1, Sem, Elements),
    out('list', Elements).

intent_close_conversation() :-
    out('close_conversation').
