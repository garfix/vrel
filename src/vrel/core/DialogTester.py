from math import ceil
import unittest
import cProfile
import time

from vrel.core.Logger import Logger
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeLogger import ALL, LAST
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

    # def run(
    #     self,
    # ):
    #     if self.profile:
    #         cProfile.runctx("self.do_run()", globals(), locals(), None, "cumulative")
    #     else:
    #         self.do_run()

    def run(self):

        logger = self.system.logger

        for i, test in enumerate(self.tests):

            logger.clear()
            logger.log_all_tests()
            logger.log_products()

            if len(test) != 2:
                raise Exception("A test item must have two elements: a sentence and an expected response")

            question, expected = test

            request = SentenceRequest(question)

            # if log_this:
            logger.add_test_separator(i + 1)
            logger.add_key_value("Human", question)

            try:
                # send the request through the pipeline
                start_time = time.perf_counter()
                self.system.enter(request)
                end_time = time.perf_counter()

                output = ""
                if self.system.output_generator:
                    output = self.system.read_output()

                logger.add_key_value("Computer", output)
                logger.add_comment(str(ceil((end_time - start_time) * 1000)) + " msecs")

                if output != expected:
                    logger.add_error("[Expected] " + expected)

                self.test_case.assertEqual(output, expected)

            except Exception as e:
                print(logger)
                raise e
