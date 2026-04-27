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
