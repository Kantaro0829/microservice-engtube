from schema import Schema, And, Use, Optional, SchemaError

class MongoSchema():
    def __init__(self):
        self.instertting_data_schema = Schema(
            [{'score': And(Use(int)), 'eng': And(str, len), 'jp': And(str, len)}]
        )
        self.messaged_data_schema = Schema(
            {
                'score': And(Use(int)),
                'data':[
                    {'eng': And(str, len),'jp': And(str, len)}
                ]
            }
        )
    def check_data_to_insert(self, data_to_insert):
        isValidated = self.instertting_data_schema.is_valid(data_to_insert)
        return isValidated

    def check_data_messaged(self, messaged_data):
        isValidated = self.messaged_data_schema.is_valid(messaged_data)
        return isValidated