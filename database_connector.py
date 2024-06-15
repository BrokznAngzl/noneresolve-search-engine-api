import pymysql


class DatabaseConnector:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database_name = 'ir2022'
        self.autocommit = True
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          database=self.database_name,
                                          autocommit=self.autocommit)

    def execute_query(self, sql):
        if not self.connection:
            self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def close_connection(self):
        if self.connection:
            self.connection.close()
