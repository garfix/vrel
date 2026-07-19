intent_understand(Story) :-
    reify(Story, Reified),
    induce_facts(Reified),
    analyze_plans(Reified),
    out('understood').


intent_explanation(Question, C1) :-
    update_saliency(Question),
    explain(Question, C1, Explanation),
    out('explanation', Explanation).

