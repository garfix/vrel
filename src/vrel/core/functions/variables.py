from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


def generate_variables(term: any, variable_generator: VariableGenerator, variable_map: dict):
    # list
    if isinstance(term, list):
        return [generate_variables(arg, variable_generator, variable_map) for arg in term]
    # tuple
    elif isinstance(term, tuple):
        raise Exception(f"tuple found!: {term}")
        return tuple([generate_variables(arg, variable_generator, variable_map) for arg in term])
    # atom
    elif isinstance(term, Atom):
        # return Atom(
        #     term.predicate,
        #     *[generate_variables(arg, variable_generator, variable_map) for arg in term.arguments],
        # ).mod([generate_variables(mod, variable_generator, variable_map) for mod in term.modifiers])
        return term.apply(lambda arg: generate_variables(arg, variable_generator, variable_map))
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


def variablize(term):
    # list
    if isinstance(term, list):
        return [variablize(arg) for arg in term]
    # tuple
    elif isinstance(term, tuple):
        raise Exception(f"tuple found!: {term}")
        return tuple([variablize(arg) for arg in term])
    # atom
    elif isinstance(term, Atom):
        raise Exception("Todo4")
    # variable
    elif isinstance(term, str) and term[0:1] == "$":
        return Variable(term)
    else:
        # just the value
        return term
