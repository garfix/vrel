from vrel.core.constants import SAME_AS
from vrel.core.functions.variables import reify_variable
from vrel.entity.Atom import Atom
from vrel.entity.BasicReference import BasicReference
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.ParseTreeNode import ParseTreeNode
from vrel.entity.Reference import Reference
from vrel.module.pronoun.saliency import EntityData, find_matching_entity


def resolve_anaphora(root: ParseTreeNode, entities: list[EntityData], context: ExecutionContext):
    resolve_parse_tree_node(root, entities, context)


def resolve_parse_tree_node(node: ParseTreeNode, entities: list[EntityData], context: ExecutionContext):
    reference = node.rule.ref
    if reference:
        handle_reference(reference, entities, context)

    # now use the functions of the constituents

    for child in node.children:
        resolve_parse_tree_node(child, entities, context)


def handle_reference(reference: BasicReference, entities: list[EntityData], context: ExecutionContext):
    same_as_relations = context.model.find_relations(SAME_AS)
    if len(same_as_relations) == 0:
        raise Exception(
            "Anaphoric relations can only be created if a PronounModule is added to the system (for same-as relations)"
        )

    if isinstance(reference, Reference):
        variable = reference.variable
        features = reference.features
        id = reify_variable(variable)
        referent = find_matching_entity(id, features, entities)

        if referent:
            context.logger.add_value("id", id)
            context.logger.add_value("features", features)
            context.logger.add_value("entities", entities)
            context.logger.add_value("referent", referent.ids)

            print(f"SAME AS REFERENCE {id}, {referent.ids[0]}")
            context.solver.write_atom(Atom(SAME_AS, id, referent.ids[0]))
