## 2026-08-14

I implemented the ellipsis in the parser, and that was easy, but I'm not very happy with that idea, because it seems pretty brittle. I prefer to have the power of the inferences when matching. That means rewriting the nested structure to a flat structure.

Structure A is being solved (needle), while B is turned into a data source (haystack). Both structures will need to be flattened.

A

    ask($19, `person:John`, $20, $21)
    tell($21, $20, $22, $23)
    where($23, $24)
    be($24, $25)
    he($25)

B

    ask(`entity:DLG8`, `entity:DLG9`, `entity:DLG10`, `entity:DLG11`)
    where(`entity:DLG11`, `entity:DLG12`)
    be(`entity:DLG12`, `entity:DLG13`)
    he(`entity:DLG13`, `entity:DLG14`)

As is, this fails on `tell`, which is not present in B. How to solve this?

    tell(X, B, C, D) :- ask(_, C, B, D) where(D, _)

This means: we can deduce that B told C where he was (D), if C asked B where he was

## 2026-08-12

A modifier can be attached to multiple arguments (rare).

    vp(C1, E1) -> vp(C1, E1, E2, E3) nominal(E2) nominal(E3, E2)

Currently the check if a modifier is attached to a argument is done by checking the occurrence of the variable anywhere in the modifier. Maybe this should just be the first argument of the top-level atom.

I made the change; the function is just used for printing the atom.

===

These should now match

```bash
A.                                                 B.

(ask                                               (ask
    1. $19                                             1. `entity:DLG8`
    2. `person:John`                                   2. `entity:DLG9`
    3. $20                                                modifier
        modifier                                             (he
            (farmer                                               1. `entity:DLG9`)
            1. $20)                                    3. `entity:DLG10`
    4. $21                                                modifier
        modifier                                             (him
            (tell                                                 1. `entity:DLG10`)
            1. $21                                     4. `entity:DLG11`
            2. $20                                        modifier
            3. $22                                          (where
                modifier                                        1. `entity:DLG11`
                    (him                                          2. `entity:DLG12`
                    1. $22)                                       modifier
            4. $23                                                  (be
                modifier                                                1. `entity:DLG12`
                    (where                                                2. `entity:DLG13`
                    1. $23                                                modifier
                    2. $24                                                  (he
                        modifier                                                1. `entity:DLG13`))))
                            (be
                            1. $24
                            2. $25
                                modifier
                                    (he
                                    1. $25)))))
```

long way to go

problems to solve:

- OK `$19` should match `entity:DLG8`
- OK `person:John` should match `entity:DLG9` (identity already established)
- DOABLE `$20` (farmer) should match `entity:DLG10` (him) => matches if `entity:DLG10` is farmer and male
- PROBLEMATIC `$21` (tell ... where ...) should match `entity:DLG11` (where ...)
- OK the structure below `where` is straightforward, because they are identical and one side is only variables

I suppose the problem (PROBLEMATIC) would not occur when using CD since these structures would result in the same uniform semantics. However, this just moves the problem to the parser.

idea: treat `A asked B where` as ellipsis when parsing, and construct semantics as `A asked B to tell A where`:

- `He asked him where he was.` => `He asked him to tell him where he was.`

## 2026-08-08

Thinking about why-requests to answer the questions correctly. "INIT-REQ is a why request" (p 297)

There are 2 why questions:

    "Why did John pull over to a farmer?"
    "Because he wanted to know where he was."

I don't know why this node is the answer. It is not the node from the init-req.

    "Why did John ask a farmer to tell him where he was?"
    "Because he wanted to get someplace."

I have several goals, from top to bottom:

- A. be_at(C1, E1, L2)
- B. know(C2, E1, location(L1))
- C. be_near(C1, E1, E2)

The answer is the top-most node for the second why-question, but the answer is the node above the first goal for the first question.

Maybe the algorithm is as follows:

- find the node that represents the question
- going up, find the first goal
- then go up until the next goal
- that is the answer

If the answer would be the first goal up, you would get:

    "Why did John pull over to a farmer?"
    "Because he wanted to be near a farmer."

    "Why did John ask a farmer to tell him where he was?"
    "Because he wanted to know where he was."

Which, we can agree, is not very informative.

Applying this to "Why did Willa pick up a Michelin guide?" this results in something like "Because she wanted to know the distance to a restaurant."

## 2026-08-07

In order to pass substructures as part of an inference, do I need a new transformation?

Would I still be able to query it? How is this used; wait until I know.

## 2026-08-06

node 2 has action 0 => this follows logically from the implementation. "lost" is not part of the objects in pages 304/305

When "John was lost" is processed, PAM creates a goal for it, but apparently the relation between the fact "John was lost" and this goal of knowing where he is is not stored. Maybe I should add this to the rule, but for the moment the existence of the extra action doesn't hurt.

A syntax could be:

    lost(C1, E1) -> Plan => goal(know(C2, E1, location(L1))).

Where `->` denotes that the one causes the other, but no relation should be stored (the fact is not an action of the plan)

## 2026-08-05

I need to add links between nodes before they are "approved" and added to memory. I need to do this because I now need the goal of the plan of a goal.

This makes more explicit the problem that has been accumulating, namely, that nodes are added to the set of nodes, some of which should be discarded, as leading to nowhere.

I will need to create a temporary (within sentence) node set and a more permanent (within dialog) node set.

## 2026-08-02

The first 2 sentences have been turned into explanation nodes: "John was lost. He pulled over to a farmer standing by the side of the road.".

Now I need to unify two goals.

    [2] Goal
    (goal
        1. [
            (know
                1. `entity:PA1`
                2. `person:John`
                3. [
                    (location
                        1. `entity:PA2`)
                ])
        ])
    attempts: [3]

and

    [5] Goal
    (goal
        1. [
            (know
                1. `entity:PA6`
                2. `entity:DLG3`
                3. [
                    (location
                        1. `entity:PA7`)
                ])
        ])
    attempts: [6]

## 2026-08-01

I first added the new nodes in `try_rules`, then remembered that that's what the `check_init_req` was for. So now I'm checking there for the unknown plan. So far so good.

