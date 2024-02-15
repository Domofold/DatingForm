from ConnectionFactory import ConnectionFactory
from MysqlConnection import MysqlConnection


class MysqlConnectionFactory(ConnectionFactory):
    def connect(self):
        return MysqlConnection()
