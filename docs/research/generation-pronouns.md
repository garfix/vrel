By Claud Sonnet 4.6

Use a pronoun when:

- The entity is the current discourse topic — i.e., it was mentioned recently and is "in focus"
- There's no ambiguity about which entity the pronoun refers to (no other salient entity with the same gender/number)
- The pronoun is in the same sentence or immediately adjacent clause/sentence to its antecedent
- The entity has been continuously active in the discourse (not mentioned, then dropped, then re-raised)

Avoid a pronoun when:

- Two or more entities share the same pronoun form (two women → "she" is ambiguous)
- The entity was last mentioned several sentences ago (salience has decayed)
- You're re-introducing an entity after a topic shift
- The entity is being contrasted with another ("Alice stayed, but Bob left" — stressing Bob by name)

## Salience Modeling

The standard formal model is Centering Theory (Grosz, Joshi & Weinstein 1995). It ranks entities in each utterance by grammatical role:

    Subject > Object > Indirect Object > Oblique > Possessive > Other

The highest-ranked forward-looking center (Cf) that persists into the next utterance is the backward-looking center (Cb) — the entity most "in focus." That entity is the best candidate for pronominalization. Entities lower in the ranking get fuller descriptions.

A practical simplification:

- Maintain a salience score for each entity, initialized on first mention
- Boost the score when the entity is: the subject (+3), object (+2), mentioned at all (+1)
- Decay all scores slightly at each sentence boundary
- If an entity's score is above a threshold and it's unambiguous, use a pronoun

Choosing Which Pronoun
Once you've decided to pronominalize, select based on the entity's features:

| Feature                            | Pronoun         |
| ---------------------------------- | --------------- |
| Human, singular, masc.             | he/him/his      |
| Human, singular, fem.              | she/her/hers    |
| Human, singular, unknown/nonbinary | they/them/their |
| Human, plural                      | they/them/their |
| Non-human, singular                | it/its          |
| Non-human, plural                  | they/them/their |

You'll need gender/animacy attributes on each entity in your semantic structure. For real-world named entities (people), this may require a lookup or inference step.

## Handling Ambiguity

Before committing to a pronoun, run an ambiguity check:

    for each candidate pronoun P for entity E:
        competitors = {X in salience_list : X ≠ E and pronoun(X) == P and salience(X) > threshold}
        if competitors is empty → pronoun is safe
        else → fall back to a name or description

This is essentially simulating what a reader would do: resolve the pronoun to the most salient matching entity, and check if that's actually the intended one.

## Practical Architecture

    For each entity mention in the output sentence:
    1. Is this the first mention? → Use name/description
    2. Compute salience score from discourse history
    3. Is salience above threshold?
        No → Use name
        Yes → Compute candidate pronoun from entity features
    4. Ambiguity check: does any other salient entity map to the same pronoun?
        Yes → Use name or definite description
        No → Use pronoun
    5. Update salience scores after sentence is finalized

## Useful References

- Centering Theory: Grosz, Joshi & Weinstein (1995) — the theoretical foundation
- Dale & Reiter (1995) — incremental algorithm for referring expression generation
- Kibble & Power (2004) — operationalizing centering for NLG
- For neural approaches: REG has been revisited with LLMs, but rule-based salience tracking is still often more controllable in structured generation pipelines

The trickiest cases are always cataphora (pronoun before antecedent), bridging references, and entities with unknown or non-binary gender — those typically need special-case handling on top of the general framework.
