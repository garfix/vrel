import re
from vrel.core.constants import IGNORED


class Parameter:
    name: str
    argument_size: int | None
    entity_type: str | None

    def __init__(self, name: str, argument_size: int = None, entity_type: str = None):
        self.name = name
        self.argument_size = argument_size
        self.entity_type = entity_type


class Relation:
    predicate: str
    parameters: list[Parameter] | None
    relation_size: str
    # argument_sizes: list[str]
    query_function: callable
    write_function: callable
    # formal_parameters: list[str]

    def __init__(
        self,
        predicate: str,
        parameters: list[Parameter] = None,
        # formal_parameters: list[str] = None,
        query_function: callable = None,
        write_function: callable = None,
        relation_size: str = IGNORED,
        # argument_sizes: list[str] = [],
    ) -> None:
        if not re.fullmatch("\\$?[\\w_]+", predicate):
            raise Exception("Predicate is not a word: " + predicate)

        self.predicate = predicate
        self.parameters = parameters
        self.query_function = query_function
        self.relation_size = relation_size
        # self.argument_sizes = argument_sizes
        self.write_function = write_function
        # self.formal_parameters = formal_parameters

    def get_parameter_names(self):
        if self.parameters is None:
            return None
        return list(map(lambda e: e.name, self.parameters))
