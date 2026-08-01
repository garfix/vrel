from abc import ABC, abstractmethod


class SomeLogger(ABC):

    @abstractmethod
    def add_test_number(self, test_number: int):
        pass

    @abstractmethod
    def add_value(self, key: str, value: str):
        """Key: value - single line"""
        pass

    @abstractmethod
    def add_comment(self, comment: str):
        """Comment"""
        pass

    @abstractmethod
    def add_section(self, head: str, section: any):
        """Header \n Section"""
        pass

    @abstractmethod
    def add_error(self, error):
        """Error"""
        pass

    @abstractmethod
    def clear(self):
        pass
