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

        for index, arg in enumerate(args[rest_start:]):
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self.arguments[k] = v
                    if isinstance(k, int):
                        self.setNumberedArgument(k, v)
                    else:
                        self.named_arguments[k] = v
            elif (
                isinstance(arg, Atom)
                or isinstance(arg, float)
                or isinstance(arg, int)
                or isinstance(arg, str)
                or isinstance(arg, Variable)
                or isinstance(arg, list)
                or arg == None
            ):
                self.arguments[index] = arg
                self.setNumberedArgument(index, arg)
            else:
                raise Exception(f"Unknown argument type: {arg}")

        if self.variable != DUMMY:
            self.positional_arguments.append(self.variable)
        self.positional_arguments.extend(self.numbered_arguments)

    def setNumberedArgument(self, index: int, value: any):
        while len(self.numbered_arguments) < index + 1:
            self.numbered_arguments.append(None)
        self.numbered_arguments[index] = value

    def add_arguments(self, arguments: dict):

        return Atom(
            self.variable,
            self.predicate,
            self.arguments | arguments,
        )

    def set_predicate(self, predicate: str):

        return Atom(
            self.variable,
            predicate,
            self.arguments,
        )

    def set_arg1(self, arg: any):

        args = self.numbered_arguments
        args[0] = arg

        return Atom(self.variable, self.predicate, *args, self.named_arguments)

    def set_numbered_args(self, args: list[any]):

        return Atom(self.variable, self.predicate, *args, self.named_arguments)

    def remove_argument(self, argument_name: str):
        new_args = {k: v for k, v in self.arguments.items() if k != argument_name}
        return Atom(
            self.variable,
            self.predicate,
            *self.numbered_arguments,
            new_args,
        )

    def copy(self):
        return Atom(
            self.variable,
            self.predicate,
            *self.numbered_arguments,
            self.named_arguments,
        )

    def __eq__(self, value):
        return (
            isinstance(value, Atom)
            and self.variable == value.variable
            and self.predicate == value.predicate
            and self.numbered_arguments == value.numbered_arguments
            and self.named_arguments == self.named_arguments
        )

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

        return f"A({self.variable.name}, {self.predicate}{pos_args}{nmd_args})"
