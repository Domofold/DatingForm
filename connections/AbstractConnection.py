from abc import abstractmethod, ABC


class AbstractConnection(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass
