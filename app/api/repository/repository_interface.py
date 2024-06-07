from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def get_list(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass
