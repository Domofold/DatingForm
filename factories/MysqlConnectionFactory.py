from factories.ConnectionFactory import ConnectionFactory
from connections.MysqlConnection import MysqlConnection


class MysqlConnectionFactory(ConnectionFactory):
    def connection(self):
        return MysqlConnection()
