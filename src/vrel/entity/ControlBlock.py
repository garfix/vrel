from __future__ import annotations
from vrel.entity.BlockResult import BlockResult
from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeProcessor import SomeProcessor


class ControlBlock:

    processor: SomeProcessor
    next_block: ControlBlock


    def __init__(self, processor) -> None:
        self.processor = processor


    def process(self, request: SentenceRequest) -> BlockResult:
        pass

