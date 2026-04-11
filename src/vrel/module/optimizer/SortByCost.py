from vrel.core.functions.terms import get_variables
from vrel.core.constants import IGNORED, INFINITE
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSolver import SomeSolver


class SortByCost:
    """
    Based on "Efficient processing of interactive relational database queries in logic" - David H.D. Warren (1981)
    """

    def sort(
        self,
        composition: list[Atom],
        solver: SomeSolver,
        model: SomeModel,
        bound_variables: set[str] = set(),
    ):
        if len(composition) == 0:
            return []

        result = self.sort_rest([], composition, solver, model, bound_variables)

        return result

    def sort_rest(
        self,
        done: list[Atom],
        todo: list[Atom],
        solver: SomeSolver,
        model: SomeModel,
        bound_variables: set[str],
    ) -> list[Atom]:

        if len(todo) == 0:
            return done

        results = []
        for atom in todo:
            cost = self.calculate_cost(model, atom, bound_variables, solver)
            results.append({"atom": atom, "cost": cost})

        results.sort(key=lambda result: result["cost"])
        sorted = [result["atom"] for result in results]

        sorted_first_atom = self.sort_arguments(sorted[0], solver, model, bound_variables)
        bound_variables = bound_variables | set(get_variables(sorted_first_atom))

        return self.sort_rest(done + [sorted_first_atom], sorted[1:], solver, model, bound_variables)

    def sort_arguments(
        self,
        atom: Atom,
        solver: SomeSolver,
        model: SomeModel,
        bound_variables: set[str],
    ) -> Atom:
        new_args = atom.arguments.copy()
        replaced = False
        for key, value in atom.arguments.items():
            if isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], Atom):
                    new_args[key] = self.sort(value, solver, model, bound_variables)
                    replaced = True
        if replaced:
            return Atom(atom.predicate, new_args)
        else:
            return atom

    def calculate_cost(self, model: SomeModel, atom: Atom, bound_variables: set, solver: SomeSolver):
        predicate = atom.predicate
        relations = model.find_relations(predicate)
        if len(relations) == 0:
            return 0

        costs = []
        for relation in relations:
            unbound_argument_size_product = 1
            arguments = atom.numbered_arguments

            if relation.relation_size == IGNORED:
                cost = INFINITE
            else:

                if len(arguments) != len(relation.argument_sizes):
                    raise Exception("Number of argument sizes doesn't match that of relation: " + predicate)

                for argument, argument_size in zip(arguments, relation.argument_sizes):

                    if argument_size == IGNORED:
                        pass
                    elif isinstance(argument, Variable):
                        if argument.name in bound_variables:
                            unbound_argument_size_product *= argument_size
                    elif isinstance(argument, list):
                        pass
                    elif isinstance(argument, Atom):
                        pass
                    else:
                        unbound_argument_size_product *= argument_size

                cost = relation.relation_size / unbound_argument_size_product

            costs.append(cost)

        # if the predicate occurs in multiple relations, take the maximal cost
        # (not the sum of the costs, because we don't want to double the cost with 2 simular relations)
        return max(costs)
