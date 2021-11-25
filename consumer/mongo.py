from pymongo import MongoClient, results
import datetime
from schema_check import MongoSchema

def get_mongo():
    mongo_client = MongoClient('api_mongo', 27017)
    mongo_client['admin'].authenticate("root","password")
    return mongo_client

class RegistryData():
    def __init__(self):
        self.client = get_mongo()
        self.db = self.client['test-database']
        self.posts = self.db.posts
        self.schema = MongoSchema()

    def parse_messaged_data(self, messaged_data):
        """
        messaged_data
        これを整形
        {
           "score": 0,
           "data": [
             {"eng": "english","jp": "英語"},
             {"eng": "japanese","jp": "日本語"}
           ]
        }

        to

        [{"score":Int, "eng":String, "jp":String},,,,,]

        """
        data_list =[]
        for i in messaged_data['data']:
            temp_dic = {}
            temp_dic['score'] = messaged_data['score']
            temp_dic['eng'] = i['eng']
            temp_dic['jp'] = i['jp']
            data_list.append(temp_dic)

        return data_list

    def insert_one(self, messaged_data):
        print("!!!!!!!!!!!!!!!!!!!!!!!!",messaged_data)
        if self.schema.check_data_messaged(messaged_data):
            parsed_data = self.parse_messaged_data(messaged_data)
        
        if self.schema.check_data_to_insert(parsed_data):
            result = self.posts.insert_many(parsed_data)
        
        if not result.acknowledged:
            print("登録失敗")
        
        print("確認",result.acknowledged)
        return result