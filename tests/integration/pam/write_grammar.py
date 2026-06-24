from vrel.core.constants import E1, E2, UNIFICATION
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

Explanation = Variable("Explanation")
Goal = Variable("Goal")


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'OK'",
            "if": [Atom("output_type", "understood")],
        },
        {
            "syn": "s() -> 'Because' reason(Explanation)",
            "if": [Atom("output_type", "explanation"), Atom("output_explanation", Explanation)],
        },
        {
            "syn": "reason(Explanation) -> goal(Goal)",
            "if": [Atom(UNIFICATION, Explanation, Atom("goal", Goal))],
        },
        {
            "syn": "goal(Goal) -> desc(E1) 'wanted' 'to' 'be' 'not' 'hungry'+'.'",
            "if": [Atom(UNIFICATION, Goal, [Atom("not", [Atom("hungry", E1)])])],
        },
        {
            "syn": "desc(E1) -> 'she'",
            "if": [
                Atom(
                    "unambiguous_pronoun",
                    E1,
                    [Atom("feature", E1, "type", "person"), Atom("feature", E1, "gender", "female")],
                )
            ],
        },
        {
            "syn": "desc(E1) -> 'they'",
        },
    ]
