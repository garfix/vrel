from abc import abstractmethod


class SomePronounHandler:

    @abstractmethod
    def update_saliency(self, Atom) -> any:
        pass
