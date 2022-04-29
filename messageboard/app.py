from tracemalloc import start
from flask import *
import yaml
import boto3
import botocore
from database import pool

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = yaml.safe_load(open('./messageboard/secret.yaml'))
s3_bucket = db["s3_bucket_name"]
s3_key = db["access-key-id"]
s3_secret = db["s3_secret"]
app.secret_key = db["mysecret"]


s3 = boto3.client(
    "s3",
    aws_access_key_id=s3_key,
    aws_secret_access_key=s3_secret
)


class handle_message:
    def save_message(self, text, img_url):
        try:
            cnx = pool.get_connection()
            cur = cnx.cursor(dictionary=True)
            cur.execute(
                "INSERT INTO messageboard(word, image) VALUES (%s, %s)", (text, img_url,))
            cnx.commit()
            message_id = cur.lastrowid
            session["message_id"] = message_id
            data = jsonify({
                "ok": True
            })
            return data, 200
        except:
            data = jsonify({"error": True,
                            "message": "內部問題"
                            })
            return data, 500
        finally:
            cur.close()
            cnx.close()

    def load_message(self):
        try:
            cnx = pool.get_connection()
            cur = cnx.cursor(dictionary=True)
            client_message_id = session["message_id"]
            cur.execute(
                "SELECT word, image FROM messageboard WHERE id=%s", (client_message_id,))
            message_info = cur.fetchone()
            data = jsonify({"data": message_info})
            return data, 200
        except:
            data = jsonify({"error": True,
                            "message": "內部問題"
                            })
            return data, 500

        finally:
            cur.close()
            cnx.close()

    def load_messageboard_data(self):
        try:
            startdata = 0
            perpage = 12
            cnx = pool.get_connection()
            cur = cnx.cursor(dictionary=True)

            cur.execute("SELECT COUNT(*) FROM messageboard")
            dataQty = cur.fetchone()
            Qty = dataQty["COUNT(*)"]

            cur.execute(
                "SELECT word, image FROM messageboard Limit %s, %s;", (startdata, perpage))
            message_info = cur.fetchall()
            data = jsonify({"data": message_info,
                            "count": Qty})
            return data, 200
        except:
            data = jsonify({"error": True,
                            "message": "內部問題"
                            })
            return data, 500

        finally:
            cur.close()
            cnx.close()


handle_message = handle_message()


@app.route("/")
def myhome():
    return render_template("index.html")


@app.route("/file/upload", methods=["POST"])
def upload_file():
    client_file = request.files["file"]
    file_name = request.form["fileName"]
    client_message = request.form["message"]
    try:
        s3.upload_fileobj(client_file, s3_bucket, file_name,
                          ExtraArgs={"ContentType": "image/jpeg"})
        img_url = "https://my-message-board.s3.amazonaws.com/%s" % (file_name)

    except:
        return "error"
    return handle_message.save_message(client_message, img_url)


@app.route("/file/upload", methods=["GET"])
def load_file():
    return handle_message.load_message()


@app.route("/file/load", methods=["GET"])
def load_messageboard():
    return handle_message.load_messageboard_data()


app.run(host='0.0.0.0', port=4000)
