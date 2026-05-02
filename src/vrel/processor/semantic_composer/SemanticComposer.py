from vrel.core.functions.terms import format_term
from vrel.entity.Atom import Atom
from vrel.entity.ReifiedVariable import ReifiedVariable
from vrel.entity.ParseTreeNode import ParseTreeNode
from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.Variable import Variable
from vrel.interface.SomeProcessor import SomeProcessor
from vrel.processor.parser.BasicParserProduct import BasicParserProduct
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence
from vrel.processor.semantic_composer.SemanticComposerProduct import SemanticComposerProduct
from vrel.processor.semantic_composer.helper.VariableGenerator import VariableGenerator
from vrel.entity.SemanticFunction import SemanticFunction


class SemanticComposer(SomeProcessor):
    """
    Performs semantic composition on the product of the parser
    Opimizes the composition for speed of execution
    """

    parser: SomeProcessor
    variable_generator: VariableGenerator

    def __init__(self, parser: SomeProcessor) -> None:
        super().__init__()
        self.parser = parser
        self.variable_generator = VariableGenerator("$")

    def get_name(self) -> str:
        return "Composer"

    def process(self, incoming: BasicParserProduct) -> ProcessResult:

        parse_trees = incoming.parse_trees
        sentences = []

        for parse_tree in parse_trees:

            self.check_for_sem(parse_tree)

            root_variables = [self.variable_generator.next() for _ in parse_tree.rule.antecedent.arguments]
            semantics = self.compose(parse_tree, root_variables)

            sentences.append(SemanticSentence(semantics, root_variables))

        product = SemanticComposerProduct(sentences)

        return ProcessResult([product], "")

    def check_for_sem(self, node: ParseTreeNode):
        if node.form == "" and node.rule.sem is None:
            raise Exception("Rule '" + str(node.rule) + "' is missing key 'sem'")

        for child in node.children:
            self.check_for_sem(child)

    def compose(self, node: ParseTreeNode, incoming_variables: list[str]) -> list[Atom]:

        # map formal variables to unified, sentence-wide variables
        map = self.create_map(node, incoming_variables)

        # collect the semantics of the child nodes
        child_semantics = []

        for child, consequent in zip(node.children, node.rule.consequents):
            if not child.is_leaf_node():
                incoming_child_variables = [map[arg] for arg in consequent.arguments]
                semantics = self.compose(child, incoming_child_variables)
                child_semantics.append(semantics)
            elif child.rule.sem:
                child_semantics.append(child.rule.sem())

        # create the semantics of this node by executing its function, passing the values of its children as arguments
        semantics = node.rule.sem(*child_semantics)

        # extend the map with variables found in the result of the semantics function
        self.extend_map_with_semantics(map, semantics)

        # replace the formal parameters in the semantics with the unified variables
        unified_semantics = self.unify_variables(semantics, map)

        return unified_semantics

    def create_map(self, node: ParseTreeNode, incoming_variables: list[str]):
        # start variable map by mapping antecedent variables to incoming variables
        map = {}
        for i, arg in enumerate(node.rule.antecedent.arguments):
            map[arg] = incoming_variables[i]

        # complete map with other variables from the consequents
        for cons in node.rule.consequents:
            for i, arg in enumerate(cons.arguments):
                if arg not in map:
                    map[arg] = self.variable_generator.next()

        return map

    def extend_map_with_semantics(self, map: dict, term: list[Atom]):
        if isinstance(term, Variable):
            if term.name not in map and not self.variable_generator.isinstance(term):
                map[term.name] = self.variable_generator.next()

        # only lists of atoms for now
        elif isinstance(term, list):
            for element in term:
                # for atom in term:
                # for arg in atom.arguments:
                # since we're late in the game, don't replace variables that have already been replaced
                self.extend_map_with_semantics(map, element)
                # if (
                #     isinstance(arg, Variable)
                #     and arg.name not in map
                #     and not self.variable_generator.isinstance(arg)
                # ):
                #     map[arg.name] = self.variable_generator.next()
        elif isinstance(term, Atom):
            for arg in term.arguments:
                # since we're late in the game, don't replace variables that have already been replaced
                self.extend_map_with_semantics(map, arg)
                # if isinstance(arg, Variable) and arg.name not in map and not self.variable_generator.isinstance(arg):
                #     map[arg.name] = self.variable_generator.next()

            for mod in term.modifiers:
                self.extend_map_with_semantics(map, mod)

    def unify_variables(self, term: any, map: dict[str, str]) -> any:
        if isinstance(term, list):
            return [self.unify_variables(atom, map) for atom in term]
        elif isinstance(term, Atom):
            # return Atom(
            #     term.predicate,
            #     *[self.unify_variables(arg, map) for arg in term.arguments],
            # ).mod([self.unify_variables(mod, map) for mod in term.modifiers])
            return term.apply_to_each_atom(lambda arg: self.unify_variables(arg, map))
        elif isinstance(term, tuple):
            raise Exception(f"tuple found 9: {term}")
            return tuple([self.unify_variables(term, map) for term in term])
        elif isinstance(term, SemanticFunction):
            return SemanticFunction(term.args, self.unify_variables(term.body, map))
        elif isinstance(term, Variable) and term.name in map:
            return Variable(map[term.name])
        elif isinstance(term, ReifiedVariable) and term.name in map:
            return map[term.name]
        else:
            return term
