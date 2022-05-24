import mysql.connector as mycon
from mysql.connector import pooling


class YehPW_UAS_DB_Service():
    def __init__(self, mysql_url, mysql_username, mysql_password, mysql_db_name):
        self._mysql_url = mysql_url
        self._mysql_username = mysql_username
        self._mysql_password = mysql_password
        self._mysql_db_name = mysql_db_name
        self._db_config = {
            "host" : self._mysql_url,
            "user" : self._mysql_username,
            "password" : self._mysql_password,
            "database" : self._mysql_db_name
        }
        self._db_pool = pooling.MySQLConnectionPool(pool_name="yehpw_pool", pool_size=10, **self._db_config)
        self._isolation_setting()

    def _cursor(self):
        conn = self._db_pool.get_connection()
        return conn

    def _isolation_setting(self):
        query = "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED"
        self._cursor.execute(query)
        self._conn.commit()

    # Authn & Authz
