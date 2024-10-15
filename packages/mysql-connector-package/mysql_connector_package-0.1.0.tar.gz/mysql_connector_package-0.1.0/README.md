# MySQL Connector Package

A simple Python package that connects to a MySQL database using pymysql.

## Usage

```python
from my_connector.get_connection import GetConnection

# Method 1: Direct credentials
conn = GetConnection(host='localhost', user='root', password='password').get_mysql_conn()

# Method 2: Load credentials from JSON file
conn = GetConnection.get_connection_file('test.json').get_mysql_conn()
