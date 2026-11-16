from vrel.entity.BasicReference import BasicReference


class Reference(BasicReference):

    features: dict[str, str]

    def __init__(self, variable, features: dict[str, str]):
        super().__init__(variable)
        self.features = features

    def __repr__(self):
        return f"Reference {self.variable}"
