from vrel.core.constants import E1, E2, E3, UNIFICATION
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

Explanation = Variable("Explanation")
Consequence = Variable("Consequence")
Goal = Variable("Goal")
Action = Variable("Action")
Event = Variable("Event")
Name = Variable("Name")


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'OK'",
            "if": [Atom("last_output", "understood")],
        },
        {
            "syn": "s() -> 'Because' reason(Explanation)",
            "if": [Atom("last_output", "explanation", Explanation)],
        },
        {
            "syn": "s() -> 'This enabled' action(Consequence)",
            "if": [Atom("last_output", "consequences", Consequence)],
        },
        {
            "syn": "reason(Explanation) -> goal(Goal)",
            "if": [Atom(UNIFICATION, Explanation, Atom("goal", Goal))],
        },
        # {
        #     "syn": "goal(Goal) -> desc(E1) 'wanted' 'to' 'be' 'not' 'hungry'+'.'",
        #     "if": [Atom(UNIFICATION, Goal, [Atom("not", [Atom("hungry", E1)])])],
        # },
        {
            "syn": "goal(Goal) -> desc(E1) 'wanted' 'to' 'know' 'the' 'distance' 'to' 'a' 'restaurant'+'.'",
            "if": [
                Atom(
                    UNIFICATION,
                    Goal,
                    [Atom("know", E1, [Atom("fact", [Atom("distance", "restaurant")])])],
                )
            ],
        },
        {
            "syn": "goal(Goal) -> desc(E1) 'wanted' 'to' 'know' 'where' desc(E1) 'was'+'.'",
            "if": [
                Atom(
                    UNIFICATION,
                    Goal,
                    [Atom("know", Event, E1, [Atom("location", E2)])],
                )
            ],
        },
        {
            "syn": "goal(Goal) -> desc(E1) 'wanted' 'to' 'get' 'someplace'+'.'",
            "if": [
                Atom(
                    UNIFICATION,
                    Goal,
                    [Atom("be_at", Event, E1, E2)],
                )
            ],
        },
        {
            "syn": "action(Action) -> desc_object(E1) 'to' 'ask' desc_object(E2)",
            "if": [
                Atom(
                    UNIFICATION,
                    Action,
                    Atom("ask", Event, E1, E2, E3),
                )
            ],
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
            "syn": "desc(E1) -> 'he'",
            "if": [
                Atom(
                    "unambiguous_pronoun",
                    E1,
                    [Atom("feature", E1, "type", "person"), Atom("feature", E1, "gender", "male")],
                )
            ],
        },
        {
            "syn": "desc(E1) -> 'they'",
        },
        {
            "syn": "desc_object(E1) -> 'her'",
            "if": [
                Atom(
                    "unambiguous_pronoun",
                    E1,
                    [Atom("feature", E1, "type", "person"), Atom("feature", E1, "gender", "female")],
                )
            ],
        },
        {
            "syn": "desc_object(E1) -> 'him'",
            "if": [
                Atom(
                    "unambiguous_pronoun",
                    E1,
                    [Atom("feature", E1, "type", "person"), Atom("feature", E1, "gender", "male")],
                )
            ],
        },
        {
            "syn": "desc_object(E1) -> literal(Name)",
            "if": [Atom("resolve_name", E1, Name)],
        },
        {
            "syn": "desc_object(E1) -> 'the' 'farmer'",
            "if": [Atom("farmer", E1)],
        },
        {
            "syn": "desc_object(E1) -> 'them'",
        },
    ]
