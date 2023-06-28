from src.profane_moderation import profane_detection
from src.spam_moderation import spamDetection
from src.utils import preprocess_text
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import config as cf
from pathlib import Path
from loguru import logger


class TextModeration_preload(Resource):
    def __init__(
            self,
            PD_model,
            SD_model
    ) -> None:

        super().__init__()

        self.PD = PD_model
        self.SD = SD_model

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text", type=str, location='args', required=True)
        text = parser.parse_args()['text']
        if len(text) > cf.MINIMUM_LENGTH:
            profane_score, profane_req = self.PD.isModerationRequire(text)
            spam_score, spam_req = self.SD.isModerationRequire(text)
            return {
                "StatusCode": 200,
                "Response": {
                    "Spam_moderation_Require": spam_req,
                    "Spam_moderation_score": str(spam_score),
                    "Profane_moderation_require": profane_req,
                    "Profane_moderation_score": str(profane_score)
                }
            }
        else:
            return {
                "StatusCode": 200,
                "Response": "Invalid Text (Require minimum Text length 5)"
            }

    def post(self):
        post_data = request.get_json()
        keys = ["userID", "token", "text"]
        for i in keys:
            if i not in post_data.keys():
                return {
                    "StatusCode": 404,
                    "Response": "invalid Parameter"
                }

        userID = str(post_data["userID"])
        token = str(post_data["token"])
        text = str(post_data["text"])

        if userID == cf.USERID and token == cf.TOKEN:

            if len(text) > cf.MINIMUM_LENGTH:
                
                logger.info(f"Preprocessing Input text ... ")
                prepOutPut = preprocess_text(text)
                if prepOutPut['StatusCode'] == 200:
                    logger.info(f"Running Profanity Moderation ... ")
                    profane_score, profane_req = self.PD.isModerationRequire(prepOutPut['Text'])

                    logger.info(f"Running Spam Moderation ... ")
                    spam_score, spam_req = self.SD.isModerationRequire(prepOutPut['Text'])

                    return {
                        "StatusCode": 200,
                        "Response": {
                            "Spam_moderation_Require": spam_req,
                            "Spam_moderation_score": str(spam_score),
                            "Profane_moderation_require": profane_req,
                            "Profane_moderation_score": str(profane_score)
                        }
                    }
                else:
                    return {
                    "StatusCode": 200,
                    "Response": "Invalid Text!!"
                }

            else:
                return {
                    "StatusCode": 200,
                    "Response": "Invalid Text (Require minimum Text length 5)"
                }
        else:
            return {
                "StatusCode": 200,
                "Response": "Invalid credentials details"
            }


if __name__ == "__main__":
    parent_path = Path(__file__).parent.absolute()
    arguments = {
        "BERT_Tokenizer":str(parent_path.joinpath(cf.BERT_TOKENIZER_PATH)),
        "BERT_preTrainedModel":str(parent_path.joinpath(cf.BERT_MODEL_PARENT)), 
        "Profane_modelWeightPath":str(parent_path.joinpath(cf.PROFANE_MODEL_WEIGHT_PATH)),
        "spam_model_weightPath":str(parent_path.joinpath(cf.SPAM_MODEL_WEIGHT_PATH))
        }
    PD_model = profane_detection(arguments["BERT_Tokenizer"],
                              arguments["Profane_modelWeightPath"],
                              arguments["BERT_preTrainedModel"])
    SD_model = spamDetection(arguments["BERT_Tokenizer"],
                              arguments["spam_model_weightPath"],
                              arguments["BERT_preTrainedModel"])    
    myapp = Flask("Text Moderation")
    api = Api(myapp)
    api.add_resource(TextModeration_preload,"/index",resource_class_args = [PD_model,SD_model])
    myapp.run()
