# report
intent_report(A, Facts) :-
    exec(Facts),
    out('report', A).
