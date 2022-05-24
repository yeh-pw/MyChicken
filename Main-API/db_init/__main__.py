from db_init.db_init_script import YehPW_UAS_DB_Init
import yaml

with open(r'./db_config.yaml') as file:
    db_config = yaml.load(file, Loader=yaml.FullLoader)

mysql_db_address = db_config.get("mysql_db_address")
mysql_db_username = db_config.get("mysql_db_username")
mysql_db_password = db_config.get("mysql_password")
mysql_db_name = db_config.get("mysql_db_name")

if __name__ == "__main__":
    db = YehPW_UAS_DB_Init(
        mysql_db_address, mysql_db_username, mysql_db_password, mysql_db_name)
    db.init()
