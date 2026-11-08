from vrel.entity.ParseTreeNode import ParseTreeNode


def resolve_anaphora(root: ParseTreeNode):
    resolve_parse_tree_node(root)


def resolve_parse_tree_node(node: ParseTreeNode):
    # for argument in node.:
    #     print("AAA", argument)

    for child in node.children:
        resolve_parse_tree_node(child)
