from vrel.core.Solver import Solver
from vrel.entity.Atom import Atom
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.InductionRule import InductionRule
from vrel.entity.InferenceRule import InferenceRule
from vrel.module.induction.ExplanationNode import ExplanationNode
from vrel.module.transform.query import make_query


def explain(
    question: list[Atom],
    induction_rules: list[InductionRule],
    deduction_rules: list[InferenceRule],
    context: ExecutionContext,
    nodes: list[ExplanationNode],
    known_links: list,
    induction_model,
):
    query = make_query(question)

    for event in nodes:

        atom = event.get_atom()

        event1 = make_query(atom)

        # todo should not be fixed
        module = induction_model.modules[2]
        module.clear()

        for atom1 in event1:
            module.add_atom(atom1)

        solver = Solver(induction_model)

        result = solver.solve(query)

        if len(result) > 0:
            return event

    return None
