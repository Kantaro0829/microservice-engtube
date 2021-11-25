#from _typeshed import Self
from sqlalchemy.engine import engine_from_config
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import user
from setting import session# セッション変数の取得
from user import *# Userモデルの取得
import hashlib#ハッシュ化用
import datetime

class UserRegistry():

    def __init__(self, user_info):
        self.password = hashlib.sha256(user_info['password'].encode()).hexdigest()
        self.mail = user_info["email"]
        self.api_key = user_info["api_key"]
        self.dic = {}

    def new_user_reg(self):
        user = User()
        user.mail = self.mail
        user.api_key = self.api_key
        user.password = self.password

        session.add(user)#データ登録
        session.flush()
        session.commit()#コミット
        #自動で生成されたID
        id = user.id
        key = user.api_key
        session.close

        self.dic = {"id": id, "key":key}
        return self.dic
    
    def update_user(self):
        pass

class UserLogin():
    def __init__(self, user_info):
        self.password = hashlib.sha256(user_info['password'].encode()).hexdigest()
        self.mail = user_info['email']
        self.dic = {}
    
    def login(self):
        user = User()

        #このメールアドレスのパスワードを抽出
        auth_pass = session.query(User.password).\
            filter(User.mail == self.mail).\
                one()

        print(auth_pass[0], "は", self.mail, "のパスワード！！")

        #パスワード比較
        if self.password == auth_pass[0]:
            
            id = session.query(User.id).\
                    filter(User.mail == self.mail).\
                        one()
            
            key = session.query(User.api_key).\
                    filter(User.id == id[0]).\
                        one()
                        
            score = session.query(User.score).\
                        filter(User.id == id[0]).\
                            one()

            print("id: ", id[0])
            print("apiKey: ", key[0])
            print("toeic_score: ", score[0])

            self.dic = {"id": id[0], "key": key[0], "score": score[0]}
            print("encode 前の状態：", self.dic)

            session.close

            return self.dic
        
        else:
            self.dic = {"id": 0}
            return self.dic