## todo

match

- Don't match all atoms of the query at once, go through them one by one.
- Accumulate bindings.
- Make sure they're flattened in the right order.
- The first one should match the first one.
- Each of the others should match the sentence; if it doesn't, try the dialog; try inference (for "tell" for example).
- If all fail, skip it and continue.
- At the end, take the event that matches most (but only if this is still necessary; perhaps make this a system option).

predicted

`predicted` tries to match a `current_subject` to the known facts by applying rules

Given a `current_subject` and a rule A => Plan => B, if `current_subject` matches A and `nodes` contains nodes that match Plan => B (let's call them Plan1 and B1), (note: Plan may be empty and only contain a potential predicate) then create a link between `current_subject` and Plan, and fill the unbound variables in Plan1 and B1.

- find a rule R1 whose antecedent matches `current_subject` and produce binding B
- find nodes Plan1 and B1 that match R1's plan and consequent, given binding B
- link `current_subject` to Plan1 and fill in Plan1 and B1

can i work with nodes directly instead of trying to find them everytime?

===

- OK (sort of) question: how does PAM create the dummy plan between two goals?

- OK should be able to introduce a new variable in the RHS
- OK Maak een Node klasse voor plans/goals/themes
- OK implement ... => Plan => ...
- OK make the chain more transparent (add a command?)
- OK add nodes in the try_rules function (but no link)
- OK should the nodes be added already? i didn't even implement check_init_req
- OK add links between nodes
- OK Add the plan to the chain
- OK implement check_init_req
- OK check the nodes of the sentence John.
- OK relate is not presented goals because only plans lead to goals (but not here)
- OK be_near is linked directly to know_loc, while the plan above it should be linked
- OK story actions should be added as actions to plans, not as plans
- OK ask plan should have a link to ask-as-action, but these links are only created when justify is done
- OK can the `known_links` be removed?
- OK link the third sentence
- sommige identifiers voor locations zijn variabelen voor location atoms; dat werkt niet goed
- have the pronouns been resolved completely?
- store both the plans and the plan-ids in the goal (etc), to make reasoning about them easier
- I will need to create a temporary (within sentence) node set and a more permanent (within dialog) node set.
  - or: add_node does not add to nodes list?
- explain: bij het matchen: zowel vraag als explanation omzetten in platte query
- he/him => male (semantics)

later

- node 9 is not needed
- node 4 doesn't say anything about using a vehicle, like in PAM's example
- `DLG11` must be replaced by `where he was` (?) same for all variables: pass them over at inference
- node 2 has action 0 => this follows logically from the implementation. "lost" is not part of the objects in pages 304/305
- 'John is lost' is now a kind of "plan" with a goal (attempt)

SAME AS C2, `entity:PA1`
SAME AS DLG3, `person:John`
SAME AS L1, `entity:PA2`
SAME AS C2, `entity:PA1`
SAME AS DLG9, `person:John`

- change license
- PAM next test
- document all influences on the library
- start on SHRDLU
- study Preform / Inform https://ganelson.github.io/inform/words-module/4-ap.html

- not(last_output(T)) means: no output has been produced yet => elk aantal parameters?
- maak van "if" een parsable string
- the fact induction doesn't work
- research: denk na over onderscheid tabel / Relation / columns; note: borders (id1, id2) en (id2, id1)
- make sure the reified constructs are stored in a dialog-specific store (how? is an open question)
- inject solver in BasicGenerator
- with_context

- neem in de Relation op welke parameter de unieke id bevat
  - check op deze parameter in extract_determiner_arguments (`arguments[0]`)

## Pronouns

update saliency when

- reading an utterance: subject, object iobj
- writing an utterance
- updating saliency should only done for entities in verbs
- also: use the syntactive subject, not the semantic subject

## Breaking out of toy worlds

Create a system that combines multiple systems and proves that it can't just deal with a single toy world.

## PAM

- the `match` in `relate` matches perhaps by accident: I thought I had to bind the consequent, then replace the constants by variables. But omitting both seems to have the same effect. check this
- create links between goals in both the predict and the inference phase

## Same as

- matching van geneste structuren zal nog niet werken omdat same_as niet aan nesting doet

## API

- api: bv tk.keras.layers.Dense

## Context

- A word like "short" has no meaning by itself, only in the context of some other word.
- How to implement contexts? As some sort of a hierarchy?
- How to implement the current context? As a list, the last item of which is the recent context, and the others the fallback-context?
- Should there be enter-context / leave-context conditions? Have other systems done this?

## Customize

- PronounModule must have its data source as a parameter (which defaults to the current data source)

## Resolve name / constant

- Consider if resolve can (or should) be done as function, if so, or not, give a good reason.

## New relation function: command

Just an idea: next to `query_function` and `write_function`, create a `command_function` that allows the predicate to be executed as a command. There would be no need to create a separate predicate (like in nli-go) for commands.

## Plugin

If elegantly possible, create a plugin structure for Solver.

## Documenteer

De eerste argument van een atom moet zijn identifier variable zijn.
De volgorder van de modifiers van een atom doet ertoe als ze determiners hebben.

## Dialog and database

Make a distinction between dialog constants (short term) and database ids (long term)

## booleans

Create constants for true / false.

## remove sentence_categories

Is there an easier way?

## Infinite loop detection

If the executor comes into a loop, stop it, and print the looping commands.

Also, possibly, add an option to just skip and continue from a loop.

## DSL parser

Proper error messages with line numbers.

## Agreement

Create an example to show that agreement can be implemented.

## Relation arguments

Create proper Argument objects for the Relation

## same as

- Same as now assumes that the identifiers are unique in the whole domain, while in practise they're only unique within the relation.
- Find id arguments in stead of arguments named "id"
- Id's are now presumed integers, while stored as text

## dialog or LTM

When we `store` a structure, is that in dialog or LTM? Should that be decidable from the application?

## PAM

- de deducties van PAM moeten een mate van onzekerheid hebben; het zijn geen zekerheden; hoe streep je hypothesen af?

- Is de molecule structuur van zinnen nuttig (essentieel) voor PAM? Probeer hier achter te komen.

## AMR and other structures

- to query an amr, quantify it; the atoms then become "quantified"
- to state a rule, turn it into a structure that can be queried, and store it
- to state a goal, leave the amr as is
- to command an amr, leave the command as is, but quantify the argument(s) and perform the command

## input-only variables

From `results.py`:

    # todo: maybe declare properly
    #
    if isinstance(result_arg, Variable):
        raise Exception(
            f"Result of '{predicate}' contains a variable: {result}"
        )

## context

Work out context in inference rules:

- syntax: `name{ rule. rule. }`
- application: the rules must only be applied when context name is active

## scoped

`scoped` used to result in no new variables. This has changed. Now it does. And the tests still pass. And this has advantages, but maybe also disadvantages. Create a new predicate that explicitly exposes variables? Change the name of `scoped` to `execute`?

## multiple sentences

- the parser should always return multiple sentences, and there should be a better standard way on how to find different sentences

## inference to deduction

Everything called inference should be called deduction, to contrast it with induction.

## database

- use a db like Neo4j to store second order, modal, and time-based sentences

## module

- (?) add `common_query` and `common_write` to SomeModule to reduce code duplication
- $unification of 2 variables (both should be assigned a new anonymous variable. https://www.dai.ed.ac.uk/groups/ssp/bookpages/quickprolog/node12.html)

## isolation of independent parts

optimize isolate independent parts:

- is it possible to place the independent parts directly after the head atom? faster?
- isolate the list arguments of an atom (this is not done yet)
- but: don't use isolate independent parts for predicates like "store"

## MCP

Write an MCP server to make Vrel interact with an LLM.

## done

- remove bindings from ExecutionContext?

* $unification
* replace SimpleResponder by BasicGenerator
* learn_grammar_rule
* directly execute code
* characters as tokens; exit tokenizer
* add ResultIterator
* can parsing be done faster?
* document parse tree sort heuristics
* chat-80 import csv
* optimize in-memory db
* import from csv
* can np's be implemented as atoms without find?
* optimize: reorder atoms
* inference engine
* create numbers based on a token
* create a context and pass it to each module function, in stead of the arguments which are mostly unused
* table select columns to display => intents as atoms?
* add units to scalar answers and floor floating point numbers in tables to integers
* can aggregates by simplified?
* importers based on hand-written grammar in stead of regex
* store type information with the variable in stead of an Instance?
* start using dialog variables in stead of sentence variables; it's hard to change them later
* pass variables to functions or None values?
* more access to in-between results of blocks
* added data sources for Postgres, MySQL, Sqlite3, Sparql
* simplify the responder
