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
