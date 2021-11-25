from flask import Flask, jsonify, request
import json          
from mongo import GetData               
app = Flask(__name__) 
app.config['JSON_AS_ASCII'] = False   
get_data = GetData()

@app.route('/')                                   
def hello_world():                                
    return "get rec0mmend word"    

@app.route("/get-all", methods=["GET"])
def get_all():
    result = get_data.get_all()
    print(f'get_all結果{result}')

    for doc in result:
        print(doc)

    temp = get_data.get_fillter_sample()
    print(f'get_fillter_sample結果{temp}')

    for doc in temp:
        print("##### filltered #####")
        print(doc)

    projection = get_data.get_projection()
    print(f'get_projection結果{projection}')

    for doc in projection:
        for doc in projection:
            print("!!!!!!!!!!!projection!!!!!!!!")
            print(doc)

    return jsonify({"status":200, "message": "成功"})


if __name__ == '__main__':                        
    app.run(host="0.0.0.0", port=5006, debug=True)