from connections.AbstractConnection import AbstractConnection
import os


class MysqlConnection(AbstractConnection):
    _config = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_USER_PASS')}@{os.getenv('DB_URL')}"

    def connect(self):
        return self._config
