from flask import Flask, request, jsonify
import json  
from get_meaning import GetMeaning                    
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
import json                         

@app.route('/')                                   
def hello_world():                                
    return "getMeaning" 

@app.route("/get_meaning", methods=["POST"])
#@cross_origin(supports_credentials=True)
def get_meaning():
    """
    受け取るJson
    {
        token: String,
        data: [apple, lemon]
    }
    """
    token_and_data = json.loads(request.get_data().decode())
    gm = GetMeaning(token_and_data['data'])

    result_list, failure_list = gm.scrape_from_weblio()
    return jsonify({
        "status": 200,
        "data": result_list,
        "failure": failure_list
    })
if __name__ == '__main__':                        
    app.run(host="0.0.0.0", port=5002, debug=True)