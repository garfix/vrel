from vrel.core.functions.helper import hash_it
from vrel.core.functions.terms import bind_variables
from vrel.core.functions.variables import generate_constants, variablize
from vrel.entity.Atom import Atom
from vrel.entity.Id import Id
from vrel.entity.InductionRule import InductionRule
from vrel.entity.ExecutionContext import ExecutionContext
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

                for item in self.known_facts:

                    # match the consequent to the known item
                    item_binding = match(rule.consequent, item, {}, self.induction_model)
                    if item_binding is not None:

                        # the equality between dialog variables that connect two sentences can now be stored
                        self.store_identity(subject_binding, item_binding, context)

                        if rule.plan is not None:
                            # self.predicted_plan(current_subject, item)
                            pass
                        else:
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
                            pass
                            print("</>")

                        return True

        return False

    def predicted_plan(self, current_subject, item):
        # this:         P => Plan1 => Q
        # exist:        A => Plan2 => Q
        # new link:     P => Plan2
        node1 = self.add_node(current_subject)
        print("node1", node1)
        # print("rule", rule)
        node2 = self.add_node(item)
        plan_node_id = node2.get_first_attempt()
        plan_node: PlanNode = self.nodes[plan_node_id]
        self.link_nodes(node2, plan_node)
        self.link_nodes(plan_node, node1)

    def predicted_no_plan(self, current_subject: list, item):
        found = False

        # todo: this creates a node that is of no use
        node1 = self.add_node(current_subject)
        node2 = self.add_node(item)
        if isinstance(node1, PlanNode) and isinstance(node2, GoalNode):

            plan_node_id = node2.get_first_attempt()
            if plan_node_id:
                plan_node: PlanNode = self.nodes[plan_node_id]
                sub_plan_node_ids = plan_node.get_subepisodes()
                print("sub_plan_node", self.nodes[sub_plan_node_ids[0]])
                if plan_node.is_empty():
                    pre_goal_ids = node1.get_subepisodes()
                    pre_action_ids = node1.get_actions()
                    # this:         Plan1 => Q
                    # exist:        pre-Q => empty Plan2 => Q
                    # new link:     pre-Q => empty Plan1:filled with Plan2
                    plan_node.plan = node1.plan

                    if len(pre_goal_ids) > 0:
                        subepisode = self.nodes[pre_goal_ids[0]]
                        self.link_nodes(plan_node, subepisode)
                    elif len(pre_action_ids) > 0:
                        action = self.nodes[pre_action_ids[0]]
                        self.link_nodes(plan_node, action)
                    else:
                        raise Exception("Plan has neither subepisode nor action")

                    found = True

        if not found:
            self.link_nodes(node2, node1)

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

            node1 = self.add_node(current_subject)
            node2 = self.add_node(c2)

            if last_rule.plan:
                self.generator += 1
                atoms = [Atom("plan", "variable", self.generator)]
                plan_node = self.add_node(atoms)
                chain.append(Link(atoms, rules))

                self.link_nodes(node2, plan_node)
                self.link_nodes(plan_node, node1)

            else:
                self.link_nodes(node2, node1)

            return c2

        return None

    def update_db(self, sentence: list[Atom], context: ExecutionContext):

        self.known_facts.append(sentence)

    def add_node(self, atoms: list[Atom]) -> ExplanationNode:
        atom = atoms[0]
        for index, node in enumerate(self.nodes):
            if node.get_atom() == atom:
                return node

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
