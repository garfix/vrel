from vrel.entity.Relation import Relation
from vrel.module.BasicOutputBuffer import BasicOutputBuffer


class SimpleOutputBuffer(BasicOutputBuffer):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_predicate", formal_parameters=["predication", "predicate"]))
        self.add_relation(Relation("output_subject", formal_parameters=["predication", "subject"]))
        self.add_relation(Relation("output_object", formal_parameters=["predication", "object"]))
