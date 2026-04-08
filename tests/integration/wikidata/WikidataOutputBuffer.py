from vrel.entity.Relation import Relation
from vrel.module.BasicOutputBuffer import BasicOutputBuffer
from vrel.module.SqliteMemoryModule import SqliteMemoryModule


class WikidataOutputBuffer(BasicOutputBuffer):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_report", formal_parameters=["report"]))
