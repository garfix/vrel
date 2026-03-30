from vrel.core.constants import DUMMY

from vrel.entity.Variable import Variable


class Atom:
    predicate: str
    variable: Variable
    arguments: dict
    positional_arguments: list
    named_arguments: dict
    numbered_arguments: list

    def __init__(self, *args):
        self.arguments = {}
        self.positional_arguments = []
        self.named_arguments = {}
        self.numbered_arguments = []

        if len(args) < 1:
            raise Exception("Atom must have at least 1 argument")

        rest_start = 0
        if isinstance(args[0], str):
            self.predicate = args[0]
            self.variable = DUMMY
            rest_start = 1
        elif isinstance(args[1], str):
            if not isinstance(args[0], Variable):
                raise Exception(f"Arg 1 must be a variable: {args}")
            self.variable = args[0]
            self.predicate = args[1]
            rest_start = 2
        else:
            raise Exception(f"Either arg 1 or arg 2 must hold the predicate: {args}")

        if self.variable != DUMMY:
            self.positional_arguments.append(self.variable)

        for index, arg in enumerate(args[rest_start:]):
            if isinstance(arg, dict):
                self.arguments |= arg
                for k, v in arg.items():
                    self.named_arguments[k] = v
                    if k.startswith("ARG"):
                        raise Exception("Named arguments must not have numbered names: {args}")
            elif (
                isinstance(arg, Atom)
                or isinstance(arg, float)
                or isinstance(arg, int)
                or isinstance(arg, str)
                or isinstance(arg, Variable)
                or isinstance(arg, list)
            ):
                key = f"ARG{index}"
                self.arguments[key] = arg
                self.positional_arguments.append(arg)
                self.numbered_arguments.append(arg)
            else:
                raise Exception(f"Unknown argument type: {arg}")

        # print()
        # print(self.predicate)
        # print(self.named_arguments)
        # print(args)

    def addArguments(self, arguments: dict):
        return Atom(self.variable, self.predicate, *self.numbered_arguments, self.named_arguments | arguments)

    def __str__(self) -> str:
        from vrel.core.functions.terms import format_term

        return format_term(self, "")

    def __repr__(self):
        pos_args = ""
        for arg in self.numbered_arguments:
            pos_args += f", {repr(arg)}"
        nmd_args = ""
        for k, v in self.named_arguments.items():
            nmd_args += f", {k}={repr(v)}"

        return f"({self.variable}, {self.predicate}{pos_args}{nmd_args})"
