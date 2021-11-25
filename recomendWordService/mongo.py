from pymongo import MongoClient, results, cursor

def get_mongo():
    mongo_client = MongoClient('api_mongo', 27017)
    mongo_client['admin'].authenticate("root","password")
    return mongo_client

class GetData():
    def __init__(self):
        self.client = get_mongo()
        self.db = self.client['test-database']
        self.posts = self.db.posts
    
    def get_all(self):
        data = self.posts.find()
        return data
    
    def get_fillter_sample(self):
        data = self.posts.find({"eng": "english"})
        return data

    #指定したcolumn をselect時に無視
    #{something:True of False} True でそれだけ抽出、falseは無視
    def get_projection(self):
        data = self.posts.find(
            filter={"score": 0},
            projection={'_id':False}
        )
        return data