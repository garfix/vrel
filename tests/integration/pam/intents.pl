intent_understand(Story) :-
    # log('story', Story),
    reify(Story, Reified),
    log('reified', Reified),
    induce_facts(Reified),
    analyze_plans(Reified),
    store(output_type('understood')).


intent_explanation(Question, C1) :-
    # log('question', Question),
    update_saliency(Question),
    explain(Question, C1, Explanation),
    # log('explanation', Explanation),
    store(output_type('explanation'), output_explanation(Explanation)).

