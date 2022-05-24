import mysql.connector as mycon


class YehPW_UAS_DB_Init():
    def __init__(self, mysql_url, mysql_username, mysql_password, mysql_db_name):
        self._mysql_url = mysql_url
        self._mysql_username = mysql_username
        self._mysql_password = mysql_password
        self._mysql_db_name = mysql_db_name
        self._create_db_if_not_exist()
        self._conn = self._create_connection()

    def _create_connection(self):
        connection = mycon.connect(
            host=self._mysql_url,
            user=self._mysql_username,
            password=self._mysql_password,
            database=self._mysql_db_name
        )
        return connection

    def _create_db_if_not_exist(self):
        db = mycon.connect(
            host=self._mysql_url,
            user=self._mysql_username,
            password=self._mysql_password
        )
        query = "CREATE DATABASE IF NOT EXISTS %s;"
        cursor = db.cursor()
        cursor.execute(query % (self._mysql_db_name,))
        db.commit()
        cursor.close()
        db.close()

    def _init_accounts_table(self):
        command = "CREATE TABLE accounts(account_id VARCHAR(191) UNIQUE, account_password BINARY(60), account_role VARCHAR(191));"
        cursor = self._conn.cursor()
        cursor.execute(command)
        self._conn.commit()
        cursor.close()

    def _init_products_table(self):
        command = "CREATE TABLE products(product_name VARCHAR(191) UNIQUE, product_price INT, product_image VARCHAR(191));"
        cursor = self._conn.cursor()
        cursor.execute(command)
        self._conn.commit()
        cursor.close()

    def _init_invoices_table(self):
        command = "CREATE TABLE invoices(invoice_id INT AUTO_INCREMENT PRIMARY KEY, invoice_date DATE, invoice_total INT) AUTO_INCREMENT=1000;"
        cursor = self._conn.cursor()
        cursor.execute(command)
        self._conn.commit()
        cursor.close()

    def _init_solds_table(self):
        command = "CREATE TABLE solds(sold_date DATE, product_name VARCHAR(191), solds_quantity INT, product_price INT, sub_total INT);"
        cursor = self._conn.cursor()
        cursor.execute(command)
        self._conn.commit()
        cursor.close()

    def _init_accounts(self):
        manager1_pw = bcrypt.hashpw(b'manager1_pw', bcrypt.gensalt())
        manager2_pw = bcrypt.hashpw(b'manager2_pw', bcrypt.gensalt())
        cashier1_pw = bcrypt.hashpw(b'cashier1_pw', bcrypt.gensalt())
        cashier2_pw = bcrypt.hashpw(b'cashier2_pw', bcrypt.gensalt())
        command = """
            INSERT INTO accounts(account_id, account_password, account_role)
            VALUES
                ("manager1", %s, "manager"),
                ("manager2", %s, "manager"),

                ("cashier1", %s, "cashier"),
                ("cashier2", %s, "cashier");
        """
        cursor = self._conn.cursor()
        cursor.execute(command, (manager1_pw, manager2_pw,
                       cashier1_pw, cashier2_pw))
        self._conn.commit()
        cursor.close()

    def _init_products(self):
        command = """
            INSERT INTO products( product_name, product_price, product_image)
            VALUES
                ("Ayam Goreng Dada", 8000, "ayam_goreng_dada"),
                ("Ayam Goreng Paha Atas", 8000, "ayam_goreng_paha_atas"),
                ("Ayam Goreng Paha Bawah", 7000, "ayam_goreng_paha_bawah"),
                ("Ayam Goreng Sayap", 6000, "ayam_goreng_sayap"),
                ("Nasi", 2000, "nasi"),
                ("Sambal Bawang", 3000, "sambal_bawang"),
                ("Sambal Terasi", 3000, "sambal_terasi"),
                ("Sambal Matah", 3000, "sambal_matah"),
                ("Sambal Ijo", 3000, "sambal_ijo"),
                ("Aqua 600ml", 3000, "aqua_600ml"),
                ("Coca-Cola", 5000, "coca_cola"),   
                ("Badak Sarsaparila", 5000, "badak_sarsaparila")
        """
        cursor = self._conn.cursor()
        cursor.execute(command)
        self._conn.commit()
        cursor.close()

    def init(self):
        self._init_accounts_table()
        self._init_products_table()
        self._init_invoices_table()
        self._init_solds_table()
        self._init_accounts()
        self._init_products()
        self._conn.close()
