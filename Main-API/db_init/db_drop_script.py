import mysql.connector as mycon
import yaml

with open(r'./db_config.yaml') as file:
    db_config = yaml.load(file, Loader=yaml.FullLoader) 

mysql_db_address = db_config.get("mysql_db_address")
mysql_db_username = db_config.get("mysql_db_username")
mysql_db_password = db_config.get("mysql_password")
mysql_db_name = db_config.get("mysql_db_name")


db_connection = mycon.connect(
  host=mysql_db_address,
  user=mysql_db_username,
  password=mysql_db_password,
)

command = f"""
        DROP DATABASE {mysql_db_name}
        """
cursor = db_connection.cursor()
cursor.execute(command)
db_connection.commit()
cursor.close()
db_connection.close()