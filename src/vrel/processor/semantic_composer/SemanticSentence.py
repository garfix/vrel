from dataclasses import dataclass
from vrel.entity.Atom import Atom
from vrel.entity.ParseTreeNode import ParseTreeNode


@dataclass(frozen=True)
class SemanticSentence:
    dialog_parse_tree: ParseTreeNode
    semantics: list[Atom]
    root_variables: list[str]