## 2026-07-30

I can be good to give the goals and plans names:

    use_vehicle: plan(use_vehicle(C1, E1))

    use_vehicle => be_at_location

This makes the rules easier to read and clearly shows how the plans and goals reoccur in other rules.

On the other hand, the way the variables that connect them are linked is gone.

## 2026-07-29

Following the explanation of PAM in chapter 14 is like wandering through a maze. If you ever hope to find out how to make it work, you must set yourself short-term goals and try to fulfill them, partly using the knowledge given, but also being content with just reaching your own goals, knowing that you cut off some corners in the process. Is it really necessary to build all these structures? It looks hopelessly complicated.

MicroPAM is declarative, and allows for an DSL, where PAM uses full Lisp structures for rules/requests and these are open ended. The full-lisp way is unmanageable and unlearnable for a novice. And since Wilensky wrote MicroPAM he is telling us that the declarative way is the way forward. Therefore we try this and hope (but not know!) that it leads to the solution. We can always "backtrack" but that won't be fun.

## 2026-07-26

Waarom blijven de inducties van "John was lost" bestaan? Ze vormen geen explanation.

"The only requests around at the beginning of a story are looking for goal episodes and static information (e. g., “John lived in New York” )"

"Now when the episode built by LOC-SUBGOAL-REQ is placed in IN, the
condition of INIT-REQ is met. INIT-REQ is a request activated at the
beginning of PAM, and which looks for a goal episode whose source is a
theme, or an unknown plan. Since the latter case holds for the goal
structure above, INIT-REQ fires."

PAM, contrary to MicroPAM has declarative/procedural rules that build nodes. I'm not sure yet if I need these, and if they should be in Python or in an DSL structure. Story-independent rules can be implemented in Python.

Let's try to recreate this INIT-REQ. It can't be implemented as a simple induction rule, but it can be implemented in the algorithm.

I think I need to create an extra node to turn what's basically a single list, the explaining plans and goals in MicroPAM, into a dag. This is necessary for more complicated stories, and they quickly get complicated, wherein the pieces of information don't immediately string together anymore.

Node (GoalNode, PlanNode, ThemeNode)

shared attributes, in order to create a dag

- parent
- children

PAM has the `*goal-episode*` node with `source` (parent) and `attempts` (children), and the `plan` node with `source` (parent) and `subepisodes` (children).

## 2026-07-25

New plan for the story. I'm reexamining the example in chapter 14. This changes things.

- A. John was lost.
- B. He pulled over to a farmer standing by the side of the road.
- C. He asked him where he was.

travel planning

- [A] goal(know(C1, E1, location(C2, E1, L1))) => Plan => goal(be_at(C1, E1, L2)). . . . . => this P2 will remain unresolved, but is essential to INIT_REQ
- [A] lost(C1, E1) -> goal(know(C2, E1, location(C2, E1, L1))).

general problem solving

- [B] goal(be_near(C1, E1, E2)) => Plan => goal(know(C2, E1, location(C2, E1, L1))).
- [B] plan(use_vehicle(C1, E1, E2)) => goal(be_near(C2, E1, E2))

- [C] plan(ask(C1, E1, E2, F1)) => goal(know(C2, E1, F1)) . . . . . . . => then the plan(ask) will replace plan(P1)

actions

- [B] pull_over(C1, E1) to(C1, E2) => plan(use_vehicle(C2, E1, E2)).
- [C] ask(C1, E1, E2, F1) => plan(ask(C1, E1, E2, F1)).

## 2026-07-24

Trying to understand how a plan is inserted between two goals.

```
HUNGER-RULE

 Action:
    [BUILD '((GOAL (*S-HUNGER* PLANNER (NIL))
              SOURCE (*THEME* VAL (*HUNGER-DRIVE*))
              PLAN (NIL) ))]
```

This action part of a rule indicates that PAM tries to build causal structures by creating loose clusters of nodes, then combining them. This is different from MicroPAM which just links two adjacent nodes.

This build structure is not enough reason to abandon the current X => Y induction rules that I have.

A "missing" plan is called a "gap", and there must be a rule that describes which plans can fill the gap. These rules are called "suggestions". Here's an example suggestion:

```
Suggestions: [( (PLAN) !INPUT! SUITABLE-PLAN-RULE)]
```

This says: the gap must be filled by a plan that is a suitable-plan-rule.

```
SUITABLE-PLAN-RULE

 Condition:    SUITABLE-PLAN-PREDICATE

 Action:       !FOCUS!
```

The rule simply suggests a predicate.

"This condition, SUITABLE-PLAN-PREDICATE, examines a list of plans associated with a goal to determine if the input is a plan for that goal. Since _DO-$RESTAURANT-PLAN_ is contained in the list of plans for the goal _S-HUNGER_, the predicate returns true." (p 272-273)

This is a big find. As all plans and goals have names, the suggestion simply names the allowed plans for the gap.

The question comes to mind: is it necessary to name all plans, and create a list of allowed plans, if we already know the relations between plans and goals through the induction rules.

- goal(be_near(C1, E1, E2)) => plan(P1) => goal(know(C2, E1, F1))

Every plan that is the antecedent to a rule whose consequent matches the goal here can replace plan here, right?

- plan(ask(C1, E1, E2, F1)) => goal(know(C2, E1, F1))

So if the input is `ask(C1, E1, E2, F1)`, this leads to `plan(ask(C1, E1, E2, F1))` and since there are gaps left, this plan is matched against existing rules to see if they lead to the goal following the plan gap.

## 2026-07-23

I think it's better to introduce constants, because storing variables in the database should be avoided if possible.

===

Regarding

extra

- plan(travel_to(C3, E1, L2)) => goal(be_at(C1, E1, L2)).

problems

- lost(C1, E1).

travel planning

- not(lost(C1, E1)) -> lost(C1, E1).
- goal(know(C1, E1, location(C2, E1, L1))) => not(lost(C3, E1)).
- goal(know(C1, E1, location(C2, E1, L1))) => plan(travel_to(C3, E1, L2)).

general problem solving

