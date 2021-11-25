from flask import Flask, jsonify, request
from get_subtitle import GetSubtitle
import json

app = Flask(__name__)   
app.config['JSON_AS_ASCII'] = False                          

@app.route('/')                                   
def hello_world():                                
    return "getSubtitle"     

@app.route("/get_subtittle", methods=["POST"])
def get_subtittle():
    """
    {
        token: String,
        video_id: String
    }
    """
    subtittle = ""
    token_and_videoid = json.loads(request.get_data().decode())
    gs = GetSubtitle(token_and_videoid["video_id"])

    try:
        subtittle = gs.get_normal_subtitle()
    except:
        subtittle = gs.get_autogenerated_subtitle()
    
    return jsonify({
        "status": 200,
        "subtittle": subtittle
    })
                    

if __name__ == '__main__':                        
    app.run(host="0.0.0.0", port=5001, debug=True)