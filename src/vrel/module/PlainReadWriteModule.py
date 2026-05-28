from vrel.core.functions.terms import has_variables
from vrel.core.functions.unification import unification
from vrel.entity.Atom import Atom
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Relation import Parameter, Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeModule import SomeModule


class PlainReadWriteModule(SomeModule):
    """
    A flexible storage that accepts any relation, and no relation needs to be specified
    """

    atoms: list[tuple]

    def __init__(self, atoms: list[tuple] = []) -> None:
        super().__init__()

        self.atoms = []
        for atom in atoms:
            self.add_atom(atom)

    def add_atom(self, atom: Atom):

        self.atoms.append(atom)

        if has_variables(atom.arguments):
            raise Exception(f"Atom should be bound: {atom.arguments}")

        predicate = atom.predicate
        if predicate not in self.relations:
            arguments = atom.arguments
            # formal_parameters = [Variable(f"E{i}") for i, _ in enumerate(arguments)]
            formal_parameters = [Parameter(f"E{i}") for i, _ in enumerate(arguments)]
            self.add_relation(
                Relation(predicate, parameters=formal_parameters, query_function=self.query, write_function=self.write)
            )

    def query(self, arguments: list, context: ExecutionContext) -> list[list]:
        predicate = context.relation.predicate
        formal_parameters = context.relation.get_parameter_names()

        results = []
        for atom in self.atoms:
            if atom.predicate == predicate:
                if unification(formal_parameters, list(arguments), {}) is not None:
                    results.append(atom.arguments)

        return results

    def write(self, arguments: list, context: ExecutionContext):
        if has_variables(arguments):
            raise Exception(f"Atom should be bound: {arguments}")

        # print("write", tuple([context.relation.predicate] + list(arguments)))

        # self.atoms.append(tuple([context.relation.predicate] + list(arguments)))

    def get_relation(self, predicate: str) -> Relation | None:
        if not predicate in self.relations:
            self.add_relation(Relation(predicate, query_function=self.query, write_function=self.write))

        return self.relations[predicate]

    def clear(self):
        self.atoms = []
