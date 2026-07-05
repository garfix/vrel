from vrel.core.constants import CATEGORY_FORMAT, CATEGORY_LITERAL, CATEGORY_VALUE, POS_TYPE_WORD_FORM
from vrel.core.functions.terms import bind_variables
from vrel.entity.GrammarRule import GrammarRule
from vrel.entity.Grammar import Grammar
from vrel.entity.SimpleGrammar import SimpleGrammar
from vrel.interface import SomeModel
from vrel.interface.SomeGenerator import SomeGenerator
from vrel.interface.SomeSolver import SomeSolver
from vrel.module.BasicOutputBuffer import BasicOutputBuffer
from vrel.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser


class BasicGenerator(SomeGenerator):

    grammar: Grammar
    solver: SomeSolver
    output_buffer: BasicOutputBuffer

    def __init__(self, model: SomeModel, output_buffer: BasicOutputBuffer):

        from vrel.core.Solver import Solver

        self.grammar = Grammar([])
        self.solver = Solver(model, None, None)
        self.output_buffer = output_buffer

    def add_grammar_rules(self, rules: SimpleGrammar):
        SimpleGrammarRulesParser().parse_write_grammar(rules, self.grammar)

    def generate_output(self):
        output = self.generate_node([], "s", [], False)
        self.output_buffer.clear()
        return output

    def generate_node(
        self, used_rules: list[int], antecedent_cat: str, antecedent_arguments: list[any], optional: bool
    ) -> list[str]:

        rule, binding, found = self.find_rule(used_rules, antecedent_cat, antecedent_arguments)

        if found:

            hash = rule.hash
            used_rules.append(hash)

            if rule.list_element == None:
                result = self.rewrite(rule, used_rules, binding)
            else:
                result = []
                elements = binding[rule.list_element.name]
                for element in elements:
                    element_binding = binding | {rule.list_element.name: element}
                    result.append(self.rewrite(rule, used_rules, element_binding))

                if rule.list_combine:
                    result = rule.list_combine(result)

            return result

        else:
            if not optional:
                raise Exception(f"No rule found for {antecedent_cat}: {antecedent_arguments}")

    def rewrite(self, rule: GrammarRule, used_rules: list[int], binding: dict):
        consequent_results = []
        for i, consequent in enumerate(rule.consequents):
            consequent_vals = self.get_consequent_values(rule, i, binding)
            consequent_result = self.generate_single_consequent(
                rule,
                used_rules,
                consequent.predicate,
                consequent_vals,
                rule.consequents[i].position_type,
                consequent.optional,
            )
            consequent_results.append(consequent_result)

            # todo?
            # if consequentValue.IsId() && !consequentValue.Equals(antecedentValue) {
            #     generator.state.MarkGenerated(consequentValue)

        # combine consequent results into a string (or other type)
        if rule.combine:
            # custom combination of consequents: a function that takes all consequent results as arguments
            combined = rule.combine(*consequent_results)
        else:
            # default combination of consequents: convert to string and concatenate, filter out results that return None
            real_results = filter(lambda r: r is not None, consequent_results)
            strings = map(lambda r: str(r), real_results)
            combined = "".join(strings)

        # extra string processing
        post_processed = combined
        if rule.post:
            post_processed = rule.post(combined)

        return post_processed

    def get_consequent_values(self, rule: GrammarRule, i: int, binding: dict) -> any:
        consequent_values = []

        consequent = rule.consequents[i]
        for a in range(len(consequent.arguments)):
            if consequent.position_type == POS_TYPE_WORD_FORM:
                consequent_value = ""
            else:
                consequent_variable = consequent.arguments[a]
                if consequent_variable in binding:
                    consequent_value = binding[consequent_variable]
                else:
                    consequent_value = ""

            consequent_values.append(consequent_value)

        return consequent_values

    def find_rule(self, used_rules: list, antecedent_cat: str, antecedent_arguments: list[any]):

        found = False
        result_rule = None
        binding = {}

        rules = self.grammar.find_rules(antecedent_cat, len(antecedent_arguments))

        for rule in rules:

            # example rule:
            # syn: s(E1) -> np(E2) vp(E1)
            # if: [('output_type', 'declarative'), ('output_subject', E1, E2)]

            # rule_antecedent_variable = rule.antecedent.arguments[0]
            binding = {}
            for rule_antecedent_variable, antecedent_value in zip(rule.antecedent.arguments, antecedent_arguments):
                binding[rule_antecedent_variable] = antecedent_value

            # start the binding with the antecedent variable (in the example: E1)
            # if antecedent_values is not None:
            #     binding[rule_antecedent_variable] = antecedent_values

            if not rule.sem:
                # no condition
                result_rule = rule
                found = True

            else:

                # match the condition
                # will bind the E2 in the example ([('output_type', 'declarative'), ('output_subject', E1, E2)])
                match_bindings = self.solver.solve(bind_variables(rule.sem, binding))

                if len(match_bindings) > 0:
                    binding = binding | match_bindings[0]
                    result_rule = rule
                    found = True

            if found:
                # make sure the same rule is not executed again and again
                if rule.hash not in used_rules:
                    break

        return result_rule, binding, found

    def generate_single_consequent(
        self,
        rule: GrammarRule,
        used_rules: list[str],
        category: str,
        arguments: list[any],
        position_type: str,
        optional: bool,
    ) -> list[str]:

        if position_type == POS_TYPE_WORD_FORM:
            result = category
        elif category == CATEGORY_VALUE:
            result = arguments[0]
        elif category == CATEGORY_LITERAL:
            result = arguments[0]
        elif category == CATEGORY_FORMAT:
            result = rule.format(*arguments)
        else:
            result = self.generate_node(used_rules, category, arguments, optional)

        return result
