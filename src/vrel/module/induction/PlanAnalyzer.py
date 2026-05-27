from vrel.core.functions.helper import hash_it
from vrel.core.functions.terms import bind_variables
from vrel.core.functions.variables import variablize
from vrel.entity.Atom import Atom
from vrel.entity.InferenceRule import InferenceRule
from vrel.entity.InductionRule import InductionRule
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Variable import Variable
from vrel.module.induction.Link import Link
from vrel.module.induction.explain import explain
from vrel.module.induction.match import match
from vrel.module.transform.query import make_query


# Based on MicroPAM (see https://github.com/garfix/micropam)
class PlanAnalyzer:

    known_themes: list[Atom]
    known_goals: list[Atom]
    known_plans: list[Atom]

    known_events = list[Atom]
    known_links = list

    try_check: dict

    def __init__(self):
        self.known_themes = []
        self.known_goals = []
        self.known_plans = []
        self.try_check = {}

        self.known_events = []
        self.known_links = []

    def add_known_event(self, atom: Atom):
        for index, a in enumerate(self.known_events):
            if a == atom:
                return index
        self.known_events.append(atom)
        return len(self.known_events) - 1

    def add_link(self, id1, id2):
        self.known_links.append([id1, id2])

    def justify(
        self,
        sentence: list[Atom],
        induction_rules: list[InductionRule],
        deduction_rules: list[InferenceRule],
        context: ExecutionContext,
    ):

        log = []

        log.append("")
        log.append("---")
        log.append("")
        log.append("Trying to explain")
        log.append(sentence)

        # print("#")

        chain: list[Link] = []

        current_subject = sentence

        while True:
            if self.predicted(
                current_subject,
                induction_rules,
                deduction_rules,
                context,
                log,
                sentence,
            ):
                break

            log.append("Does not confirm prediction")
            chain.append(Link(current_subject, induction_rules[:]))
            # print("push A", len(chain))

            current_subject = self.try_inference(chain, deduction_rules, context, log, sentence)
            if not current_subject:
                break

        if current_subject:
            log.append("Adding inference chain to data base")
            # print("---")
            for link in reversed(chain):
                # print("---1")
                # print(link.atoms)
                self.update_db(link.atoms, context, log)
            # print("--2")
            # print(current_subject)
            self.update_db(current_subject, context, log)

            prev = current_subject
            for link in reversed(chain):
                current = link.atoms
                id1 = self.add_known_event(prev)
                id2 = self.add_known_event(current)
                self.add_link(id2, id1)
                prev = current

        else:
            log.append("No inference chain found - adding")
            self.update_db(sentence, context, log)

        # for line in log:
        #     print(line)

        # for i, a in enumerate(self.known_events):
        #     print(i, a)

        # for i, a in enumerate(self.known_links):
        #     print(i, a)

    def explain(
        self,
        question: list[Atom],
        induction_rules: list[InductionRule],
        deduction_rules: list[InferenceRule],
        context: ExecutionContext,
    ):
        return explain(question, induction_rules, deduction_rules, context, self.known_events, self.known_links)

    def predicted(
        self,
        current_subject: list,
        induction_rules: list[InductionRule],
        deduction_rules: list[InferenceRule],
        context: ExecutionContext,
        log: list[str],
        sentence,
    ):
        # is cd part of the known plans, goals or themes?
        if self.isa("goal", current_subject):
            # return self.relate(sentence, self.known_themes, self.init_rules, deduction_rules, context, log) \
            #     or self.relate(sentence, self.known_plans, self.sub_for, deduction_rules, context, log)
            return self.relate(
                current_subject,
                self.known_themes,
                induction_rules,
                deduction_rules,
                context,
                log,
                sentence,
            ) or self.relate(
                current_subject,
                self.known_plans,
                induction_rules,
                deduction_rules,
                context,
                log,
                sentence,
            )
        elif self.isa("plan", current_subject):
            # return self.relate(sentence, self.known_goals, self.plans_for, deduction_rules, context, log)
            return self.relate(
                current_subject,
                self.known_goals,
                induction_rules,
                deduction_rules,
                context,
                log,
                sentence,
            )
        elif self.isa("action", current_subject):
            # return self.relate(sentence, self.known_plans, self.instance_of, deduction_rules, context, log)
            return self.relate(
                current_subject,
                self.known_plans,
                induction_rules,
                deduction_rules,
                context,
                log,
                sentence,
            )
        else:
            return None

    def relate(
        self,
        current_subject: list,
        item_list: list,
        induction_rules: list[InductionRule],
        deduction_rules: list[InferenceRule],
        context: ExecutionContext,
        log: list[str],
        sentence,
    ):
        # item_list contains known themes, goals, or plans
        # rule_list contains all rules that belong to the themes, goals or plans
        # each rule has an antecedent (rhs) and a consequent (lhs)
        # the function tries the match the current_subject (via the antecedent) with the known theme, goal, or plan (via the consequent)

        # The predict phase tries to link the current subject with a known item,
        # by matching the current subject with the antedent and the item with the consequent of an induction rule
        for item in item_list:
            for rule in induction_rules:
                # print("RELATE")
                # print("----------------------------")
                # print()
                # print("current_subject", current_subject)
                # print("antecedent", rule.antecedent)

                cs = make_query(current_subject)

                subject_binding = match(
                    rule.antecedent,
                    cs,
                    {},
                    deduction_rules,
                    context,
                    sentence,
                )
                if subject_binding is not None:

                    consequent1 = bind_variables(rule.consequent, subject_binding)
                    consequent2 = variablize(consequent1)

                    item_binding = match(consequent2, item, {}, deduction_rules, context, current_subject)

                    if item_binding is not None:
                        # the equality between dialog variables that connect two sentences can now be stored

                        # print(f" XX subject binding: {subject_binding}")
                        # print(f" XX rule antecedent: {rule.antecedent}")
                        # print(f" XX rule consequent: {rule.consequent}")
                        # print(f" XX consequent1: {consequent1}")
                        # print(f" XX consequent2: {consequent2}")
                        # print(f" XX item: {item}")

                        self.store_identity(item_binding, context, log)

                        # print("---")
                        # print(cs)
                        # print(item)

                        id1 = self.add_known_event(current_subject)
                        id2 = self.add_known_event(item)
                        self.add_link(id1, id2)

                        log.append("Confirms prediction from")
                        log.append(item)
                        return True

        return False

    def store_identity(
        self,
        item_binding: dict,
        context: ExecutionContext,
        log: list,
    ):
        # print(item_binding)

        for variable in item_binding:
            # todo: this excludes rule variables like E1, but they might need to be included
            if isinstance(item_binding[variable], str) and variable[0:3] == "DLG":
                log.append(f"SAME AS {variable}, {item_binding[variable]}")
                print(f"SAME AS {variable}, {item_binding[variable]}")
                context.solver.write_atom(Atom("same_as", variable, item_binding[variable]))

    def try_inference(
        self,
        chain: list[Link],
        deduction_rules: list[InferenceRule],
        context: ExecutionContext,
        log: list,
        sentence,
    ):
        # chain is a list of [cd, all_inference_rules]
        # return the lhs of the first match, and extend the chain
        current_subject = None
        while len(chain) > 0:
            last_link = chain.pop()
            # print("pop", len(chain))
            # try all inference rules in the cd
            # if the cd matches a rule, add it to the chain
            # and return the bound lhs of the rule
            current_subject = self.try_rules(
                last_link.atoms,
                last_link.rules[:],
                chain,
                deduction_rules,
                context,
                log,
                sentence,
            )
            if current_subject is None:
                log.append("No usable inferences from")
                log.append(last_link.atoms)
            else:
                break

        # print("end")

        if current_subject:
            log.append("Possible explanation assuming")
            log.append(current_subject)
            return current_subject

        return None

    def try_rules(
        self,
        current_subject,
        rules: list[InductionRule],
        chain: list[Link],
        deduction_rules: list[InferenceRule],
        context: ExecutionContext,
        log: list,
        sentence,
    ):
        # match cd with the rhs of each of the rules
        # if a match occurs, return a binding with the lhs of the rule
        last_rule = None
        binding = None
        while len(rules) > 0:
            last_rule = rules.pop()
            # print("TRY RULES")
            cs = make_query(current_subject)
            binding = match(
                last_rule.antecedent,
                cs,
                {},
                deduction_rules,
                context,
                sentence,
            )

            # log.append('')
            # log.append(f' XX antecedent: {last_rule.antecedent}')
            # log.append(f' XX current_subject: {current_subject}')
            # log.append(f' XX binding: {binding}')
            # log.append('')

            # if the combination of antecedent and binding has happened before, skip it
            hash = hash_it([last_rule.antecedent, binding])
            # print(hash, last_rule.antecedent, sentence, binding)
            if hash in self.try_check:
                continue
            else:
                self.try_check[hash] = True

            # print('binding', binding)

            if binding is not None:

                # print("!!!")
                # print(last_rule.consequent)

                # c = bind_variables(last_rule.consequent, binding)

                break

        if binding is not None:
            # append the fact to the chain
            chain.append(Link(current_subject, rules))
            # print("push B", len(chain))

            c = bind_variables(last_rule.consequent, binding)
            # print(c)

            return c

        # print("failed", current_subject)

        return None

    def update_db(self, sentence: list[Atom], context: ExecutionContext, log: list):
        log.append(sentence)

        # add cd as a fact to the `database`
        context.solver.write_atoms(sentence)

        # add cd to the known themes, goals or plans
        # if self.isa("is", sentence):
        #     log.append("---theme")
        #     self.known_themes.append(sentence)
        if self.isa("goal", sentence):
            self.known_goals.append(sentence)
        elif self.isa("plan", sentence):
            self.known_plans.append(sentence)
        else:
            log.append("---theme")
            # note: in MicroPAM only sentences with "is" are stored as themes (i.e. only the first sentence)
            self.known_themes.append(sentence)

    def isa(self, type: str, current_subject: any):
        predicate = current_subject[0].predicate
        return predicate == type
