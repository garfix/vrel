from vrel.core.Solver import Solver
from vrel.core.functions.terms import bind_variables
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.InferenceRule import InferenceRule
from vrel.interface.SomeModel import SomeModel


def match(
    pattern,
    current_subject,
    binding: dict,
    deduction_rules: list[InferenceRule],
    context: ExecutionContext,
    sentence,
    induction_model: SomeModel,
):
    module = induction_model.modules[1]
    module.clear()

    for atom in current_subject:
        module.add_atom(atom)

    solver = Solver(induction_model)

    bound = bind_variables(pattern, binding)

    results = solver.solve(bound)

    return results[0] if len(results) > 0 else None