- plan(ask(C1, E1, E2, F1)) => goal(know(C2, E1, F1)).
- plan(use_vehicle(C1, E1, E2)) => goal(be_near(C2, E1, E2))

- goal(be_near(C1, E1, E2)) => plan(ask(C2, E1, E2, location(C3, E1, L1))).

actions

- pull_over(C1, E1) to(C1, E2) => plan(use_vehicle(C2, E1, E2)).
- ask(C1, E1, E2, F1) => plan(ask(C1, E1, E2, F1)).

===

this one seems to too story-specific

- goal(be_near(C1, E1, E2)) => plan(ask(C2, E1, E2, location(C3, E1, L1))).

what about this

- goal(be_near(C1, E1, E2)) => plan(tell(C2, E1, E2, F1)).
- plan(ask(C2, E1, E2, F1)) => plan(tell(C2, E1, E2, F1))
- ask(C1, E1, E2, F1) => plan(ask(C1, E1, E2, F1)).

but if i do that, the `ask` node will not placed just between the two goals. This seems to be the problem Wilensky solved by introducing the complicated technique.

my aim is to fill the argument F1 with new information

===

PAM's rule `USE-PERSON` is supposed to be quite abstract, but it basically says: A wanted to be near B in order to know A's location. That is actually quite specific. The range of possible plans connecting the two must be quite small. In fact the plan found later seems to be one of few possibilities. Why then this special construction?

Because even though it is a likely plan, we can't just guess it. Once the chain of plans/goals leads to an explanation, it is stored in memory as facts. The farmer might also have given John a piece of paper with his location, as part of a quiz.

But how does this inserting of plan nodes in a causal chain work exactly?

## 2026-07-22

Based on the reasoning below this is seems to be a working set of rules to answer the questions.

- plan(travel_to(C3, E1, L2)) => goal(be_at(C1, E1, L2))
- lost(C1, E1)
- not(lost(C1, E1)) -> lost(C1, E1)
- goal(know(C1, E1, location(C2, E1, L1))) => not(lost(C3, E1))
- goal(know(C1, E1, location(C2, E1, L1))) => plan(travel_to(C3, E1, L2))
- plan(ask(C1, E1, E2, F1)) => goal(know(C2, E1, F1))
- goal(be_near(C1, E1, E2)) => plan(ask(C2, E1, E2, location(C3, E1, L1)))
- plan(use_vehicle(C1, E1, E2)) => goal(be_near(C2, E1, E2))
- pull_over(C1, E1) to(C1, E2) => plan(use_vehicle(C2, E1, E2))

===

The plan analyzer matcher couldn't handle variables in atoms, as it needed to store them temporarily in a data store. Therefore I will now generate constants for induced facts. That seems to be an okay thing to do.

Update: I will not generate constants, because that would decrease the chance of matching. (Does it, because matching in this module may include same as bindings ...) In stead, I will change PlainReadWriteModule to allow storing variables. That seems to be an okay thing to do.

PAM's rules don't seem to introduce many variables, as it can do without mostly, but it _does occur_.

## 2026-07-21

About the unknown plan, let's try to find out how the match to the position between the goals caan be made

the goals:

    NAMED-PLAN USE-PERSON RELATES
    GOAL:
    (*DPROX*
        PLANNER HUMO
        OBJECT HUMO
        LOCATION (*PROX* PART HUM1))

                                                                            <---------------- this rule creates a REQUEST
    TO
    GOAL:
    (*DKNOW*
        PLANNER HUMO
        RECIPIENT HUMO
        FACT (
              (ACTOR HUMO IS (*PROX* PART (*UNSPEC* CLASS (*LOCATION*) )))  <------- link A
              TIME (TIMK2)))

