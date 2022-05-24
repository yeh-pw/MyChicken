from flask import *
from flask_jwt_extended import *
from db_dal import YehPW_UAS_DB_Service
from flask_cors import CORS
import yaml

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "MWD-UAS Kelompok YehezkielPW MegaB JoseB"
app.config["SECRET_KEY"] = "MWD-UAS Kelompok YehezkielPW MegaB JoseB"

CORS(app)
jwt = JWTManager(app)

with open(r'./db_config.yaml') as file:
    db_config = yaml.load(file, Loader=yaml.FullLoader)

mysql_db_address = db_config.get("mysql_db_address")
mysql_db_username = db_config.get("mysql_db_username")
mysql_db_password = db_config.get("mysql_password")
mysql_db_name = db_config.get("mysql_db_name")
file.close()


db_service = YehPW_UAS_DB_Service(
    mysql_db_address, mysql_db_username, mysql_db_password, mysql_db_name)

# Authn & Authz


@app.route('/login', methods=["POST"])
def login():
    log = request.json
    id = log["id"]
    pw = log["password"]
    check = db_service.validation(id, pw)
    if check == None:
        message = "ID Not Exist"
        return jsonify(error=message)
    elif check == False:
        message = "Wrong Password"
        return jsonify(error=message)
    else:
        token = create_access_token(identity={
            "id": check["id"],
            "role": check["role"]
        })
        return jsonify(access_token=token, id=check["id"], role=check["role"])


@app.route('/get_products')
def get_products():
    products = db_service.get_products()
    return jsonify(products)


@app.route("/post_invoice", methods=["POST"])
def post_invoice():
    data = request.json
    total = data["total"]
    db_service.post_invoice(total)
    return jsonify(status="success")


@app.route("/post_solds", methods=["POST"])
def post_solds():
    data = request.json
    print(data)
    for x in data:
        print(x)
        product_name = x['makanan']
        solds_quantity = x['qty']
        product_price = x['harga']
        sub_total = x['sub_tot']
        db_service.post_solds(product_name,solds_quantity,product_price,sub_total)
    return jsonify(status="success")


if __name__ == '__main__':
    app.run(debug=True)
