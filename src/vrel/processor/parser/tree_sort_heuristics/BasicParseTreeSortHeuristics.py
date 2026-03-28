from vrel.entity.ParseTreeNode import ParseTreeNode
from vrel.processor.parser.tree_sort_heuristics.SortByBoost import SortByBoost
from vrel.processor.parser.tree_sort_heuristics.SortByTreeDepth import SortByTreeDepth


class BasicParseTreeSortHeuristics:
    def sort_trees(self, trees: list[ParseTreeNode]) -> list[ParseTreeNode]:
        # in order of increasing priority:
        trees = SortByTreeDepth().sort(trees)
        trees = SortByBoost().sort(trees)
        return trees
