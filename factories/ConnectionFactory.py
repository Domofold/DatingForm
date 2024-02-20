from abc import abstractmethod, ABC
from connections.AbstractConnection import AbstractConnection


class ConnectionFactory(ABC):
    @abstractmethod
    def connect(self) -> AbstractConnection:
        pass
