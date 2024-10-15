import pymysql
import json
import os

class GetConnection:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    @classmethod
    def get_connection_file(cls, file_name):
        if file_name.endswith('.json'):
            with open('test.json', 'r') as file:
                content = json.load(file)
            host = content['host']
            user = content['user']
            password = content['password']
        return cls(host, user, password)

    def get_mysql_conn(self):
        mysqldbconn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password)
        return mysqldbconn