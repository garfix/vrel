# intent predicates

optimize(SemIn, SemOut) :-
    create_query(SemIn, Q),
    optimize_cost_sort(Q, S),
    optimize_isolate(S, SemOut).

intent_list(E1, Sem) :-
    optimize(Sem, SemOpt),
    find_all(E1, SemOpt, Elements),
    out('list', Elements).

intent_table(Variables, Units, Sem) :-
    optimize(Sem, SemOpt),
    find_all(Variables, SemOpt, Results),
    out('table', Results, Units).

intent_yn(Sem) :- (
    optimize(Sem, SemOpt),
    exec(SemOpt),  out('yes')
;   out('no')
).

intent_value(Variable, Sem) :-
    optimize(Sem, SemOpt),
    find_one(Variable, SemOpt, Result),
    out('value', Result).

intent_value_with_unit(Variable, Unit, Sem) :-
    optimize(Sem, SemOpt),
    find_one(Variable, SemOpt, Result),
    out('value_with_unit', Result, Unit).

intent_close_conversation() :-
    out('close_conversation').
