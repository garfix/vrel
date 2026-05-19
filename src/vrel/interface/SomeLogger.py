from abc import ABC, abstractmethod


class SomeLogger(ABC):

    @abstractmethod
    def add_test_number(self, test_number: int):
        pass

    @abstractmethod
    def add_value(self, key: str, value: str):
        pass

    @abstractmethod
    def add_comment(self, key: str, value: str):
        pass

    @abstractmethod
    def add_section(self, header):
        pass

    @abstractmethod
    def add_error(self, error):
        pass

    @abstractmethod
    def clear(self):
        pass
