from dataclasses import dataclass

from vrel.interface.SomeLogger import SomeLogger
import shutil

NO_COLOR = "\033[0m"
HEADER_COLOR = "\033[33m"
SECTION_COLOR = "\033[36m"
VALUE_COLOR = "\033[37m"
SEPARATOR_COLOR = "\033[33m"
KEY_COLOR = "\033[34m"
ERROR_COLOR = "\033[31m"
COMMENT_COLOR = "\033[90m"


@dataclass(frozen=True)
class Entry:
    type: str
    name: str
    value: any


class Logger(SomeLogger):

    entries: list[Entry]

    def __init__(self):
        self.entries = []

    def clear(self):
        self.entries = []

    def add(self, entry):
        self.entries.append(entry + "\n")

    def add_test_number(self, test_number: int):
        self.entries.append(Entry("test-number", "", test_number))

    def add_value(self, key: str, value: str):
        self.entries.append(Entry("value", key, value))

    def add_section(self, head, section):
        self.entries.append(Entry("section", head, section))

    def add_comment(self, comment: str):
        self.entries.append(Entry("comment", None, comment))

    def add_error(self, error):
        self.entries.append(Entry("error", None, error))

    def __str__(self) -> str:
        s = ""
        for entry in self.entries:
            if entry.type == "section":
                s += SECTION_COLOR + entry.name + NO_COLOR + "\n"
                s += str(entry.value) + "\n\n"
            elif entry.type == "test-number":
                terminal_width = shutil.get_terminal_size().columns
                sep = "~" * terminal_width
                line = "{}~~[{} {} {}]{}".format(SEPARATOR_COLOR, VALUE_COLOR, entry.value, SEPARATOR_COLOR, sep)
                truncated = line[: terminal_width + len(SEPARATOR_COLOR) + len(VALUE_COLOR) + len(SEPARATOR_COLOR)]
                s += truncated + NO_COLOR + "\n\n"

            elif entry.type == "value":
                s += ("{}[{}]{} {}\n").format(KEY_COLOR, entry.name, NO_COLOR, entry.value) + "\n\n"
            elif entry.type == "comment":
                s += str(entry.value) + "\n\n"
            elif entry.type == "error":
                s += ERROR_COLOR + entry.value + NO_COLOR + "\n\n"
            else:
                raise Exception(f"Unknown log type: {entry.type}")
        return s
