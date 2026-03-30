from vrel.core.functions.terms import flatten
from vrel.core.functions.unification import unification
from vrel.entity.BindingResult import BindingResult
from vrel.interface.SomeDataSource import SomeDataSource


class SimpleFrameDataSource(SomeDataSource):

    index: dict[str, list]

    def __init__(self):
        self.clear()

    def create_atom(self, table: str, columns: list[str], values: list):
        return tuple([table] + list(values))

    def select(self, table: str, columns: list[str], values: list) -> list[list]:
        atom = self.create_atom(table, columns, values)
        flat = flatten(atom)

        if not table in self.index:
            return []

        result = []
        for a in self.index[table]:
            binding = unification(a, flat, {})
            if binding is not None:
                result.append(binding)

        return BindingResult(result)

    def insert(self, table: str, columns: list[str], values: list):
        atom = self.create_atom(table, columns, values)

        if not table in self.index:
            self.index[table] = []

        self.index[table].append(atom)

    def clear(self):
        self.index = {}
