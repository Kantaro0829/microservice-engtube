from flask import Flask                           
app = Flask(__name__)   
app.config['JSON_AS_ASCII'] = False                          

@app.route('/')                                   
def hello_world():                                
    return "get audio"                         

if __name__ == '__main__':                        
    app.run(host="0.0.0.0", port=5003, debug=True)