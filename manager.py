from flask import Flask, request ,render_template ,make_response ,jsonify
import json
import redis

app = Flask(__name__)

# r = redis.StrictRedis(host="**********", port=6379, db=0)
pool = redis.ConnectionPool(decode_responses=True, host="*******", port=6379, db=3)
r = redis.Redis(connection_pool=pool)


@app.route("/add/")
def add():
    return render_template('add.html')

@app.route("/upload/", methods=["POST"])
def upload():
    client_s = int(request.values.get('client_score', 0))
    if client_s < 0:
        resp = make_response(jsonify({"message": "添加失败", "code": 400}))
        return resp
    client_n = request.values.get('client_number', '')
    if not client_n:
        resp = make_response(jsonify({"message": "请输入参数", "code": 400}))
        return resp

    ok = r.zadd(name='ranking',mapping={client_n:client_s})
    if ok ==1:
        resp = make_response(jsonify({"message": "添加成功", "code": 200}))
        resp.set_cookie('username',client_n)
    elif ok == 0:
        resp = make_response(jsonify({"message": "更新成功", "code": 200}))
        resp.set_cookie('username',client_n)
    return resp

@app.route("/show/", methods=["POST"])
def show():
    username = request.cookies.get('username')
    start_id = int(request.values.get('start_id', ''))
    end_id = int(request.values.get('end_id', ''))
    if not start_id or not end_id:
        return json.dumps({"message": "请输入正确参数",'code':400})
    data = r.zrange(name='ranking',start=start_id-1,end=end_id-1,withscores=True,score_cast_func=int,desc=True)
    data = [{'name':n,'val':v} for n,v in data]
    rank = r.zrevrank('ranking',username)
    source = r.zscore('ranking',username)
    jsondata = json.dumps({"message": "查询成功", "data": data,'rank':int(rank) + 1,'username':username,'source':int(source)})
    return jsondata

if __name__ == '__main__':
    app.run()
