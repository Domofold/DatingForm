from AbstractConnection import AbstractConnection
import os


class MysqlConnection(AbstractConnection):
    config = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_USER_PASS')}@{os.getenv('DB_URL')}"

    def connect(self):
        return self.config
