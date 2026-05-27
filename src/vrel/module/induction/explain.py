import copy

from vrel.core.Model import Model
from vrel.core.Solver import Solver
from vrel.core.handlers.SameAsHandler import SameAsHandler
from vrel.entity.Atom import Atom
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.InductionRule import InductionRule
from vrel.entity.InferenceRule import InferenceRule
from vrel.module.DeductionModule import DeductionModule
from vrel.module.PlainReadWriteModule import PlainReadWriteModule
from vrel.module.transform.query import make_query


def explain(
    question: list[Atom],
    induction_rules: list[InductionRule],
    deduction_rules: list[InferenceRule],
    context: ExecutionContext,
    known_events: list[Atom],
    known_links: list,
):
    query = make_query(question)

    context.logger.add_value("query", query)

    for event in known_events:

        if event[0].predicate == "pick_up":

            event1 = make_query(event)

            # model = Model(
            #     [
            #         PlainReadWriteModule(event1),
            #         DeductionModule(deduction_rules),
            #     ],
            #     same_as_handler=context.model.get_same_as_handler(),
            # )

            model = copy.copy(context.model)
            model.modules.append(PlainReadWriteModule(event1))

            solver = Solver(model)

            result = solver.solve(query)

            context.logger.add_value("event", event1)
            context.logger.add_value("result", result)

    return question
