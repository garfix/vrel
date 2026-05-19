from abc import abstractmethod


class SomeProduct:

    @abstractmethod
    def get_output(self) -> any:
        """
        When this product is the output of the pipeline, this is its value
        """
        pass
