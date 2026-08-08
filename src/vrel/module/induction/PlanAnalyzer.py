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

    def __init__(self, induction_model: SomeModel):
        self.induction_model = induction_model
        self.known_facts = []
        self.try_check = {}
        self.nodes: list[ExplanationNode] = []
        self.generator = 0
        self.variable_generator = VariableGenerator("PA")

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

            current_subject = self.try_inference(chain)
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

        # consider all known facts (item_list) and all rules (induction_rules)
        for item in self.known_facts:
            for rule in induction_rules:

                current_subject_query = make_query(current_subject)

                # match the antecedent to the current subject
                subject_binding = match(rule.antecedent, current_subject_query, {}, self.induction_model)
                if subject_binding is not None:

                    bound_consequent = bind_variables(rule.consequent, subject_binding)
                    variablized_consequent = variablize(bound_consequent)

                    # print("RELATE")
                    # print("----------------------------")
                    # print()
                    # print("current_subject", current_subject)
                    # print("antecedent", rule.antecedent)
                    # print("variablized_consequent", variablized_consequent)
                    # print("item", item)

                    # match the consequent to the known item
                    item_binding = match(variablized_consequent, item, {}, self.induction_model)

                    if item_binding is not None:
                        # the equality between dialog variables that connect two sentences can now be stored

                        # print(f" XX subject binding: {subject_binding}")
                        # print(f" XX rule antecedent: {rule.antecedent}")
                        # print(f" XX rule consequent: {rule.consequent}")
                        # print(f" XX consequent1: {bound_consequent}")
                        # print(f" XX consequent2: {variablized_consequent}")
                        # print(f" XX current subject: {current_subject}")
                        # print(f" XX item: {item}")

                        self.store_identity(item_binding, context)

                        if rule.plan:
                            # this:         P => Plan1 => Q
                            # exist:        A => Plan2 => Q
                            # new link:     P => Plan2
                            node1 = self.add_node(current_subject)
                            node2 = self.add_node(item)
                            # print(node2)
                            plan_node_id = node2.get_first_attempt()
                            plan_node: PlanNode = self.nodes[plan_node_id]
                            plan_node.subepisodes.append(node1.id)
                        else:

                            found = False

                            # todo: this creates a node that is of no use
                            node1 = self.add_node(current_subject)
                            node2 = self.add_node(item)
                            if isinstance(node1, PlanNode) and isinstance(node2, GoalNode):

                                plan_node_id = node2.get_first_attempt()
                                if plan_node_id:
                                    plan_node: PlanNode = self.nodes[plan_node_id]
                                    if plan_node.is_empty():
                                        pre_goal_ids = node1.get_subepisodes()
                                        pre_action_ids = node1.get_actions()
                                        # print("node1", node1)
                                        # print("node2", node2)
                                        # print("plan node", plan_node)
                                        # this:         Plan1 => Q
                                        # exist:        pre-Q => empty Plan2 => Q
                                        # new link:     pre-Q => empty Plan1:filled with Plan2
                                        plan_node.plan = node1.plan
                                        if len(pre_goal_ids) > 0:
                                            # plan_node.add_subepisode(pre_goal_ids[0])
                                            subepisode = self.nodes[pre_goal_ids[0]]
                                            self.link_nodes(plan_node, subepisode)
                                        elif len(pre_action_ids) > 0:
                                            # plan_node.add_action(pre_action_ids[0])
                                            action = self.nodes[pre_action_ids[0]]
                                            self.link_nodes(plan_node, action)

                                        else:
                                            raise Exception("Plan has neither subepisode nor action")

                                        found = True

                                        # exit()
                            if not found:
                                # print("link2", node1.id, node2.id)
                                self.link_nodes(node2, node1)

                        return True

        return False

    def store_identity(
        self,
        item_binding: dict,
        context: ExecutionContext,
    ):
        for variable in item_binding:
            if isinstance(item_binding[variable], Id):
                print(f"SAME AS {variable}, {item_binding[variable]}")
                context.solver.write_atom(Atom("same_as", Id(variable, "entity"), item_binding[variable]))

    def try_inference(
        self,
        chain: list[Link],
    ):
        # chain is a list of [cd, all_inference_rules]
        # return the lhs of the first match, and extend the chain
        current_subject = None
        while len(chain) > 0:
            last_link = chain.pop()
            # try all inference rules in the cd
            # if the cd matches a rule, add it to the chain
            # and return the bound lhs of the rule
            current_subject = self.try_rules(
                last_link.atoms,
                last_link.rules[:],
                chain,
            )
            if current_subject is not None:
                break

        if current_subject:
            return current_subject

        return None

    def try_rules(
        self,
        current_subject,
        rules: list[InductionRule],
        chain: list[Link],
    ):
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
            # append the fact to the chain

            # print(f" XX current_subject: {current_subject}")
            # print(f" XX binding: {binding}")

            chain.append(Link(current_subject, rules))

            c = bind_variables(last_rule.consequent, binding)
            # print("===")
            # print(last_rule.antecedent)
            # print(last_rule.consequent)
            # print(cs)
            # print(binding)
            # print(c)

            variable_map = {}
            c = generate_constants(c, self.variable_generator, variable_map)

            node1 = self.add_node(current_subject)
            node2 = self.add_node(c)

            if last_rule.plan:
                self.generator += 1
                atoms = [Atom("plan", "variable", self.generator)]
                plan_node = self.add_node(atoms)
                chain.append(Link(atoms, rules))

                self.link_nodes(node2, plan_node)
                self.link_nodes(plan_node, node1)
                # print("try rules")
                # print(node2)
                # print(node1)

            else:
                self.link_nodes(node2, node1)

            return c

        return None

    def update_db(self, sentence: list[Atom], context: ExecutionContext):

        # add cd as a fact to the `database`
        context.solver.write_atoms(sentence)

        self.known_facts.append(sentence)

    def explain(
        self,
        question: list[Atom],
    ):
        event = explain(
            question,
            self.nodes,
            self.induction_model,
        )

        cause = None

        while event is not None:
            atom = event.get_atom()
            if atom.predicate == "goal":
                cause = atom
            event = event.parent

        return cause