the new fact:

    ((ACTOR HUM3 <=> (*MTRANS*)
        MOBJECT
        ((CON
            ((ACTOR HUM4 <=> (*MTRANS*)
                MOBJECT
                ((ACTOR HUM5 IS (*PROX* PART (*UNSPEC* CLASS (*LOCATION*))))
                    TIME (FORM43))
                TO (*CP* PART HUM3)
                TIME (FORM44))
            LEADTO
                ((ACTOR HUM3 TOWARD (*JOY* VAL (NIL)))
                    INC (2.) TIME (FORM45))))
        TO (*CP* PART HUM4))
        TIME (FORM46))

the rule:

    EXPLANATION IS
    PLAN:

    (*PB-ASK*
        PLANNER HUMO
        PERSUADEE HUM1
        REQUEST                                                             <---------------- REQUEST
            ((ACTOR
                    HUM1
                    <=> (*MTRANS*) MOBJECT
                                    ((ACTOR HUMO                            <------- link A
                                            IS (*PROX*
                                                PART (*UNSPEC*
                                                        CLASS (*LOCATION*))))
                                            TIME (TIMK7))
                    TO (*CP* PART HUMO))
        TIME (TIMK6)))

"link A" in the ask planbox matches the "link A" in the rule. The planbox has a `REQUEST` attribute. Somehow a link can be made between those.

But I will try to solve the story without this extra complication first.

## 2026-07-19

Story: John was lost. He pulled over to a farmer standing by the side of the road. He asked him where he was.
Q: Why did John pull over to a farmer?

Before looking at clues in Wilensky's doctoral thesis, let me try to model the causal chains myself.

- pull_over(C2, E1) to(C2, E2) => plan(be_near(E1, E2)).

Remarks:

- right hand side must be a single plan or goal
- when exactly is something a goal or a plan?
  - plans are verbs; goals are states
- start with rewriting actions to plans/goals (bottom-up); the plan is just a little more abstract
  - John was lost. : No plan
  - He pulled over to a farmer standing by the side of the road. : pull_over_to => goal(be_near)
  - He asked him where he was. : ask location => goal(know(location))
- continue by rewriting actions to goals
  - goal(not(lost)) => lost
- fill in the steps between these nodes
  - goal(know(location)) => goal(not(lost))
  - goal(be_near) => plan(ask(location))
  - plan(ask(location)) => plan(know(location))
- the last sentence "He asked him where he was." is not superfluous: usually when someone drives there care over to you, they want to know the route to some destination

The chain

- lost(C1, E1)
- goal(not(lost(C1, E1)))
- goal(know(C1, E1, location(C2, E1, L1)))
- plan(ask(C1, E1, E2, location(C2, E1, L1)))
  - # alternative: ask the route
  - plan(ask(C1, E1, E2, route(C2, E1, G1)))
- goal(be_near(C1, E1, E2))
- pull_over(C1, E1) to(C1, E2)

Now for the questions

                ["Why did John pull over to a farmer?", "Because he wanted to know where he was."],
                ["Why did John ask a farmer to tell him where he was?", "Because he wanted to get someplace."],
                ["What were the consequences of John's pulling over to a farmer?", "This enabled him to ask him where John was."],
                ["What happened when John pulled over to a farmer?", "He asked him to tell him where he was."],
                ["What happened when John asked a farmer to tell him where he was?", "I don't know."],
                ["How did John go over to a farmer?", "He drove over to him."]

can we answer them?

Okay, he's not just lost. Being lost is just a state within the plan to get somewhere. Adapting ... The goal of not being lost we can skip.

- lost(C1, E1)
- not(lost(C1, E1)) -> lost(C1, E1)
- plan(travel_to(C3, E1, L1)) => goal(be_at(C1, E1, L2))
- goal(know(C1, E1, location(C2, E1, L1))) => not(lost(C1, E1))
- goal(know(C1, E1, location(C2, E1, L1))) => plan(travel_to(C3, E1, L2))
- plan(ask(C1, E1, E2, F1)) => goal(know(C1, E1, F1))
- goal(be_near(C1, E1, E2)) => plan(ask(C1, E1, E2, location(C2, E1, L1)))
- goal(be_near(C1, E1, E2)) => plan(ask(C1, E1, E2, route(C2, E1, G1)))
- plan(go_to(C1, E1, E2)) => goal(be_near(C1, E1, E2))
- pull_over(C1, E1) to(C1, E2) => plan(go_to(C1, E1, E2))

Something like this?

===

Checking chapter 14 of the thesis, and paraphrasing, yields

- lost(C1, E1)
- goal(know(C1, E1, location(C2, E1, L1))) => lost(C1, E1) (FIND-OUT-REQ, p 293)
- goal(know(C1, E1, location(C2, E1, L1))) => plan(travel_to(C3, E1, L2)) (UNK-DPROX-REQ, p 297)
- plan(travel_to(C3, E1, L2)) => goal(be_at(C1, E1, L2)) (LOC-SUBGOAL-REQ, p 297)

- plan(P1) => goal(know(C1, E1, F1)) (USE-PERSON, p. 300)
- goal(be_near(C1, E1, E2)) => plan(P1) (USE-PERSON, p. 300)
- plan(use_vehicle(C1, E1, E2)) => goal(be_near(C1, E1, E2)) (USE-VEHICLE-GOAL-EPISODE-REQ, p. 300)
- pull_over(C1, E1) to(C1, E2) => plan(use_vehicle(C2, E1, E2)) (USE-VEHICLE-REQ, p. 299)

- ask(C1, E1, E2) => plan(P1) (ASK-REQ, p. 302)

PAM posits an unknown plan that connects the goals `goal(be_near(C1, E1, E2))` with `goal(know(C1, E1, F1))`. The third sentence then connects the `ask` action to this unknown plan. This looks very complicated and is not part of MicroPAM. I will first try if I can get the desired result without this technique.

## 2026-07-18

Is the nested semantic structure that MicroPAM uses essential or not? We know that MicroPAM added some extra clauses to overcome limitations, as in

```
            [
                [['goal', ['planner', '?x'],
                          ['objective', ['know', ['actor', '?x'],
                                                 ['fact', ['is', ['actor', 'restaurant'], ['prox', '?z']]]]]]],
                [['read-plan', ['planner', '?x'], ['object', '?w']], ['isa', 'restaurant-guide', '?w']]
            ],
```

Here `['isa', 'restaurant-guide', '?w']` is an extra condition, and apparently couldn't be included in the main part.

===

I want to introduce an event variable in `hungry(E1)`, like `hungry(C1, E1)`, but that would mean that there as 2 kinds of adjp, right? "the hungry boy" and "the boy is hungry" would be different semantically.

Adding be would solve it, but make the rules in PAM more verbose. Also, introducing `be` for a copula feels wrong.

===

Claude says that this is the Davidsonian representation of "the hungry boy"

    λx [boy(x) ∧ ∃s [hungry(s) ∧ Holder(s, x)]]

This is semantically right, but practically verbose. It adds an atom to every adjective. And I think there's the actual problem here. In "the hungry woman", the woman is just hungry. In all worlds. In "the woman was hungry", or "Willa was hungry", the state needs to be temporary, because the goal of the story is for Willa to cease to be hungry.

===

I'm going for

    hungry(S, E1) name(E1, 'willa')

`hungry` will be an event/state relation, and it is bound directly to its subject

## 2026-07-16

which is better:

- be(S, E1, E2) hungry(E2) name(E1, 'willa')
- hungry(S, E1) name(E1, 'willa')
- be(S1, E1, hungry(E2))
- hungry(S) holder(S, E1) name(E1, 'willa')

the second would give us 2 groups of adjp's, so no

## 2026-07-13

in "he asked him where he was" i say that 'he' and 'him' are np's, but so far i say that "where he was" is a relative clause. but i want to say that all are either np's or relative clauses. what is the common category that spans both?

Claude:

The common category is "noun clause" (also called a nominal clause or content clause), which is itself a subtype of the broader category "nominal." A noun clause is a clause that does the job an NP would normally do — subject, object, complement, etc.

## 2026-07-07

For the sake of the start module, that shows the simplicity of the module, I'm redesigning the output function.

- the BasicOuputBuffer stays but will be automatically loaded
- new output will be added a list in the output buffer
- last_output will be compared to the last output in the list using unification

## 2026-06-24

I implemented a simple PronounModule and resolved Willa to "she".

## 2026-06-23

I'm introducing the predicate `feature` to hold syntactic/semantic features.

## 2026-06-22

I started a `PronounModule` to be able to test if a certain pronoun is suitable for an entity, in the generation of a sentence. See `pronouns-generation.md` and `pronouns-updating-saliency.md`.

I thought about adding the update-saliency step in the execution processor, but as it turns out, this is not a good idea.

When the semantics is

    (intent_understand
        1. [
            (get_into
                1. $6
                2. $7
                3. $8
                1. modifier
                    (car
                        1. $8
                        1. modifier
                            (her
                                1. $9))
                2. modifier
                    (she
                        1. $7))
        ])

The subject that deserves most saliency is not `[get_into ...]`, which is the "subject" of `intent_understand`, but rather `$6`, the subject of `get_into`. This means that the current architecture pushes me in the direction to implement update-saliency as a function call.

===

As for `get_into($6, $7, $8)`, which argument is the subject? For eventless relations this is the first one, by convention. But for event-bearing relations, it is the second argument.

## 2026-06-03

I want to add a `match` function next to `solve`, that will try to match two atom lists.

    match(Needle, Haystack)

Where Needle may be

    [
    (grasp
    1. S1
    2. E1
    3. E2)]

and Haystack

    [
    (pick_up
        1. 'DLG1'
        2. 'DLG2'
        3. 'DLG3'),
    (michelin_guide
        1. 'DLG3'),
    (she
        1. 'DLG2')]

This is easiest to implement as a model with the haystack as contents, with some additional deduction rules.

## 2026-05-31

In CHAT-80 I stumble over the difference between a Relation and the used columns within the relation. Often not all columns are used.

===

In CHAT-80 I have a case where two id's don't match, because their type is different, and the types have a subordinate relationship (ocean < area).

select from border where:

    [ocean:southern_ocean, $2]

result:

    [area:southern_ocean, area:atlantic]

This is because `borders` has areas as types.

Have not solved it yet, because it could be avoided by less checking result values.

## 2026-05-30

Introducing Id(id, type).

Interesting issue: how to handle `same_as()`, with 2 Id arguments? When stored in the database, the default action is to hydrate the Id's into their `id`, but this would defy the purpose of the Ids in the same-as relation. So same_as needs a custom storage/retieve function that turns the id's into strings (json).

## 2026-05-28

Looking for a way to fix

salt is natrium chloride

remarks:

- by resolving the names before everything else, only the id's are given in the sentence, so the meaning effectively becomes `same_as(11, 24)`. the types of the entities are lost, and we can only enter `same_as('entity', 11, 24)`, while we want to enter the more specific `same_as('person', 11, 24)`.
- maybe I can give all entities in the sentence a dialog id, and store information about these entities in the dialog context
  - resolving the name: `name("DLG25", "John") type("DLG25", "person") id("DLG25", 114)`
  - resolving the name (2): `name("DLG25", "John") same_as("person", "DLG25", 114)`
  - same as: `same_as("person", "DLG25", "DLG22")`. I can look up the type of the id's in the dialog context
  - same as (2): `same_as("person", 114, 13)`. I can look up the type of the id's in the dialog context
  - but why give some entities an id and not others?
  - i can add other dialog information as well, like `plural("DLG24")`, but that wouldn't help much, except for named entities
- maybe I can store the entities of the names in the sentence context, especially for these kinds of sentences with same-as: `{$25: 'person'}`.
- i can replace the names by objects while resolving: `pats(Id(114, 'person'), $8)`, but the deduction rules don't like that (is that so?)
- Is it possible to link dialog variables to information? `type($25, 'person')`? Maybe, but the variables disappear on name resolution.

What if I replace a variable (`E1`) with an id (`ID(114, 'person')`). It's possible. It would solve the same-as thingy. `same_as` could have 2 pairs of arguments: `same_as(id1, type1, id2, type2)`. The Id-objects can be replaced with their id's on query time. You can pass them around like scalars. You would know their type.

## 2026-05-27

Applying same-as id variants requires that the system knows which parameters are id's. If not, and the id's are numeric, even non-ids will get variants. For instance if id 50 is same as id 69, and some person has age 69, the same as will apply to this age as well. Obviously unacceptable. For non-numeric id's this could perhaps be avoided by requiring them to have a special prefix. Also for numeric identifiers we really need a prefix, because the id of a person is in a different namespace as the id of a building.

So basically there are two paths in solving the issue:

- demand that each relation specify the types of its parameters (currently this is not done); this doesn't solve the namespace problem yet
- namespace all identifiers and prefix with an unlikely term: `@#$person-1` for example. The prefix can easily be made configurable. namespacing can include databases as well: `@#$administration/person-1`. The problem here is how apply the modified id's in the working code. It seems user unfriendly.

===

I will give each parameter a type, and the type is an entity type (i.e., person, company, etc). These types typically match the tables in which the entities are stored.

Then I will add an `entity_type` column to the `same_as` table, so that I can check which `same_as` ids I can use.

===

This is a problem, because we don't know the enitity type here (from Cooper):

```
    # salt is natrium chloride
    # magnesium is magnesium
    {
        "syn": "s() -> proper_noun(E1) 'is' proper_noun(E2)",
        "sem": lambda proper_noun1, proper_noun2: Atom(
            "intent_tell",
            [Atom("same_as", proper_noun1, proper_noun2), Atom("let", T1, "true")],
            T1,
        ),
    },
```

The moment that names are resolved you know their entity type. These are currently not stored, but they could be stored somewhere. Perhaps we could replace the names by dialog constants, in stead of database ids. Then we could add the entity type as information to the dialog context.

"John pats the dog"
pats(E1, E2) name(E1, "John")
pats(DLG25, E2) name("DLG25", "John") type("DLG25", "person") id("DLG25", 114)
or
pats(DLG25, E2) same_as("person", "DLG25", 114)

## 2026-05-24

Storyline: She picked up the Michelin guide.

```
 [(pick_up
    1. $3
    2. $4
    3. $5
    1. modifier
         (michelin_guide
            1. $5)
    2. modifier
         (she
            1. $4))]
```

question: Why did Willa pick up a Michelin guide?

```
[(pick_up
    1. $11
    2. 'Willa'
    3. $12
    1. modifier
         (michelin_guide
            1. $12))]

```

Problems in matching these:

- pronoun resolution: she => Willa

===

I installed Claude Code on my machine, and asked it to analyze the Vrel codebase. Then I asked it to create a basic MCP server for CHAT-80.

It's in the `examples` directory.

The interesting thing about this is that it enables an LLM to use Vrel as a tool to answer questions. The added benefit of Claude is that it has a much wider scope of the human language possible, and can convert it into an expression that Vrel (CHAT-80) can understand. The added benefit of Vrel is that it can query a database expressively and efficiently.

For example: I asked Claude:

❯ What is the size of the smallest asian country?

Claude:

```
● vrel-chat80 - ask_geography (MCP)(question: "What is the size of the smallest Asian country?")

● vrel-chat80 - ask_geography (MCP)(question: "What is the area of the smallest Asian country?")

● vrel-chat80 - ask_geography (MCP)(question: "Which is the smallest Asian country?")
  ⎿  {
       "result": "bahrain"
     }

● vrel-chat80 - ask_geography (MCP)(question: "What is the area of Bahrain?")

● vrel-chat80 - ask_geography (MCP)(question: "How large is Bahrain?")
  ⎿  {
       "result": "0 ksqmiles"
     }

10:53 AM claude-opus-4-7
● The smallest Asian country in Chat-80's data is Bahrain, with an area of 0 thousand square miles (i.e. it rounds to zero at that resolution — under ~500 sq mi).

```

Interestingly, CHAT-80's test sentence "How large is the smallest american country?" doesn't report the name of the country, just the size. Claude split the question in two subquestions: "Which is the smallest Asian country?" and "How large is Bahrain?"

## 2026-05-21

So why do we need sentence molecules for PAM? (Atom based sentences)

PAM has a predict phase and an inference phase.

In the inference phase the current subject is simply matched against the antecedent and the consequent, bound to values, is added to the known goals. Here in fact the molecule is counterproductive and needs to be flattened before it can be matched, because a match condition may be a modifier of the main verb.

The predict phase tries to link the current subject with a known item, by matching the subject with the antedent and the item with the consequent.
Here the current subject is also matched against the antecedent of a rule, so this needs flattening as well. The consequent is always a single atom to there's no need to flatten atoms.

Yet, even though the hierarchical structure of PAM's sentences was one of the reason to start looking for a hierarchical sentence structure, to ease the matching process, there is as yet no convincing reason to do so. I will put this in my todo list to come back to, as I suspect it to be important at some point. But that point has not yet arrived.

---

Reminder:

"PAM flags those requests that provide explanations as being WHY requests". Inside ... (p.172) While this is about deciding when to stop making inferences, it can also tell an answerer when a fact can be used as an answer to a **why** question.

---

Put all known actions, plans, goals and themes in a list and use their index as an identifier. Then use this identifier to create causal links.

- 0: goal A
- 1: theme A
- 2: plan B
- 3: goal C

- cause(1, 3)
- cause(3, 0)

Then, when someone asks "why X", find X by matching it with the known goals list, and use the causal links to find an answer.

## 2026-05-20

Resuming PAM.

Why did Willa pick up a Michelin Guide?

```
pick_up(C1, Willa, M1)
    michelin_guide(M1)
```

I have not stored the deduction relations. How can I do that?

```
reason(
    pick_up(C1, Willa, M1),
    plan(take(C2, Willa, M1))
)
```

or

```
reason(C1, C2)
```

## 2026-05-16

I will extend the sentence request with a solver, so that it becomes available even before the first sentence is executed (to write error tuples, for example).
The executor will be responsible for resolving names and constants, and for executing attached code.

Or I can add the solver to the system, and make changes to the SentenceRequest. Everytime the SentenceSemantics changes the request is updated.

## 2026-05-13

I'm trying to use the simple `vp` as much as possible, but making an exception for the continuous, that marks a relative clause. Without it its hard to create the proper sentence structure.

---

I rewrote all Chat-80 sentences. Speed is slower than Richard still: 0.42s against 0.64s. I'look into that, as well as some other things.

## 2026-05-12

I need a way to represent a number as an np like in "exceeds 1 million".

    np(E1) -> number(E1)
    Atom("$constant", E1, number)

===

Vrel:

```
 (continent
    1. $53),
 (scope
    1. [
         (none
            1. $54
            2. [
                 (country
                    1. $54)
                 (in
                    1. $54
                    2. $53)
            ]
            3. [
                 (det_greater_than
                    1. $57
                    2. [
                         (city
                            1. $57)
                         (has_population
                            1. $57
                            2. $60)
                         (exceeds
                            1. $60
                            2. 1000000)
                    ]
                    3. [
                         (contains
                            1. $54
                            2. $57)
                    ]
                    4. 2)
            ])
    ])]
```

richard:

```
[
    ('continent', $1)
    ('scoped',
        [
            ('none',
                [
                    ('country', $2)
                    ('in', $2, $1)
                    ('det_greater_than',
                        [
                            ('contains', $2, $3)
                            ('city', $3)
                            ('has_population', $3, $4)
                            ('let', $5, 1000000)
                            ('greater_than', $4, $5)
                        ], 2)
                ])
        ])
]

```

Vrel is here much slower, because the sort by cost is about `range + body`, and vrel about both individually. Need to fix.

## 2026-05-11

Determiner / quantifier

- Code sentence molecule minimaal
- Duidelijke betekenis
- De determiner moet herkenbaar zijn in de molecule
- de determiner in de query moet wel uitvoerbaar zijn en resultaat opleveren

"sem": lambda number: Atom("det_equals", Range, Body, number),

## 2026-05-08

As the arguments and modifiers give me multiple ways to do the same thing, I need to think about the right way to do them all.

- questions
- commands
- statements

For questions the form with the variable arguments works best.
For commands a form with an atom for each argument works best.
For pam, a form with an atom for each argument works best.

```
"syn": "s() -> np(E1) verb(E1, E2) np(E2)"
    [Atom(verb, E1, E2).any([np1, np2])]

"syn": "s() -> np(E1) vp(E1)"
    [vp.any([np])]
"syn": "vp(E1) -> verb2(E1, E2) np(E2)"
    Atom(verb, E1, E2).any([np])

SHRDLU / nli-go
{ rule: vp_imperative(P1) -> 'put' np(E1) 'on' 'top' 'of' np(E2),                 sense: go:do($np1, go:do($np2, dom:do_put_on_smart(E1, E2))) }

MicroPAM
[
    [['goal', ['planner', '?x'], ['objective', ['is', ['actor', '?x'], ['state', ['hunger', ['val', [0]]]]]]]],
    [['do-$restaurant-plan', ['planner', '?x'], ['restaurant', '?y']]]

],
```

It's not possible to create a tree from a flat tuple structure, but it is possible to create a flat structure from a tree. Therefore the sentence semantics must remain a tree as much as possible. But

- what about the modifiers? Are they still needed?
- what about `[vp.any([np])]`, `Atom(verb, E1, E2).any([np])`. Is that still possible?
- what about relative clauses?

An example

    What is the ocean that borders African countries and that borders Asian countries?

    What is E1
        borders(
            [ocean(E1)],
            [african(E2), country(E2)]
        ),
        borders(
            [ocean(E1)],
            [asian(E2), country(E2)]
        )

    What are the continents no country in which contains more than two cities whose population exceeds 1 million?

    continent(E1)
        mod
            contains(
                country(E1).det(none)
                    mod in(E1, E2)
                city(E2).det(>=2)
                    mod pop >= 1M
            )

    AMR representation (Claude)

```

    (q / continent
   :ARG0-of (r / recommend-01   ; interrogative root
      :polarity ?)
   :ARG1-of (h / have-org-role-91
      :ARG2 (c / country
         :ARG1-of (h2 / have-org-role-91
            :ARG2 (c2 / city
               :quant-of (e / exceed-01
                  :ARG1 (p / population
                     :poss c2)
                  :ARG2 (v / value
                     :quant 1000000)))
            :quant (a / at-most
               :op1 2)
            :polarity -)   ; "no country"
         :quant (n / no)))))

```

## 2026-05-04

Started Chat-80 again.

Sentences must also yield Atoms, not a list of atoms.

## 2026-04-30

    oxides are not white

This is presented as a rule, but the knowledge base already has a fact that denies it ("magnesium oxide is a white metallic oxide"), so the result must be `"false"`.

Denying something that is told it pretty cool. Let's find out if I can implement it.

## 2026-04-29

I added executable code to the Atom, in order to infer from the name "ferrous sulfide" that it is a sulfide (and store that fact in the database).

## 2026-04-27

`and_3v`, as `or_3v`, should use arguments, not modifiers, because it should always produce a result (`"true"` or `"false"`). If the modifiers are executed separately, and fail, the `and_3v` is not executed.

## 2026-04-25

    salt is a compound (id = 16)

    compound(16)

    salt is sodium chloride (id = 20)

    same_as(16, 20)

    sodium chloride is a compound (id = 20)

    compound(20)

## 2026-04-23

magnesium oxide is a white metallic oxide

This sentence is encoded as a nested `and_3v`. This is fine for querying. For storing information it is necessary to loose the `and_3v`'s. I thought about and I think it's best to create a `create_records_3v`, which binds the truth values to `true`, and discards the `and_3v`'s.

## 2026-04-22

Some modifications. `during` allows for two possibilities. Either pass in the atoms as an argument or as a modifier. This causes confusion to the developer. It also requires the operation to read from the modifiers in the operation. And both would be done only in rare exceptions. This is undesirable.

New idea:

- a rule still produces a single atom. In some cases this is an annoying restriction, but overall this brings peace and quiet to the modelling phase
- modifiers are still added as `pre`, `post`, or `any`
- modifiers that are used **during** the atom's execution must be added as an argument

For OR this means

    Atom('or', [np1], [np2])
    Atom('or_3v', [np1], [np2], T1, T2, T3)

AND can stay the same

    Atom('and').pre(np1, np2)
    Atom('and_3v', T1, T2, T3).pre(np1, np2)

Also I want to give the determiner a special place.

===

It's also possible to detemine the modifier type in the relation.

## 2026-04-21

New ideas. It occurred to me that OR is a very special operation, in that its modifiers should not be executed before or after it, but during it, because the second operand should only be executed if the first fails. While most orher operations can be serialized (the modifiers before or after the operation), this doesn't hold for OR. This is also a very important restriction for a query optimizer. This can and must be generalized. Make explicit how the modifiers of an atom are executed:

- before the operation (i.e. AND)
- after the operation (i.e. dependent subclauses)
- during the operation (i.e. OR)
- don't care / either before or after (best for query optimization)

Another thing that OR brings in is that we can't just throw all modifiers on a heap, we need to know which modifier belongs to which argument. So `.mod()` is out. While each rule can decide which modifiers to pass to its atom, each rule must produce one and just one atom. Not a list, not modify an atom, produce an atom, or inherit it unmodified. That also means that nodes that just want to modify an atom, must create a new atom, like this:

    nbar(E1) -> nbar(E1) 'that' vp(E1)
    lambda nbar, vp: Atom('nop').any([nbar, vp])

`nop` is no-operation

Nodes that want to produce multiple atoms, must create a single atom, that calls the other atoms as a rule.

If atoms are part of the main operation, they may be passed as a list, for example `Atom("intent_tell", [proper_noun, np], T1)`. It's unambiguous that the arguments are executed _during_ of the operation.

The determiner is a special case. It's removed during query preparation, and can be marked as `skip`.

## 2026-04-20

I'm redoing Cooper. It had 2 grammars, one for reading and one for writing. I now want to come up with a single grammar. It means rethinking the structures. And the result should be easy to understand. Not an easy task.

## 2026-04-17

It's relatively easy to generate a name resolver that creates an id for a name in a generic `entity` table (id, name). But common databases don't usually work like that. So for "Cooper" I'm hesitating between the simpler entity table and the one-name-per-table variant. An added difficulty is that the id's produced must be unique in the other tables they're used in. Something that's not usually a problem in a relational database.

    Magnesium is a metal that burns rapidly

    name(E1, 'magnesium')
    metal(E1)
        burns_rapidly(E1)

    "sem": lambda proper_noun: Atom("name", E1, proper_noun),

    `name` will be a special predicate that will be used by `resolve_names` to produce ids, before executing the rest

## 2026-04-14

If I want to keep the hierarchical representation of sentences in, I could keep the spirit of AMR, but change the implementation to match my needs.

    Atom('bring', S1, A, B).mod([Atom('quick', M1, S1)])

By adding modifiers. I can add modifiers for noun modifying sentences, adjectives, adverbs, and non-standard verb-arguments.

## 2026-04-13

I simplified the atom to a point that it isn't pure AMR any more, and I think I'm still not satisfied.

    def isa_declaration(proper_noun: str, a, np: Atom):
        return Atom(
            "intent_tell",
            Atom(np.predicate, AUTO, proper_noun, "true", np.named_arguments),
        )

It's the `np.named_arguments` part here, that just won't fit. It creates a big new problem that I didn't have before.

There's also something else about the named arguments: why are they treated as special? They could just be other atoms. In order to be useful, they will need to be turned into atoms ...

It gave me a good idea of creating name atoms (like `('<unknown-predicate>', E1, 'name')). In a special function, these atoms can be traced, resolved, and all occurrences of E1 in the sentence replaced with the id.

What about the hierarchical structure? You can also have a hierarchical structure in the old representation. Just use more hierarchy. So instead of `(S1, want, A, S2) (S2, bring, B, C)` use `(S1, want, A, (S2, bring, B, C))`. The structure can be flattened if necessary.

AMR is out.

## 2026-04-11

In AMR, the id-argument is separated from the other arguments, and that's fine and recognisable, but when combining it with atoms / records without the special id argument, it is problematic in more and more ways.

for example I now want to add a special constant to indicate that the id of a record must be auto generated:

    A(AUTO / metal
        :0 'magnesium'
        :1 'true')

Is AUTO a variable? No, it's a constant. But the first argument should be a variable, or the predicate. And it's neither.

A good reason for separating the id variable from the rest is for recognizability. But here we have no need for it.

## 2026-04-01

The function `quantify` should also do other things to prepare the query. So, "querify"? Also, it may be interesting to just say `solve` and have `solve` do the transformations itself.

## 2026-03-31

"Every parent has 2 children" is now

    (have, ($1, parent, determiner='all'), ($2, child, determiner=2))

I can write a function that transforms this AMR into the previous version that has a quantification tree. I won't have any need for the leaf atoms any more at that point.

    (all, $1, parent, (
        number, $2, child, 2, {
            have($1, $2)
        }
    ))

This function is called **quantifier scoping** in CLE, and brings the added benefit that the scoping can now be dynamic, which it wasn't before.

Should it also be possible to solve an unquantified structure? No not necessarily, or we would have to add the constraint that the structure not contain any quantifiers.

The amr (semantic tree) is used for

- statements: can store the amr directly
- questions: turn the amr into a query
- commands: can execute the amr directly, while the arguments of the command are turned into queries

It's good to go into commands for a moment

- Pick up a big red block
  - pick_up(A) -> quantify(A, B), pick_up_real(B)
- Will you please stack up both of the red blocks and either a green cube or a pyramid?
  - stack_up(A) -> quantify(A, B), stack_up_real(B)

And statements

- The blue pyramid is mine; Do I own the blue pyramid?
- I own blocks which are not red, but I don't own anything which supports a pyramid
- Do I own anything in the box?

If I can only solve quantified atoms, it's good so distinguish between Atom's and QAtoms, or mark the root atom as "quantified".

Maybe it's necessary to turn the statements into other structures as well, before storing them in the database, in a way that is suitable for querying.

The determiner must be an atom

    (d / greater-than
        :ARG0 2
    )

(d / all)

## 2026-02-30

I had some trouble understanding the difference between the atom variable and the arguments. But now I get it.

For

    r / river

the atom is

    river(R)

and for

    s / likes
        :ARG0 mary
        :ARG1 john

the atom is

    likes(s, mary john)

Note that the main variable is always present in the atom (used to retrieve data and execute code).

What if the "neo-Davidsonion" variable isn't wanted (because the application just deals with the present, or parts of are just not time-dependent)? I want to make that variable optional. So let's say that when I say

    _ / likes
        :ARG0 mary
        :ARG1 john

the atom becomes

    likes(mary, john)

Yesterday I was writing

    Atom(_, A, B)

a lot, and I want to change that into

    Atom(_, A, B)

making the argument structure of Atom even more dynamic.

===

Reified variables?

this seems to be their only valid application

    { "syn": "main_noun(E1) -> 'oxide'", "sem": lambda: 'oxide', "dialog": [("oxide", e1, 'true')] },
    { "syn": "main_noun(E1) -> 'chloride'", "sem": lambda: 'chloride', "dialog": [("chloride", e1, 'true')] },
    { "syn": "main_noun(E1) -> 'sulfide'", "sem": lambda: 'sulfide', "dialog": [("sulfide", e1, 'true')] },

In Richard, this was implemented as adding a record to the database, at execute time.

In Vrel, I could modify the semantics of the sentence itself, as this semantics will be written to the dialog db.

    sodium chloride is an element

i / instance-of
:ARG0 t / thing
:name sodium chlode
:type chloride
:ARG1 e / element

## 2026-02-29

You can't just query `Atom(E1, "river")` because `E1` is not an argument, but it's a dialog constant. Note that's it's called a variable in the AMR documentation. (1)

So to query the database the atom needs to be transformed, into `Atom(C1, "river", E1)`

1. https://github.com/amrisi/amr-guidelines/blob/master/amr.md

## 2026-02-28

Started new project `vrel` because I'm changing some really major things, and it's easier to copy-and-modify to a new project than to change to other project.

- major syntax rules changes based on AMR
- the atom itself will change
- relation will change
- names will always be part of entities with types
- create a global variable generator
- dialog variables should look different from dialog constants

```

```
