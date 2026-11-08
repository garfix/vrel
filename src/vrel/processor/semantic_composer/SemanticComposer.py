from vrel.core.functions.terms import unify_variables
from vrel.entity.Atom import Atom
from vrel.entity.ParseTreeNode import ParseTreeNode
from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.Variable import Variable
from vrel.interface.SomeComposer import SomeComposer
from vrel.interface.SomeLogger import SomeLogger
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence
from vrel.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


class SemanticComposer(SomeComposer):
    """
    Performs semantic composition on the product of the parser
    Opimizes the composition for speed of execution
    """

    variable_generator: VariableGenerator

    def __init__(self) -> None:
        super().__init__()
        self.variable_generator = VariableGenerator("$")

    def process(self, parse_tree: ParseTreeNode, logger: SomeLogger) -> ProcessResult:

        self.check_for_sem(parse_tree)

        root_variables = [self.variable_generator.next() for _ in parse_tree.rule.antecedent.arguments]
        semantics, dialog_parse_tree = self.compose(parse_tree, root_variables)

        semantic_sentence = SemanticSentence(dialog_parse_tree, semantics, root_variables)

        logger.add_section("Unified parse tree", dialog_parse_tree)
        logger.add_section("Semantics", semantics)
        logger.add_section("Root variables", ", ".join(root_variables))

        return semantic_sentence

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
        child_nodes = []

        for child, consequent in zip(node.children, node.rule.consequents):
            if not child.is_leaf_node():
                incoming_child_variables = [map[arg] for arg in consequent.arguments]
                child_sem, child_node = self.compose(child, incoming_child_variables)
                child_semantics.append(child_sem)
                child_nodes.append(child_node)
            elif child.rule.sem:
                child_semantics.append(child.rule.sem())

        # create the semantics of this node by executing its function, passing the values of its children as arguments
        semantics = node.rule.sem(*child_semantics)

        # extend the map with variables found in the result of the semantics function
        self.extend_map_with_semantics(map, semantics)

        # replace the formal parameters in the semantics with the unified variables
        unified_semantics = unify_variables(semantics, map)

        # replace the formal parameters in the node with the unified variables
        unified_parse_node: ParseTreeNode = unify_variables(node, map)
        unified_parse_node.children = child_nodes

        return unified_semantics, unified_parse_node

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
                # since we're late in the game, don't replace variables that have already been replaced
                self.extend_map_with_semantics(map, element)
        elif isinstance(term, Atom):
            for arg in term.arguments:
                # since we're late in the game, don't replace variables that have already been replaced
                self.extend_map_with_semantics(map, arg)
            for mod in term.modifiers:
                self.extend_map_with_semantics(map, mod)
