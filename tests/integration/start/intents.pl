# intent predicates

intent_list(E1, Sem) :-
    find_all(E1, Sem, Elements),
    store(output_type('list'), output_list(Elements)).

intent_close_conversation() :-
    store(output_type('close_conversation')).
