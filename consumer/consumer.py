import pika
import time
from pymongo import MongoClient, results
import datetime
import json




from flask import Flask, jsonify, make_response, request, abort

from flask_cors import CORS, cross_origin
from mongo import RegistryData

class Calc:
    def __init__ (self, a, b):
        self.a = a
        self.b = b
    
    def add(self):
        return self.a + self.b

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['JSON_AS_ASCII'] = False

time.sleep(30)

def get_mongo():
    mongo_client = MongoClient('api_mongo', 27017)
    mongo_client['admin'].authenticate("root","password")
    return mongo_client
def callback(channel, method, properties, body):
    print(f" [x] Received {body}")
    message = json.loads(body.decode())
    # message = body.decode()


    if message == "hey":
        print("hey there")
    elif message == "hello":
        print("well hello there")

        client = get_mongo()
        db = client['test-database']
        collection = db['test-collection']

        post = {"author": "Mike",
                "text": "My first blog post!",
                "tags": ["mongodb", "python", "pymongo"],
                "date": datetime.datetime.utcnow()}

        posts = db.posts
        post_id = posts.insert_one(post).inserted_id
        print(post_id)

    else:
        registry_data = RegistryData()
        result = registry_data.insert_one(message)
        print("success!!!!!!!!!!!!!結果：", result)
        
    

    print(" [x] Done")
    # 受信したことをキューに知らせる
    channel.basic_ack(delivery_tag=method.delivery_tag)

try:
    # 初期設定
    print(" [*] Connecting to server ...")
    # RabbitMQサーバと接続（ホスト名にはコンテナ名を指定しているが，Dockerを使ってない場合はIPアドレスを指定）
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq"))
    # チャンネルの確立
    channel = connection.channel()
    # メッセージを受信するためのキュー(task_queue)が存在することを確認
    channel.queue_declare(queue="task_queue", durable=True)
    # 前のメッセージの処理が完了してACKが返るまで次のメッセージを送信しないようにするオプション
    channel.basic_qos(prefetch_count=1)
    # キュー(task_queue)にcallback関数をサブスクライブしてメッセージ受信のたびに実行
    channel.basic_consume(queue="task_queue", on_message_callback=callback)
    print(" [*] Waiting for messages. To exit press Ctrl+C")
    channel.start_consuming()
except KeyboardInterrupt:
    print(" [x] Done")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5005, threaded=True, debug=True)

