from flask import *
from flask_cors import CORS
from pathlib import *

app = Flask(__name__)
CORS(app)

@app.route("/get_image/<image_name>")
def get_image(image_name):
    path = f"./images/{image_name}.png"
    return send_file(path,mimetype="image/png")

@app.route("/delete_image/<image_name>")
def delete_image(image_name):
    path = Path(f"./images/{image_name}.png")
    path.unlink()
    return jsonify("Deleted")

# @app.route("/add_image/<image_name>")
# @app.route("/update_image/<image_name>")

if __name__ == '__main__':
    app.run(debug=True)
