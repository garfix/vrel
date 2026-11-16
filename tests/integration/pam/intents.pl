intent_understand(Story) :-
    reify(Story, Reified),
    create_records(Reified, Records),
    store(Records),
    update_saliency(Reified),
    log("reified", Reified),
    induce_facts(Reified),
    analyze_plans(Reified),
    resolve_anaphora(),
    # log_nodes(),
    out('understood').

intent_explanation(Question, C1) :-
    update_saliency(Question),
    # log_nodes(),
    explain(Question, C1, Explanation),
    out('explanation', Explanation).

intent_consequences(Question, C1) :-
    find_consequences(Question, C1, Consequence),
    update_saliency(Consequence),
    # log('C', Consequence),
    # log_nodes(),
    out('consequences', Consequence).
