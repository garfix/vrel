from vrel.entity.BasicReference import BasicReference


class Reference(BasicReference):

    attributes: dict[str, str]

    def __init__(self, variable, attributes: dict[str, str]):
        super().__init__(variable)
        self.attributes = attributes
