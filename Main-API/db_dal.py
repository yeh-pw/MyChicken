import mysql.connector as mycon
from mysql.connector import pooling
import bcrypt


class YehPW_UAS_DB_Service():
    def __init__(self, mysql_url, mysql_username, mysql_password, mysql_db_name):
        self._mysql_url = mysql_url
        self._mysql_username = mysql_username
        self._mysql_password = mysql_password
        self._mysql_db_name = mysql_db_name
        self._db_config = {
            "host": self._mysql_url,
            "user": self._mysql_username,
            "password": self._mysql_password,
            "database": self._mysql_db_name
        }
        self._db_pool = pooling.MySQLConnectionPool(
            pool_name="yehpw_pool", pool_size=15, **self._db_config, pool_reset_session=False)
        self._isolation_setting()

    def _conn(self):
        conn = self._db_pool.get_connection()

        return conn

    def _isolation_setting(self):
        query = "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED"
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    # Authn & Authz

    def validation(self, id_to_check, pw_to_check):
        query = """
            SELECT * FROM accounts
            WHERE account_id = "%s";
        """
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute(query % (id_to_check,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row != None:
            true_pw = row[1]
            role = row[2]
            if bcrypt.checkpw(pw_to_check.encode("utf"), bytes(true_pw)):
                return {
                    "id": id_to_check,
                    "role": role}
            else:
                return False
        else:
            return None

    def get_products(self):
        query = """
            SELECT * FROM products;
        """
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return row

    # def get_invoices(self):
    #     query = """
    #         SELECT * FROM invoices;
    #     """
    #     conn = self._conn()
    #     cursor = conn.cursor()
    #     cursor.execute(query)
    #     row = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return row

    # def get_solds(self):
    #     query = """
    #         SELECT * FROM solds;
    #     """
    #     self._cursor.execute(query)
        # cursor = conn.cursor()
    #     row = self._cursor.fetchall()
    #     return row

    def post_invoice(self, total):
        command = """
            INSERT INTO invoices(invoice_date, invoice_total)
            VALUES(now(),%s);
        """
        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute(command, (total,))
        conn.commit()
        cursor.close()
        conn.close()

    def post_solds(self, product_name, solds_quantity, product_price, subtotal):

        command = """
            INSERT INTO solds(sold_date, product_name,solds_quantity, product_price, sub_total)
            VALUES(now(),%s,%s,%s,%s);
        """

        conn = self._conn()
        cursor = conn.cursor()
        cursor.execute(command, (product_name, solds_quantity,
                                 product_price, subtotal,))
        conn.commit()
        cursor.close()
        conn.close()
