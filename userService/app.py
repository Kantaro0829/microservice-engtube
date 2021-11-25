from flask import Flask, jsonify, request
import json
from user_registry import UserLogin, UserRegistry 
from jwt_auth import JwtAuth
from sqlalchemy import exc, func    
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False                    

@app.route('/')                                   
def hello_world():                                
    return "userService"
@app.route("/new_user_reg", methods=["POST"])
def new_user_reg():
    '''app
    受け取るJSON : user_info[]
    {
        "password": String,
        "email": String,
        "api_key": String,
        "toeic_score": Int
    }

    '''
    print("##########################log of new_user_lrg###########################")
    user_info = json.loads(request.get_data().decode())
    print(user_info)

    #user table にレコードの追加
    try:
        ur = UserRegistry(user_info)
        dic_temp = ur.new_user_reg()
        jwt_auth = JwtAuth()
        #token生成
        token = jwt_auth.encode(dic_temp)
        print("token",token)
        temp = {
            "status": 200,
            "token": token
        }

        return jsonify(temp)
        
    except exc.SQLAlchemyError as e:
        message = None
        if type(e) is exc.IntegrityError:
            message = "メールアドレスがすでに登録されています"
            print(type(e))
            return jsonify({
                "status": 400,
                "message": message,
        })
        print(e)
        return jsonify({"status":401, "massage":"DBに問題あるかも"})

@app.route("/login", methods=["POST"])
def login():
    '''
    受け取るjson: user_info[]
    {
        "email": mail,
        "password": password
    }
    '''
    user_info = json.loads(request.get_data().decode())
    try:
        ul = UserLogin(user_info)
        id_and_apikey = ul.login()

        if id_and_apikey['id'] != 0:
            jwt_auth = JwtAuth()
            token = jwt_auth.encode(id_and_apikey)

            return jsonify({"status":200, "token":token})

        return jsonify({
            "status": 400,
            "message": "正しいメールアドレスまたはパスワードを入力してください"
        })
    except:
        return jsonify({
            "status": 400,
            "message": "db のエラー？"
        })

@app.route("/registry_toeic_score", methods=["POST"])
def registry_toeic_score():
    pass
    

if __name__ == '__main__':                        
    app.run(host="0.0.0.0", port=5000, debug=True)