from __future__ import annotations
from vrel.entity.Sentinel import Sentinel
from vrel.entity.Variable import Variable


MODIFIER_TYPE_PRE = "pre"
MODIFIER_TYPE_POST = "post"
MODIFIER_TYPE_DURING = "during"
MODIFIER_TYPE_ANYWHERE = "anywhere"


class Atom:
    predicate: str
    arguments: list
    modifiers: list[Atom]
    type: str

    def __init__(self, *args):
        self.arguments = []
        self.modifiers = []
        self.type = MODIFIER_TYPE_ANYWHERE
        self.determiner = None

        if len(args) < 1:
            raise Exception("Atom must have at least a predicate")

        if isinstance(args[0], str):
            self.predicate = args[0]
        else:
            raise Exception(f"Arg 1 must hold the predicate: {args}")

        for arg in args[1:]:
            if (
                isinstance(arg, Atom)
                or isinstance(arg, float)
                or isinstance(arg, int)
                or isinstance(arg, str)
                or isinstance(arg, Variable)
                or isinstance(arg, list)
                or isinstance(arg, Sentinel)
            ):
                self.arguments.append(arg)
            else:
                raise Exception(f"Unknown argument type: {arg}")

    def copy(self):
        a = Atom(
            self.predicate,
            *self.arguments,
        )
        a.type = self.type
        a.determiner = self.determiner
        a.modifiers.extend(self.modifiers)
        return a

    def apply(self, func):
        a = self.copy()
        a.arguments = [func(arg) for arg in a.arguments]
        a.modifiers = [func(mod) for mod in a.modifiers]
        return a

    def mod(self, modifier: list[Atom]):
        if isinstance(modifier, Atom):
            a = self.copy()
            a.modifiers.append(modifier)
            return a
        elif isinstance(modifier, list):
            a = self.copy()
            a.modifiers.extend(modifier)
            return a
        else:
            raise Exception("A modifier must be an atom or a list of atoms")

    def with_determiner(self, determiner: Atom):
        a = self.copy()
        a.determiner = determiner
        return a

    def pre(self, *atoms: list[Atom]):
        return self._modify(MODIFIER_TYPE_PRE, atoms)

    def post(self, *atoms: list[Atom]):
        return self._modify(MODIFIER_TYPE_POST, atoms)

    def any(self, *atoms: list[Atom]):
        return self._modify(MODIFIER_TYPE_ANYWHERE, atoms)

    def _modify(self, type: str, atoms: list[Atom]):
        if len(self.modifiers) > 0:
            raise Exception("The atom already has modifiers")
        a = self.copy()
        a.modifiers = atoms
        a.type = type
        return a

    def clear_modifiers(self):
        return Atom(
            self.predicate,
            *self.arguments,
        )

    def get_modifier(self, predicate: str) -> Atom | None:
        for mod in self.modifiers:
            if mod.predicate == predicate:
                return mod
        return None

    def remove_modifiers(self, predicate: str) -> Atom:
        new_modifiers = []
        for mod in self.modifiers:
            if mod.predicate != predicate:
                new_modifiers.append(mod)

        return Atom(
            self.predicate,
            *self.arguments,
        ).mod(new_modifiers)

    def get_modifiers(self, predicate: str) -> list[Atom]:
        mods = []
        for mod in self.modifiers:
            if mod.predicate == predicate:
                mods.append(mod)
        return mods

    def __eq__(self, value):
        return (
            isinstance(value, Atom)
            and self.predicate == value.predicate
            and self.arguments == value.arguments
            and self.modifiers == value.modifiers
        )

    def __repr__(self):
        from vrel.core.functions.terms import format_term

        return format_term(self)
