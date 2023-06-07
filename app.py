from src.profane_moderation import profane_detection
from src.spam_moderation import spamDetection
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import config as cf
from  pathlib import Path
class TextModeration(Resource):
    def __init__(self,BERT_Processor,BERT_Transformer,Profane_modelWeightPath: str,
                 profane_thresh: float,spam_model_weightPath,spam_thresh,preloadModel: bool=False) -> None:
        super().__init__()
        self.PD = profane_detection(BERT_Processor,BERT_Transformer,Profane_modelWeightPath,profane_thresh)
        self.SD = spamDetection(BERT_Processor,BERT_Transformer,spam_model_weightPath,spam_thresh)
        if preloadModel:
            self.PD.load_model()
            self.SD.load_model()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text",type= str, location='args', required=True)
        text = parser.parse_args()['text']
        if len(text) > cf.Minimimum_length:
            profane_score,profane_req = self.PD.isModerationRequire(text)
            spam_score, spam_req = self.SD.isModerationRequire(text)
            return {
                "StatusCode": 200,
                "Response":{
                    "Spam_moderation_Require":spam_req,
                    "Spam_moderation_score":spam_score,
                    "Profane_moderaion_require":profane_req,
                    "Profane_moderation_score":profane_score
                    }
                }
        else:
            return {
                    "StatusCode": 200,
                    "Response": "Invalida Text ( Require minimum Text length 5)"
                }
    def post(self):
        post_data = request.get_json()
        keys = ["userID","token","text"]
        for i in keys:
            if i not in post_data.keys():
                return{
                    "StatusCode": 404,
                    "Response": "invalid Parameter"
                }
        userID = post_data["userID"]
        token = post_data["token"]
        text = post_data["text"]
        if userID == cf.USERID and token == cf.TOKEN:
            if len(text) > cf.Minimimum_length:
                profane_score,profane_req = self.PD.isModerationRequire(text)
                spam_score, spam_req = self.SD.isModerationRequire(text)
                return {
                    "StatusCode": 200,
                    "Response":{
                        "Spam_moderation_Require":spam_req,
                        "Spam_moderation_score":str(spam_score),
                        "Profane_moderaion_require":profane_req,
                        "Profane_moderation_score":str(profane_score)
                        }
                    }
            else:
                return {
                        "StatusCode": 200,
                        "Response": "Invalida Text ( Require minimum Text length 5)"
                    }
        else:
            return {
                    "StatusCode": 200,
                    "Response": "Invalida credentials details"
                }



class TextModeration_preload(Resource):
    def __init__(self,PD_model,SD_model) -> None:
        super().__init__()
        self.PD = PD_model
        self.SD = SD_model
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text",type= str, location='args', required=True)
        text = parser.parse_args()['text']
        if len(text) > cf.Minimimum_length:
            profane_score,profane_req = self.PD.isModerationRequire(text)
            spam_score, spam_req = self.SD.isModerationRequire(text)
            return {
                "StatusCode": 200,
                "Response":{
                    "Spam_moderation_Require":spam_req,
                    "Spam_moderation_score":str(spam_score),
                    "Profane_moderaion_require":profane_req,
                    "Profane_moderation_score":str(profane_score)
                    }
                }
        else:
            return {
                    "StatusCode": 200,
                    "Response": "Invalida Text ( Require minimum Text length 5)"
                }
    def post(self):
        post_data = request.get_json()
        keys = ["userID","token","text"]
        for i in keys:
            if i not in post_data.keys():
                return{
                    "StatusCode": 404,
                    "Response": "invalid Parameter"
                }
        userID = post_data["userID"]
        token = post_data["token"]
        text = post_data["text"]
        if userID == cf.USERID and token == cf.TOKEN:
            if len(text) > cf.Minimimum_length:
                profane_score,profane_req = self.PD.isModerationRequire(text)
                spam_score, spam_req = self.SD.isModerationRequire(text)
                return {
                    "StatusCode": 200,
                    "Response":{
                        "Spam_moderation_Require":spam_req,
                        "Spam_moderation_score":str(spam_score),
                        "Profane_moderaion_require":profane_req,
                        "Profane_moderation_score":str(profane_score)
                        }
                    }
            else:
                return {
                        "StatusCode": 200,
                        "Response": "Invalida Text ( Require minimum Text length 5)"
                    }
        else:
            return {
                    "StatusCode": 200,
                    "Response": "Invalida credentials details"
                }

                        
        print(post_data)


if __name__ == "__main__":
    # Model Load EveryTime
    parent_path = Path(__file__).parent.absolute()
    bert_parent_path = parent_path.joinpath(cf.BERT_MODEL_PARENT)
    myapp = Flask("Text Moderation")
    api = Api(myapp)
    arguments = {
        "BERT_processor":str(bert_parent_path.joinpath(cf.BERT_PROCESSOR)),
        "BERT_transformer":str(bert_parent_path.joinpath(cf.BERT_TRANSFORMER)), 
        "Profane_modelWeightPath":cf.PROFANE_MODEL_WEIGHT_PATH,
        "profane_thresh":cf.PROFANE_THRESHHOLD,
        "spam_model_weightPath":cf.SPAM_MODEL_WEIGHT_PATH,
        "spam_thresh":cf.SPAM_THRESHHOLD
        }
    api.add_resource(TextModeration,"/index",resource_class_args = arguments.values())
    myapp.run()

    # Model Load in main (not load every request)
    # parent_path = Path(__file__).parent.absolute()
    # bert_parent_path = parent_path.joinpath(cf.BERT_MODEL_PARENT)
    # arguments = {
    #     "BERT_processor":str(bert_parent_path.joinpath(cf.BERT_PROCESSOR)),
    #     "BERT_transformer":str(bert_parent_path.joinpath(cf.BERT_TRANSFORMER)), 
    #     "Profane_modelWeightPath":cf.PROFANE_MODEL_WEIGHT_PATH,
    #     "profane_thresh":cf.PROFANE_THRESHHOLD,
    #     "spam_model_weightPath":cf.SPAM_MODEL_WEIGHT_PATH,
    #     "spam_thresh":cf.SPAM_THRESHHOLD
    #     }
    # PD_model = profane_detection(arguments["BERT_processor"],
    #                           arguments["BERT_transformer"],
    #                           arguments["Profane_modelWeightPath"],
    #                           arguments["profane_thresh"])
    # SD_model = spamDetection(arguments["BERT_processor"],
    #                           arguments["BERT_transformer"],
    #                           arguments["spam_model_weightPath"],
    #                           arguments["spam_thresh"])    
    # myapp = Flask("Text Moderation")
    # api = Api(myapp)
    # api.add_resource(TextModeration_preload,"/index",resource_class_args = [PD_model,SD_model])
    # myapp.run()
