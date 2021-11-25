#from _typeshed import Self
from sqlalchemy.engine import engine_from_config
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import user
from setting import session# セッション変数の取得
from user import *# Userモデルの取得
import hashlib#ハッシュ化用
import datetime

class WordService():
    def __init__(self, id):
        self.id = id
        self.watched_day = datetime.date.today()
    
    def word_registry(self, video_id, eng_and_jp):

        count = len(eng_and_jp)# 登録したい単語の数
        for i in eng_and_jp:
            words = Words()
            words.id = self.id
            words.video_id = video_id
            words.day = self.watched_day
            words.english = i['eng']
            words.japanese = i['jp']

            session.add(words)#データ登録
            session.flush()

            count = count - 1
        session.commit()#コミット

        if count == 0:
            return true
        
        return false
    
    def get_all_words(self):
        words = Words()

        all_eng_and_jp = session.query(Words.english, Words.japanese).\
            filter(Words.id == self.id).\
                all()

        print(all_eng_and_jp)
        print("userId === ", self.id)

        session.close()
        data_list = []
        for i in all_eng_and_jp:
            word_dic = {}
            word_dic['eng'] = i[0]
            word_dic['jp'] = i[1]
            data_list.append(word_dic)

        print("送るListの中身：", data_list)

        return data_list
    
    #tupleからlistに変更する関数
    def tuple_to_list(self, list):

        data_list = []
        print(list)
        for i in list:
            print(i)
            word_dic = {}
            word_dic['eng'] = i[0]
            word_dic['jp'] = i[1]
            print(word_dic)
            data_list.append(word_dic)
        
        return data_list
    
    def get_words_group_by_videoid(self):
        words = Words()

        all_video_id = session.query(Words.video_id).\
            filter(Words.id == self.id).\
                group_by(Words.video_id).\
                        all()
        
        print(all_video_id)
        
        data_list = []

        for id in all_video_id:
            temp_dic ={}
            eng_and_jp_list = session.query(Words.english, Words.japanese, Words.video_id).\
                filter(Words.id == self.id, Words.video_id == id[0]).\
                    all()
            """
            videoid 追加必要
            [
                {
                    videoId: STring,
                    data: [
                    ]
                },
                {
                    videoId: STring,
                    data: [
                    ]
                },
            ]
            """
            temp_dic['videoId'] = eng_and_jp_list[0][2]
            #print("videoID:###########", temp_dic["videoId"])
            temp_dic["word"] = self.tuple_to_list(eng_and_jp_list)
            data_list.append(temp_dic)
            
        print(data_list)

        return data_list

class ToeicService():
    def __init__(self, id, score):
        self.id = id
        self.score = score

    def get_score_level(self):
        
        if self.score > 800:
            return 8
        elif self.score > 700:
            return 7
        elif self.score > 600:
            return 6
        elif self.score > 500:
            return 5
        else:
            return 4
    
    def score_reg(self, level):
        tf = Toeic_info()
        tf.id = self.id
        tf.score = self.score
        tf.level = level

        session.add(tf)
        session.flush()
        session.commit()
        print("登録完了")
        print("id=", tf.id, "score=", tf.score, "level=", tf.level)
        session.close()

        return true
        
