Variables and id constants live in several scopes.

## Rule scope

The variables `E1`, `E2`, etc have rule-scope. They're only used to equate (same as) different things within a rule.

## Sentence scope

The variables `$1`, `$2`, etc have sentence scope. They're created by the composer and serve to equate different parts of the sentence, produced by different rules.

## Deduction variables

The deduction module produces variables `IM1`, `IM2`, ... while executing a rule. Their scope is the rule that is currently processed.

## Dialog constants

The constants `DLG1`, `DLG2`, etc have dialog scope. They're not automatically created. The function `reify` turns the variables in an atom-list into dialog constants. The result can be stored in a dialog-based store.
