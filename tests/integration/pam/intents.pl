intent_understand(Story) :-
    log('story', Story),
    store(output_type('understood')),
    reify(Story, Reified),
    store(Reified),
    induce_facts(Reified),
    analyze_plans(Reified).

intent_explanation(Question, C1) :-
    # log('question', Question),
    explain(Question, C1, Explanation),
    # log('explanation', Explanation),
    store(output_type('explanation', Explanation)).

