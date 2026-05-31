import re
from vrel.core.constants import IGNORED


class Parameter:
    name: str
    argument_size: int | None
    type: any

    def __init__(self, name: str, entity_type: any, argument_size: int = None):
        self.name = name
        self.argument_size = argument_size
        self.type = entity_type


class Relation:
    predicate: str
    parameters: list[Parameter] | None
    relation_size: str
    query_function: callable
    write_function: callable

    def __init__(
        self,
        predicate: str,
        parameters: list[Parameter],
        query_function: callable = None,
        write_function: callable = None,
        relation_size: str = IGNORED,
    ) -> None:
        if not re.fullmatch("\\$?[\\w_]+", predicate):
            raise Exception("Predicate is not a word: " + predicate)

        self.predicate = predicate
        self.parameters = parameters
        self.query_function = query_function
        self.relation_size = relation_size
        self.write_function = write_function

    def get_parameter_names(self):
        if self.parameters is None:
            return None
        return list(map(lambda e: e.name, self.parameters))

    def get_parameter_by_name(self, name: str) -> Parameter | None:
        return next(filter(lambda p: p.name == name, self.parameters), None)
