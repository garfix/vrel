"""
Factory that constructs a ready-to-use Chat-80 Vrel system.

The Chat-80 integration test owns the canonical wiring (`tests/integration/chat80/test.py`);
this module just lifts that wiring into a function so MCP / scripts / notebooks can reuse it.
"""

import pathlib
import sys

from vrel.core.BasicGenerator import BasicGenerator
from vrel.core.BasicSystem import BasicSystem
from vrel.core.Logger import Logger
from vrel.core.Model import Model
from vrel.grammar.en_us_write import get_en_us_write_grammar
from vrel.module.BasicDialogContext import BasicDialogContext
from vrel.module.BasicOutputBuffer import BasicOutputBuffer
from vrel.module.DeductionModule import DeductionModule
from vrel.module.OptimizerModule import OptimizerModule
from vrel.processor.parser.BasicParser import BasicParser
from vrel.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor

CHAT80_DIR = (
    pathlib.Path(__file__).resolve().parent.parent.parent
    / "tests" / "integration" / "chat80"
)

# The Chat-80 app modules use local imports (`from Chat80DB import Chat80DB`),
# so its directory must be on sys.path before importing them.
if str(CHAT80_DIR) not in sys.path:
    sys.path.insert(0, str(CHAT80_DIR))

from Chat80DB import Chat80DB  # noqa: E402
from Chat80Module import Chat80Module  # noqa: E402
from read_grammar import get_read_grammar  # noqa: E402
from write_grammar import get_write_grammar  # noqa: E402


def build_chat80_system() -> BasicSystem:
    path = str(CHAT80_DIR) + "/"

    db = Chat80DB()
    facts = Chat80Module(db)

    inferences = DeductionModule()
    inferences.import_rules(path + "inferences.pl")
    inferences.import_rules(path + "intents.pl")

    output_buffer = BasicOutputBuffer()
    dialog_context = BasicDialogContext()
    optimizer = OptimizerModule()

    model = Model([facts, inferences, optimizer, output_buffer, dialog_context])

    read_grammar = SimpleGrammarRulesParser().parse_read_grammar(get_read_grammar())
    parser = BasicParser(read_grammar)

    composer = SemanticComposer()
    executor = AtomExecutor()

    write_grammar = SimpleGrammarRulesParser().parse_write_grammar(
        get_en_us_write_grammar() + get_write_grammar()
    )
    generator = BasicGenerator(write_grammar, model, output_buffer)

    return BasicSystem(
        model=model,
        parser=parser,
        composer=composer,
        executor=executor,
        output_generator=generator,
        logger=Logger(),
    )
