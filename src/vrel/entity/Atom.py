from vrel.entity.Sentinel import Sentinel
from vrel.entity.Variable import Variable


class Atom:
    predicate: str
    arguments: dict
    named_arguments: dict
    numbered_arguments: list

    def __init__(self, *args):
        self.arguments = {}
        self.named_arguments = {}
        self.numbered_arguments = []

        if len(args) < 1:
            raise Exception("Atom must have at least 1 argument")

        if isinstance(args[0], str):
            self.predicate = args[0]
        else:
            raise Exception(f"Arg 1 must hold the predicate: {args}")

        for index, arg in enumerate(args[1:]):
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
                or isinstance(arg, Sentinel)
            ):
                self.arguments[index] = arg
                self.setNumberedArgument(index, arg)
            else:
                raise Exception(f"Unknown argument type: {arg}")

    def setNumberedArgument(self, index: int, value: any):
        while len(self.numbered_arguments) < index + 1:
            self.numbered_arguments.append(None)
        self.numbered_arguments[index] = value

    def add_arguments(self, arguments: dict):

        return Atom(
            self.predicate,
            self.arguments | arguments,
        )

    def set_predicate(self, predicate: str):

        return Atom(
            predicate,
            self.arguments,
        )

    def set_numbered_args(self, args: list[any]):

        return Atom(self.predicate, *args, self.named_arguments)

    def remove_argument(self, argument_name: str):
        new_args = {k: v for k, v in self.arguments.items() if k != argument_name}
        return Atom(
            self.predicate,
            new_args,
        )

    def copy(self):
        return Atom(
            self.predicate,
            self.arguments,
        )

    def __eq__(self, value):
        return (
            isinstance(value, Atom)
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

        return f"A({self.predicate}{pos_args}{nmd_args})"
