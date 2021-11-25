from flask import Flask, jsonify, request
from get_related_video import GetRelatedVideos
from jwt_auth import JwtAuth
import json

app = Flask(__name__)   
app.config['JSON_AS_ASCII'] = False                          

@app.route('/')                                   
def hello_world():                                
    return "getSubtitle"
     
@app.route("/get_related_videoid", methods=["POST"])
def get_related_videoid():
    """
    {
        token: String,
        video_id
    }
    apikey = "AIzaSyB5ydOIa5tDNxvehwGnP7aLj_4e7CyyIBI"
    """
    token_and_videoid = json.loads(request.get_data().decode())
    ja = JwtAuth()
    decoded = ja.decode(token_and_videoid['token'])
    grv = GetRelatedVideos(token_and_videoid['video_id'], decoded['key'])

    
    video_and_url = grv.get_videoid_and_url()
    return jsonify({"status":200, "videoInfo": video_and_url})


                    

if __name__ == '__main__':                        
    app.run(host="0.0.0.0", port=5007, debug=True)