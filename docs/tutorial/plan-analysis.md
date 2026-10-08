Plan analysis rules are like this

    plan(ask(C1, E1, E2, F1)) => goal(know(C2, E1, F1)).
    ask(C1, E1, E2, F1) => plan(ask(C1, E1, E2, F1)).

and this

    lost(C1, E1) => plan(ask(C2, E1, E2, location(L1))) => goal(know(C2, E1, location(L1))).

The first ones have an antecedent and consequent, the latter has an antecedent, a plan, and a consequent.

The plan is potential, and will later be formed into a list of multiple plans.

## Two phases

For each new `current_subject` 2 ways are tried to create new connections: prediction and inference. Prediction is tried first, and when it succeeds, the plan analysis succeeds. If not, inference is tried.

Note: prediction must be tried before inference, and when prediction succeeds, inference should not be tried. Prediction, when succeeding inferece, would always match, and it would think that the latest node was predicted, while in fact it would just have been created by the inference.

## Prediction

Definitions

- `A => B`: the rule with antecedent `A` and consequent `B`
- `a -> b`: `A` has parent `B`

When an atom is named `a` in the context of a rule `A => B`, this signifies that `a` matches `A`.

- If `A => B` and `current_subject` matches `a`, and `b` was already established (in nodes), a link between `a` and `b` is created, and identities between `a` and `b` are created.
- If `A => Plan(s) => B` and `current_subject` matches `a`, and `plan -> b` was already established (in nodes), a link between `a` and `plan` is created, and identities between `a` and `b` and `plan` are created. If `plan` was empty, it will **stay empty**, but the variables of potential plans will bound.

## Inference

In an inference step a `current_subject` is an atom being processed, and matched against an antecedent. When it matches, the consequent is instantiated and added to the nodes list.

- If `A => B` and `current_subject` matches `A`, `B` is instantiated and added
- If `A => Plan(s) => B` and `current_subject` matches `A`, `B` is instantiated and added, and _an empty plan_ is added as well, **containing partially instantiated potential atoms**.
