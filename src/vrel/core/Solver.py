from vrel.core.functions.terms import bind_variables, flatten, get_variables
from vrel.core.functions.results import tuple_results_to_bindings
from vrel.core.constants import DISJUNCTION, SAME_AS
from vrel.entity.Atom import Atom
from vrel.entity.BindingResult import BindingResult
from vrel.entity.Relation import Relation
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSolver import SomeSolver
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence


class Solver(SomeSolver):

    model: SomeModel
    logger: SomeLogger
    sentence: SemanticSentence

    def __init__(self, model: SomeModel, sentence: SemanticSentence = None, logger: SomeLogger = None) -> None:
        self.model = model
        self.sentence = sentence
        self.logger = logger

    def solve(self, atoms: Atom | list[Atom]) -> list[dict]:
        if not isinstance(atoms, list):
            raise Exception("Solver can only solve lists of atoms, this is not a list: " + str(atoms))

        return self.solve_rest(atoms, {})

    def solve_rest(self, atoms: list[Atom], binding: dict = {}) -> list[dict]:
        if len(atoms) == 0:
            return [binding]
        else:
            result = []
            bindings = self.solve_single(atoms[0], binding)
            for b in bindings:
                result.extend(self.solve_rest(atoms[1:], b))
            return result

    def solve_single(self, atom: Atom, binding: dict):

        if not isinstance(atom, Atom):
            raise Exception("Solver can only solve atoms, this is not an atom: " + str(atom))

        if atom.predicate == DISJUNCTION:
            return self.solve_disjunction(atom.arguments[0], binding)

        # handle infinite recursion
        stack_overflow_handler = self.model.get_stack_overflow_handler()
        if stack_overflow_handler.check_stack(atom):
            return []

        result = self.solve_for_all_relations(atom, binding)

        # handle infinite recursion
        stack_overflow_handler.remove(atom)

        return result

    def solve_disjunction(self, disjuncts: list[list[Atom]], binding: dict):

        for disjunct in disjuncts:
            results = self.solve_rest(disjunct, binding)
            if len(results) > 0:
                return results
        return []

    def solve_for_all_relations(self, atom: Atom, binding: dict):
        predicate = atom.predicate
        bound_arguments = bind_variables(atom.arguments, binding)

        relations = self.model.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        deduplicated_bindings = {}

        for relation in relations:
            for bound_argument_variant in self.get_same_as_variants(bound_arguments, relation):
                out_bindings = self.find_relation_values(relation, bound_argument_variant, binding)

                # deduplicate results
                for out_binding in out_bindings:
                    deduplicated_bindings[str(out_binding)] = out_binding

        return list(deduplicated_bindings.values())

    def get_same_as_variants(self, bound_arguments: list, relation: Relation):
        same_as_handler = self.model.get_same_as_handler()
        if same_as_handler:
            return same_as_handler.get_same_as_variants(bound_arguments, relation)
        else:
            return [bound_arguments]

    def find_relation_values(
        self, relation: Relation, bound_arguments: list, binding: dict, sentence: SemanticSentence = None
    ) -> list[dict]:

        predicate = relation.predicate
        context = ExecutionContext(relation, self, sentence, self.model, self.logger)

        # call the relation's query function
        out_values = relation.query_function(bound_arguments, context)

        if isinstance(out_values, BindingResult):

            # note: only one predicate can have a BindingResult
            completed_values = [binding | out_value for out_value in out_values]
            out_bindings = list(completed_values)

        elif isinstance(out_values, list):

            if len(out_values) > 0:
                if not isinstance(out_values[0], list) and not isinstance(out_values[0], tuple):
                    raise Exception("The results of '" + predicate + "' should be lists or tuples")
                if len(out_values[0]) != len(bound_arguments):
                    raise Exception(
                        f"The number of arguments in the results of '{predicate}' is {str(len(out_values[0]))} and should be {len(bound_arguments)}"
                    )

            out_bindings = tuple_results_to_bindings(predicate, bound_arguments, out_values, binding)

        else:
            raise Exception("The result of '" + predicate + "' should be a list")

        return out_bindings

    def write_atom(self, atom: Atom):

        predicate = atom.predicate
        flat = flatten(atom)

        if not isinstance(atom, Atom):
            raise Exception(f"Solver only writes atoms, and this is not an atom: {atom}")

        # when a new same_as record is added, clear the same_as handler's cache
        same_as_handler = self.model.get_same_as_handler()
        if same_as_handler and predicate == SAME_AS:
            same_as_handler.clear_cache()

        relations = self.model.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        if len(get_variables(flat)) > 0:
            raise Exception(f"'{predicate}' attempts to persist a variable: {flat}")

        # print("WRITE", atom)

        for relation in relations:
            if relation.write_function is not None:
                context = ExecutionContext(relation, self, None, self.model, self.logger)
                relation.write_function(flat, context)

    def write_atoms(self, atoms: list[Atom]):
        for atom in atoms:
            self.write_atom(atom)
