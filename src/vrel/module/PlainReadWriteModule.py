from vrel.core.functions.terms import has_variables
from vrel.core.functions.unification import unification
from vrel.entity.Atom import Atom
from vrel.entity.BindingResult import BindingResult
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

    def select(self, relation: Relation, columns: list[str], values: list[str]):
        return self.query(relation, values)

    def insert(self, relation: Relation, columns: list[str], values: list[str]):
        self.add_atom(Atom(relation.predicate, *values))

    def add_atom(self, atom: Atom):

        self.atoms.append(atom)

        if has_variables(atom.arguments):
            raise Exception(f"Atom should be bound: {atom.arguments}")

    def query(self, relation: Relation, arguments: list) -> list[list]:

        a = Atom(relation.predicate, *arguments)

        results = []
        for atom in self.atoms:
            u = unification(atom, a, {})
            if u is not None:
                results.append(u)

        return BindingResult(results)

    def clear(self):
        self.atoms = []
