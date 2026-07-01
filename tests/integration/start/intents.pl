# intent predicates

intent_single_name(E1, Sem) :-
    store(output_type('list'), output_list(Elements)).

intent_close_conversation() :-
    store(output_type('close_conversation')).
