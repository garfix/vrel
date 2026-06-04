from vrel.entity.Atom import Atom
from vrel.entity.Id import Id
from vrel.entity.Variable import Variable
from vrel.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


def generate_variables(term: any, variable_generator: VariableGenerator, variable_map: dict):
    # list
    if isinstance(term, list):
        return [generate_variables(arg, variable_generator, variable_map) for arg in term]
    # atom
    elif isinstance(term, Atom):
        return term.apply_to_each_atom(lambda arg: generate_variables(arg, variable_generator, variable_map))
    # variable
    elif isinstance(term, Variable):
        if term.name in variable_map:
            return variable_map[term.name]
        else:
            v = Variable(variable_generator.next())
            variable_map[term.name] = v
            return v
    else:
        # just the value
        return term


def generate_constants(term: any, variable_generator: VariableGenerator, variable_map: dict):
    # list
    if isinstance(term, list):
        return [generate_constants(arg, variable_generator, variable_map) for arg in term]
    # atom
    elif isinstance(term, Atom):
        return term.apply_to_each_atom(lambda arg: generate_constants(arg, variable_generator, variable_map))
    # variable
    elif isinstance(term, Variable):
        if term.name in variable_map:
            return variable_map[term.name]
        else:
            v = Id(variable_generator.next(), "entity")
            variable_map[term.name] = v
            return v
    else:
        # just the value
        return term


def variablize(term):
    # list
    if isinstance(term, list):
        return [variablize(arg) for arg in term]
    # atom
    elif isinstance(term, Atom):
        a = term.copy()
        a.arguments = variablize(a.arguments)
        a.modifiers = variablize(a.modifiers)
        return a
    # variable
    elif isinstance(term, str) and term[0:3] == "DLG":
        return Variable(term)
    # id
    elif isinstance(term, Id):
        return Variable(term.id)
    else:
        # just the value
        return term
