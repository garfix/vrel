from vrel.core.functions.terms import bind_variables
from vrel.core.functions.unification import unification
from vrel.core.functions.variables import generate_variables
from vrel.entity.Atom import Atom
from vrel.entity.Relation import Relation
from vrel.entity.Variable import Variable
from vrel.interface import SomeSolver
from vrel.interface.SomeModule import SomeModule
from vrel.dsl.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.InferenceRule import InferenceRule
from vrel.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


class DeductionModule(SomeModule):
    """
    This module handles very basic Prolog-like facts and inferences.
    """

    rules: dict[str, list[InferenceRule]]
    variable_generator: VariableGenerator

    def __init__(self, rules: list = []) -> None:
        super().__init__()
        self.add_relation(Relation("learn_rule", query_function=self.learn_rule))
        self.variable_generator = VariableGenerator("IM")
        self.rules = {}
        for rule in rules:
            self.insert_rule(rule)

    def insert_rule(self, rule: InferenceRule):
        predicate = rule.head.predicate
        self.add_relation(Relation(predicate, query_function=self.handle_rule))
        if not predicate in self.rules:
            self.rules[predicate] = []
        self.rules[predicate].append(rule)

    def import_rules(self, path: str):
        parser = SimpleInferenceRuleParser()
        with open(path) as rule_file:
            content = rule_file.read()
            rules, pos = parser.parse_rules(content)
            if pos is not None:
                raise Exception(
                    "Unable to parse inference on token "
                    + str(pos)
                    + " in file "
                    + path
                )
            for rule in rules:
                self.insert_rule(rule)

    def handle_rule(self, arguments: list, context: ExecutionContext) -> list[list]:
        results = []
        for rule in self.rules[context.relation.predicate]:
            results.extend(self.solve_rule(rule, arguments, context.solver, {}))

        return results

    def solve_rule(
        self, rule: InferenceRule, arguments: list, solver: SomeSolver, binding: dict
    ):

        # replace variables in rule with new variables
        variable_map = {}
        head = generate_variables(
            rule.head.positional_arguments, self.variable_generator, variable_map
        )
        body = [
            generate_variables(atom, self.variable_generator, variable_map)
            for atom in rule.body
        ]

        rule_binding = unification(head, arguments, binding)
        if rule_binding is None:
            return []

        if len(rule.body) == 0:
            bindings = [rule_binding]
        else:
            bindings = solver.solve(bind_variables(body, rule_binding))

        print("body", body)
        print("head", head)
        print("binding", binding)
        print("arguments", arguments)
        print("rule_binding", rule_binding)
        print("bound", bind_variables(body, rule_binding))
        print("result", bindings)
        print()

        results = [
            bind_variables(bind_variables(head, rule_binding), binding)
            for binding in bindings
        ]

        return results

    # ('learn_rule', head, [body-atoms])
    def learn_rule(self, arguments: list, context: ExecutionContext) -> list[list]:
        head, body = arguments

        if not isinstance(head, Atom):
            raise Exception("The head of a rule must be a single atom: " + str(head))

        self.insert_rule(InferenceRule(head, body))

        return [[None, None]]
