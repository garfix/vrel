from abc import abstractmethod

from vrel.entity.ParseTreeNode import ParseTreeNode


class SomeParseTreeSortHeuristics:

    @abstractmethod
    def sort_trees(self, trees: list[ParseTreeNode]) -> list[ParseTreeNode]:
        pass
