from vrel.entity.Relation import Parameter, Relation
from vrel.module.BasicOutputBuffer import BasicOutputBuffer


class SIROutputBuffer(BasicOutputBuffer):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(Relation("output_count", parameters=[Parameter("number", int)]))
        self.add_relation(
            Relation("output_how_many", parameters=[Parameter("type1", "thing"), Parameter("type2", "thing")])
        )
        self.add_relation(
            Relation("output_dont_know_part_of", parameters=[Parameter("type1", "thing"), Parameter("type2", "thing")])
        )
        self.add_relation(Relation("output_location", parameters=[Parameter("object", None)]))

        # helper to use `left of` in the "broader sense" using transitivity
        self.add_relation(Relation("context", parameters=[Parameter("type", str)]))
