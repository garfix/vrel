from vrel.core.Solver import Solver
from vrel.entity.Atom import Atom
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.InductionRule import InductionRule
from vrel.entity.InferenceRule import InferenceRule
from vrel.module.induction.ExplanationNode import ExplanationNode
from vrel.module.transform.query import make_query


def explain(
    question: list[Atom], nodes: list[ExplanationNode], induction_model, context: ExecutionContext, dialog: list[Atom]
):
    query = make_query(question)

    context.logger.add_value("explain", query)

    # todo should not be fixed
    module = induction_model.modules[2]

    for event in nodes:

        atom = event.get_atom()

        event1 = make_query(atom)

        # module.clear()

        # context.logger.add_value("dia", dialog)
        # context.logger.add_value("event1", event1)

        # for atom1 in dialog:
        #     module.add_atom(atom1)

        # for atom1 in event1:
        #     module.add_atom(atom1)
        # populate(module, event1)

        solver = Solver(induction_model)

        # query1 = query
        # result = solver.solve(query1)
        failed = False
        bindings = [{}]
        for i, a in enumerate(query):
            context.logger.add_value(i, a)
            new_bindings = []
            for binding in bindings:
                # todo: this is just absurdly inefficient
                populate(module, event1)
                b = solver.solve_single(a, binding)
                # the top-level predicate should always succeed
                if len(b) == 0 and i == 0:
                    failed = True
                # if the event yields no results, try the dialog
                if len(b) == 0:
                    # todo: this is just absurdly inefficient
                    populate(module, dialog)
                    b = solver.solve_single(a, binding)
                    # context.logger.add_value("dialog", dialog)
                    # context.logger.add_value("binding", binding)
                    # context.logger.add_value("a", a)
                    # context.logger.add_value("b", b)
                    #
                    # farmer(`entity:DLG4`) would match farmer($20), but for the binding ($20 = `entity:DLG10`)
                    #
                # accumulate bindings
                new_bindings.extend(b)
            bindings = new_bindings
            # no matches? stop
            if len(bindings) == 0:
                break

        if failed:
            result = []
        else:
            result = bindings

        # if event1[0].predicate == query[0].predicate:
        #     context.logger.add_value("event", event1)
        #     context.logger.add_value("result", result)

        if len(result) > 0:
            return event

    return None


def populate(module, atoms):
    module.clear()
    for atom1 in atoms:
        module.add_atom(atom1)
