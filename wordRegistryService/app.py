from flask import Flask, jsonify, request
from sqlalchemy.sql.functions import register_function
from jwt_auth import JwtAuth  
from word_registry import WordService
import json
import pika


app = Flask(__name__)   
app.config['JSON_AS_ASCII'] = False                          

@app.route('/')                                   
def hello_world():                                
    return "wordReristry"

@app.route("/word_registry", methods=["POST"])
def word_registry():
    """
    {
        token: String,
        date: date,
        video_id: string,
        data:[
            {"eng": string, "jp": string}, 
        ]
    }
    """
    token_and_data = json.loads(request.get_data().decode())
    print("token_and_data: ", token_and_data)

    ja = JwtAuth()
    decoded = ja.decode(token_and_data['token'])
    ws = WordService(decoded['id'])
    print("token data の中身:",token_and_data['data'])
    result = ws.word_registry(token_and_data['video_id'], token_and_data['data'])
    message = {}
    message['score'] = decoded['score']
    message['data'] = token_and_data['data']

    print("送るJson：", message)
    string_message = json.dumps(message, indent=2, ensure_ascii=False)
    print(string_message)
    print(type(string_message))




    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq"))
    # チャンネルの確立
    channel = connection.channel()
    # メッセージを格納するためのキュー(task_queue)を作成
    channel.queue_declare(queue="task_queue", durable=True)
    # メッセージをキュー(task_queue)に格納
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=string_message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # メッセージの永続化
        ))
    # 接続のクローズ及びメッセージが配信されたことを確認
    connection.close()




    if result:
        return jsonify({"status": 200, "message": "登録成功"})
    
    return jsonify({"status": 400, "message": "登録失敗"})  

@app.route("/get_word_by_videoid", methods=["POST"])
def get_word_by_videoid():
    """
    {
        token: String
    }
    """
    token = json.loads(request.get_data().decode())
    ja = JwtAuth()
    decoded = ja.decode(token['token'])
    ws = WordService(decoded['id'])
    #result = ws.get_all_words()
    result = ws.get_words_group_by_videoid()
    print(result)
    if result:
        return jsonify({"status":200, "data":result}) 
    return jsonify({"status": 400, "message":"取得失敗"}) 

@app.route("/get_all_words", methods=["POST"])
def get_all_words():
    """
    {
        token: String
    }
    """
    token = json.loads(request.get_data().decode())
    ja = JwtAuth()
    decoded = ja.decode(token['token'])
    ws = WordService(decoded['id'])
    result = ws.get_all_words()
    if result:
        return jsonify({"status":200, "data":result})
    return jsonify({"status":400, "message":"取得しっぱい"})

                 

if __name__ == '__main__':                        
    app.run(host="0.0.0.0", port=5004, debug=True)