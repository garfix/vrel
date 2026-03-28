from vrel.core.Model import Model
from vrel.core.Solver import Solver
from vrel.core.functions.terms import bind_variables
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.InferenceRule import InferenceRule
from vrel.module.PlainReadWriteModule import PlainReadWriteModule
from vrel.module.InferenceModule import InferenceModule


def match(pattern, current_subject, binding: dict, deduction_rules: list[InferenceRule], context: ExecutionContext, sentence):
    model = Model([
        # PlainReadWriteModule(sentence),
        PlainReadWriteModule(current_subject),
        InferenceModule(deduction_rules)
    ])
    # print()
    # print('sentence', sentence)
    # print('current_subject', current_subject)
    solver = Solver(model)

    bound = bind_variables(pattern, binding)

    results = solver.solve(bound)
    # results = context.solver.solve(pattern)

    return results[0] if len(results) > 0 else None
