from __future__ import annotations
from vrel.entity.Sentinel import Sentinel
from vrel.entity.Variable import Variable


class Atom:
    predicate: str
    arguments: list
    modifiers: list[Atom]

    def __init__(self, *args):
        self.arguments = []
        self.modifiers = []

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
        a.modifiers.extend(self.modifiers)
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
        return isinstance(value, Atom) and self.predicate == value.predicate and self.arguments == self.arguments

    def __repr__(self):
        from vrel.core.functions.terms import format_term

        return format_term(self)
