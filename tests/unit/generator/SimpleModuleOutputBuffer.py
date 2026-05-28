from vrel.entity.Relation import Parameter, Relation
from vrel.module.BasicOutputBuffer import BasicOutputBuffer


class SimpleOutputBuffer(BasicOutputBuffer):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_predicate", parameters=[Parameter("predication"), Parameter("predicate")]))
        self.add_relation(Relation("output_subject", parameters=[Parameter("predication"), Parameter("subject")]))
        self.add_relation(Relation("output_object", parameters=[Parameter("predication"), Parameter("object")]))
