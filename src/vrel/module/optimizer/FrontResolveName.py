from vrel.core.Model import Model
from vrel.core.constants import RESOLVE_NAME
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


class FrontResolveName:

    def sort(self, composition: list[Atom]):
        name_resolvers, others = self.extract_list(composition)
        return name_resolvers + others

    def extract_list(self, composition: list[Atom]):
        name_resolvers = []
        rest_composition = []

        for atom in composition:
            if isinstance(atom, list):
                child_name_resolvers, child = self.extract_list(atom)
                name_resolvers.extend(child_name_resolvers)
                rest_composition.append(child)
            elif isinstance(atom, Atom):
                if atom.predicate == RESOLVE_NAME:
                    name_resolvers.append(atom)
                else:
                    child_name_resolvers, child = self.extract_atom(atom)
                    name_resolvers.extend(child_name_resolvers)
                    rest_composition.append(child)
            else:
                rest_composition.append(atom)

        return name_resolvers, rest_composition

    def extract_atom(self, atom: Atom):
        name_resolvers = []
        rest_composition = []

        for _, arg in atom.numbered_arguments:
            if isinstance(arg, list):
                child_name_resolvers, child = self.extract_list(arg)
                name_resolvers.extend(child_name_resolvers)
                rest_composition.append(child)
            else:
                rest_composition.append(arg)

        return name_resolvers, Atom(atom.variable, atom.predicate, *rest_composition)
