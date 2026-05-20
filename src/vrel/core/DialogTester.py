from math import ceil
import unittest
import cProfile
import time

from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeSystem import SomeSystem


class DialogTester:

    test_case: unittest.TestCase

    tests: list
    system: SomeSystem

    # profile all tests and print the results
    profile: bool

    def __init__(
        self,
        test_case: unittest.TestCase,
        tests: list,
        system: SomeSystem,
        profile: bool = False,
    ) -> None:
        self.test_case = test_case
        self.tests = tests
        self.system = system
        self.profile = profile

    def run(
        self,
    ):
        if self.profile == True:
            cProfile.runctx("self.do_run()", globals(), locals(), None, "cumulative")
        else:
            self.do_run()

    def do_run(self):

        logger = self.system.get_logger()

        for i, test in enumerate(self.tests):

            logger.clear()

            if len(test) != 2:
                raise Exception("A test item must have two elements: a sentence and an expected response")

            question, expected = test

            request = SentenceRequest(question)

            # if log_this:
            logger.add_test_number(i + 1)
            logger.add_value("Human", question)

            try:
                # send the request through the pipeline
                start_time = time.perf_counter()
                self.system.enter(request)
                end_time = time.perf_counter()

                output = ""
                if self.system.output_generator:
                    output = self.system.read_output()

                logger.add_value("Computer", output)
                logger.add_comment(str(ceil((end_time - start_time) * 1000)) + " msecs")

                if output != expected:
                    logger.add_error("[Expected] " + str(expected))

                self.test_case.assertEqual(output, expected)

            except Exception as e:
                # print(logger)
                raise e
