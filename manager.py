from flask import Flask, request ,render_template
from flask_sqlalchemy import SQLAlchemy
import json, os
class Config:
    SECRET_KEY = "wfsdgagasdfsafd"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "mydata.db")


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Config)

class Client_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_number = db.Column(db.String(20), unique=True)
    client_score = db.Column(db.Integer, default=0)

@app.route("/add/")
def add():
    return render_template('add.html')



@app.route("/search/")
def search():
    return render_template('search.html')


@app.route("/show/", methods=["POST"])
def show():
    # request_data = json.loads(request.get_data().decode("utf-8"))
    # start_id = request_data.get('start_id')
    # end_id = request_data.get('end_id')
    start_id = request.values.get('start_id', '')
    end_id = request.values.get('end_id', '')
    client_model = Client_Model.query.order_by(Client_Model.client_score.desc()).offset(start_id).limit(end_id).all()
    data = {}
    for i in client_model:
        subdata = {}
        subdata[client_model.client_number] = client_model.client_score
        data[i] = subdata
    jsondata = json.dumps({"message": "success", "code": data})
    return jsondata


@app.route("/upload/", methods=["POST"])
def upload():
    # request_data = json.loads(request.get_data().decode("utf-8"))
    # client_number = request_data.get("client_number")
    # client_score = request_data.get("client_score")
    client_s = int(request.values.get('client_score', 0))
    client_n = request.values.get('client_number', '')
    client_model = Client_Model.query.filter_by(client_number=client_n).first()
    if client_model:
        client_model.client_score = client_s
    else:
        client_model = Client_Model(client_number=client_n, client_score=client_s)
    print(client_model)

    db.session.add(client_model)
    db.session.commit()
    jsondata = json.dumps({"message": "success", "code": 200})
    return jsondata


if __name__ == '__main__':
    app.run()
