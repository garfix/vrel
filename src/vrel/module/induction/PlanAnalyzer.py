from vrel.core.functions.id_unification import id_unification
from vrel.core.functions.helper import hash_it
from vrel.core.functions.terms import bind_variables
from vrel.core.functions.variables import generate_constants, variablize
from vrel.entity.Atom import Atom
from vrel.entity.Id import Id
from vrel.entity.InductionRule import InductionRule
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Variable import Variable
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeModule import SomeModule
from vrel.module.induction.ActionNode import ActionNode
from vrel.module.induction.ExplanationNode import ExplanationNode
from vrel.module.induction.GoalNode import GoalNode
from vrel.module.induction.Link import Link
from vrel.module.induction.PlanNode import PlanNode
from vrel.module.induction.explain import explain
from vrel.module.induction.match import match
from vrel.module.transform.query import make_query
from vrel.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


# Based on MicroPAM (see https://github.com/garfix/micropam)
class PlanAnalyzer:

    induction_model: SomeModule
    nodes = list[ExplanationNode]
    known_links = list
    try_check: dict
    generator: int
    variable_generator: VariableGenerator
    dialog: list[Atom]

    def __init__(self, induction_model: SomeModel):
        self.induction_model = induction_model
        self.known_facts = []
        self.try_check = {}
        self.nodes: list[ExplanationNode] = []
        self.generator = 0
        self.variable_generator = VariableGenerator("PA")
        self.dialog = []

    def justify(
        self,
        sentence: list[Atom],
        induction_rules: list[InductionRule],
        context: ExecutionContext,
    ):
        chain: list[Link] = []
        current_subject = sentence

        while True:

            # if current_subject is a known fact, an explanation is found
            if self.predicted(current_subject, induction_rules, context):
                break

            if self.check_init_req(chain):
                break

            chain.append(Link(current_subject, induction_rules[:]))

            current_subject = self.try_inference(chain, context)
            if not current_subject:
                break

        if current_subject:
            self.chain_to_nodes(current_subject, chain, context)
        else:
            self.update_db(sentence, context)

    def chain_to_nodes(self, current_subject: list[Atom], chain: list[Link], context: ExecutionContext):
        for link in reversed(chain):
            self.update_db(link.atoms, context)
        self.update_db(current_subject, context)

    # looks for a goal episode whose source is a theme, or an unknown plan
    def check_init_req(self, chain: list[Link]):

        if len(chain) > 2:
            # source is an unknown plan
            a = chain[len(chain) - 1].atoms[0]
            # empty check
            if a.predicate == "plan" and a.arguments[0] == "variable":
                return True

    def predicted(
        self,
        current_subject: list,
        induction_rules: list[InductionRule],
        context: ExecutionContext,
    ):
        # if Q is known, and there is a rule that induces P => Q, and the current subject is P,
        # then P was predicted and may be added as a known fact

        current_subject_query = make_query(current_subject)

        # consider all known facts (item_list) and all rules (induction_rules)
        for rule in induction_rules:

            # match the antecedent to the current subject
            subject_binding = match(rule.antecedent, current_subject_query, {}, self.induction_model)
            if subject_binding is not None:

                # bind constants, but not id's, because their identity has not yet been established, so they will seem different,
                # even though they may be identical
                sb = dict(filter(lambda kv: not isinstance(kv[1], Id), subject_binding.items()))

                for item in self.known_facts:

                    # match the consequent to the known item
                    item_binding = match(rule.consequent, item, sb, self.induction_model)

                    if item_binding is not None:

                        ib = dict(filter(lambda kv: not isinstance(kv[1], Id), item_binding.items()))

                        # the equality between dialog variables that connect two sentences can now be stored
                        print("==========")
                        # print("rule", rule)
                        # print("current_subject", current_subject)
                        # print("item", item)
                        # print("subject_binding", subject_binding)
                        # self.store_identity(subject_binding, item_binding, context)

                        if rule.plan is not None:
                            if self.predicted_plan(
                                rule.plan, current_subject, subject_binding, item_binding, item, context
                            ):
                                return True
                        else:
                            if self.predicted_no_plan(
                                rule.plan, current_subject, subject_binding, item_binding, item, context
                            ):
                                return True

                            # print("<>")
                            # print("item", item)
                            # print("variablized_consequent", variablized_consequent)
                            # print("bound_consequent", bound_consequent)
                            # print("bound_antecedent", bind_variables(rule.antecedent, subject_binding))
                            # print("item_binding", item_binding)
                            # print("subject_binding", subject_binding)
                            # print("rule", rule)
                            # print("current_subject", current_subject)
                            # self.predicted_no_plan(current_subject, item)

                        # return True

        return False

    def predicted_no_plan(self, rule_plan, bottom, subject_binding, item_binding, top: list[Atom], context):

        top_node = self.find_node(top)
        bottom_node = self.find_node(bottom)

        # plan_node_index = top_node.get_first_attempt()
        # plan_node = self.nodes[plan_node_index]
        # plan = plan_node.get_atom()
        # potential_plan = plan_node.get_potential_plans()[0] if len(plan_node.get_potential_plans()) > 0 else None

        # # fill an empty plan
        # if plan_node.is_empty():
        #     plan_node.set_atom(potential_plan)

        # print("subject_binding", subject_binding)
        # print("item_binding", item_binding)
        # print("bottom_node", bottom_node)
        # print("top_node", top_node)

        self.store_identity(subject_binding, item_binding, context)
        return True

    def predicted_plan(self, rule_plan, bottom, subject_binding, item_binding, top: list[Atom], context):
        top_node = self.find_node(top)
        bottom_node = self.find_node(bottom)
        plan_node_index = top_node.get_first_attempt()
        plan_node = self.nodes[plan_node_index]
        plan = plan_node.get_atom()
        potential_plan = plan_node.get_potential_plans()[0] if len(plan_node.get_potential_plans()) > 0 else None
        sb = dict(filter(lambda kv: not isinstance(kv[1], Id), subject_binding.items()))

        # print("potential_plan", potential_plan)
        # print("rule_plan", rule_plan)

        if plan_node.is_empty():
            plan_binding = match(rule_plan, [potential_plan], sb, self.induction_model)
            if plan_binding is None:
                return False
        else:
            plan_binding = match(rule_plan, [plan], sb, self.induction_model)
            if plan_binding is None:
                return False

        plan_node.add_subepisode(bottom_node.id)

        print("subject_binding", subject_binding)
        print("plan_binding", plan_binding)
        print("item_binding", item_binding)
        print("bottom_node", bottom_node)
        print("plan_node", plan_node)
        print("top_node", top_node)

        self.store_identity(subject_binding, plan_binding, context)
        self.store_identity(plan_binding, item_binding, context)
        self.store_identity(subject_binding, item_binding, context)

        return True

    def store_identity(
        self,
        subject_binding: dict,
        item_binding: dict,
        context: ExecutionContext,
    ):
        print("Store identity")
        for variable in subject_binding:
            if variable in item_binding:
                if isinstance(subject_binding[variable], Id) and isinstance(item_binding[variable], Id):
                    print(f"SAME AS {subject_binding[variable]}, {item_binding[variable]}")
                    context.solver.write_atom(Atom("same_as", subject_binding[variable], item_binding[variable]))

    def try_inference(self, chain: list[Link], context: ExecutionContext):
        # chain is a list of [cd, all_inference_rules]
        # return the lhs of the first match, and extend the chain
        current_subject = None
        while len(chain) > 0:
            last_link = chain.pop()
            # try all inference rules in the cd
            # if the cd matches a rule, add it to the chain
            # and return the bound lhs of the rule
            current_subject = self.try_rules(last_link.atoms, last_link.rules[:], chain, context)
            if current_subject is not None:
                break

        if current_subject:
            return current_subject

        return None

    def try_rules(self, current_subject, rules: list[InductionRule], chain: list[Link], context: ExecutionContext):
        # match cd with the rhs of each of the rules
        # if a match occurs, return a binding with the lhs of the rule
        last_rule = None
        binding = None
        while len(rules) > 0:
            last_rule = rules.pop()
            cs = make_query(current_subject)
            # print("m3")
            binding = match(last_rule.antecedent, cs, {}, self.induction_model)

            # if the combination of antecedent and binding has happened before, skip it
            hash = hash_it([last_rule.antecedent, binding])
            if hash in self.try_check:
                continue
            else:
                self.try_check[hash] = True

            if binding is not None:
                break

        if binding is not None:
            chain.append(Link(current_subject, rules))

            c1 = bind_variables(last_rule.consequent, binding)

            variable_map = {}
            c2 = generate_constants(c1, self.variable_generator, variable_map)

            # print("last_rule.antecedent", last_rule.antecedent)
            # print("cs", cs)
            # print("binding", binding)
            # print("c1", c1)
            # print("c2", c2)

            node1 = self.add_node(current_subject, context)
            node2 = self.add_node(c2, context)

            if last_rule.plan:
                self.generator += 1
                atoms = [Atom("plan", "variable", self.generator)]
                plan_node = self.add_node(atoms, context)
                map = {}
                genny = self.variable_generator
                potential_plan = generate_constants(bind_variables(last_rule.plan[0], binding), genny, map)
                plan_node.add_potential_plan(potential_plan)
                chain.append(Link(atoms, rules))

                self.link_nodes(node2, plan_node)
                self.link_nodes(plan_node, node1)

            else:
                self.link_nodes(node2, node1)

            return c2

        return None

    def update_db(self, sentence: list[Atom], context: ExecutionContext):

        self.known_facts.append(sentence)

    def find_node(self, atoms: list[Atom]) -> None | ExplanationNode:
        atom = atoms[0]
        for index, node in enumerate(self.nodes):
            if node.get_atom() == atom:
                return node
        return None

    def find_potential_node(self, atoms: list[Atom], context):
        for node in self.nodes:
            if isinstance(node, PlanNode):
                for potential_plan in node.get_potential_plans():
                    print("pot", potential_plan)
                    print("atoms", atoms)
                    id_bindings = id_unification([potential_plan], atoms, [])
                    if id_bindings is not None:
                        print("MATCH")
                        b1, b2 = self.process_id_unification_result(id_bindings)
                        self.store_identity(b1, b2, context)
                    return node
        return None

    def process_id_unification_result(self, result: list[list[Atom, Atom]]):
        b1 = {}
        b2 = {}

        for duo in result:
            variable = self.variable_generator.next()
            b1[variable] = duo[0]
            b2[variable] = duo[1]

        return b1, b2

    def add_node(self, atoms: list[Atom], context) -> ExplanationNode:
        node = self.find_node(atoms)
        if node is not None:
            return node

        node = self.find_potential_node(atoms, context)
        if node is not None:
            node.set_atom(atoms[0])
            return node

        atom = atoms[0]
        index = len(self.nodes)
        if atom.predicate == "plan":
            new_node = PlanNode(index, atom)
        elif atom.predicate == "goal":
            new_node = GoalNode(index, atom)
        else:
            new_node = ActionNode(index, atom)

        self.nodes.append(new_node)
        return new_node

    def link_nodes(self, parent: ExplanationNode, child: ExplanationNode):
        if isinstance(parent, GoalNode):
            if isinstance(child, PlanNode):
                parent.add_attempt(child.id)
        elif isinstance(parent, PlanNode):
            if isinstance(child, GoalNode):
                parent.add_subepisode(child.id)
            elif isinstance(child, ActionNode):
                parent.add_action(child.id)

        child.parent = parent

    def explain(self, question: list[Atom], context: ExecutionContext):
        event = explain(question, self.nodes, self.induction_model, context, self.dialog)

        cause = None
        goal_count = 0

        # print("event id", event)

        # find the second goal above the event
        # (the first goal in not very informative)
        while event is not None:
            if isinstance(event, GoalNode):
                goal_count += 1
                if goal_count == 2:
                    cause = event.get_atom()
            event = event.parent

        return cause
