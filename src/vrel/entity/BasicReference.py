from vrel.entity.Variable import Variable


class BasicReference:
    variable: Variable

    def __init__(self, variable: Variable):
        self.variable = variable
