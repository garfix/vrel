By Claud Sonnet 4.6 ("At which moments, and how, should I update the salience scores?")

Salience updating is really about when discourse state changes — and the answer depends on whether you're generating sentence-by-sentence or have the whole text plan upfront. Here's a detailed breakdown:

## The Core Update Cycle

The general pattern is: update after each sentence/utterance is finalized, not incrementally within a sentence. This matters because all entities mentioned in the same sentence should be ranked relative to each other using that sentence's own grammatical structure, before you move to the next one.

    for each sentence S in the generation plan:
        1. Decide referring expressions for entities in S using CURRENT salience scores
        2. Finalize S
        3. UPDATE salience scores based on how entities appeared in S
        4. DECAY scores for entities not mentioned in S

## What Triggers an Update

1. After every sentence boundary (always) This is the primary trigger. Centering Theory operates per-utterance, and most practical systems follow this granularity.
2. Within a sentence, at clause boundaries (optional, finer-grained) If your sentences are long or have multiple clauses with different subjects, some systems update at the clause level instead of waiting for the full sentence. This matters more for languages/genres with complex subordination.
3. At paragraph or topic boundaries (extra decay)

When you detect a topic shift (new paragraph, discourse marker like "Meanwhile," "On the other hand"), apply a stronger decay or reset — salience from the previous topic shouldn't bleed into pronoun choice for the new one.

## How to Update: The Mechanics

**Step A — Grammatical role boost**

After finalizing a sentence, score each mentioned entity by the role it played:

    subject:             +3 (or set to max)
    direct object:       +2
    indirect object:     +1.5
    oblique/PP object:   +1
    possessive/genitive: +0.5

This mirrors the Cf-ranking in Centering Theory — subjects are far more likely antecedents than obliques.

**Step B — Recency boost**

Independent of role, simply being mentioned at all should refresh the entity's "last mentioned at sentence N" timestamp. This is used for decay calculations (Step C), not for the score itself.

**Step C — Decay for unmentioned entities**

Every entity not mentioned in the current sentence should have its score reduced:

    score(E) = score(E) * decay_factor   // e.g., decay_factor = 0.5–0.7

A common simplification: decay scores even for entities that were mentioned, then add the boost on top — this way an entity that was salient long ago but is absent for several sentences in a row drops out gradually rather than all-or-nothing.

    score(E) = score(E) * decay_factor + role_boost(E, current_sentence)

If role_boost is 0 (not mentioned), the entity just decays.

**Step D — Cb continuity check (Centering-specific)**

If you're following Centering Theory more strictly, also track whether the Backward-looking Center (Cb) of sentence N equals the Cb of sentence N–1:

- If yes → this is a CONTINUE transition → that entity's salience should stay high or even get an extra boost (the discourse is "staying on topic")
- If no but the new Cb was ranked highly before → RETAIN → moderate salience
- If the Cb shifts to a previously low-ranked entity → SHIFT → that's a cue this entity needed a fuller NP (name), not a pronoun, precisely because the transition is disruptive

This transition type is itself diagnostic: SHIFT transitions are exactly where pronoun ambiguity risk is highest, so some systems use it as a trigger to force a fuller referring expression regardless of raw score.

## Special Triggers Beyond Routine Decay

**Entity re-introduction after absence**

If an entity drops below threshold and is later needed again, don't just "revive" its old score — treat it like a fresh mention requiring a name/description first, then let normal salience accumulation restart from there.

**Contrastive/parallel structure**

If you detect a contrast construction ("X did A, but Y did B"), bump the salience of both entities involved equally, since both need to remain distinguishable as the contrast continues — this is also a case where you might suppress pronouns even at high salience, because the rhetorical structure demands explicit naming.

**Quoted speech / reported dialogue**

When entering or exiting a quotation, salience tracking sometimes needs a soft reset, since the speaker becomes hyper-salient inside the quote regardless of prior discourse score.

## Practical Pseudocode

    def update_salience(entities_in_sentence, salience_scores, decay=0.6):
        role_boosts = {
            'subject': 3.0, 'object': 2.0, 'iobj': 1.5,
            'oblique': 1.0, 'possessive': 0.5
        }

        mentioned = {e['entity'] for e in entities_in_sentence}

        # Decay everyone first
        for entity in salience_scores:
            salience_scores[entity] *= decay

        # Then boost mentioned entities
        for mention in entities_in_sentence:
            e = mention['entity']
            boost = role_boosts.get(mention['role'], 0.5)
            salience_scores[e] = salience_scores.get(e, 0) + boost

        return salience_scores

## Key Takeaway

Update once per sentence (or clause, for finer control), always via decay-then-boost, using grammatical role as the boost signal, and treat Cb shifts and topic boundaries as special cases that override the raw numeric score when choosing between pronoun vs. fuller reference.
