intent_understand(Story) :-
    reify(Story, Reified),
    induce_facts(Reified),
    analyze_plans(Reified),
    # log_nodes(),
    out('understood').

intent_explanation(Question, C1) :-
    update_saliency(Question),
    # log_nodes(),
    explain(Question, C1, Explanation),
    out('explanation', Explanation).

