from vrel.core.Solver import Solver
from vrel.entity.Atom import Atom
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.InductionRule import InductionRule
from vrel.entity.InferenceRule import InferenceRule
from vrel.module.transform.query import make_query


def explain(
    question: list[Atom],
    induction_rules: list[InductionRule],
    deduction_rules: list[InferenceRule],
    context: ExecutionContext,
    known_events: list[Atom],
    known_links: list,
    induction_model,
):
    query = make_query(question)

    for event in known_events:

        event1 = make_query(event)

        module = induction_model.modules[1]
        module.clear()

        for atom in event1:
            module.add_atom(atom)

        solver = Solver(induction_model)

        result = solver.solve(query)

        if len(result) > 0:
            return event

    return None
