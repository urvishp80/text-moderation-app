from src.profane_moderation import profane_detection
from flask import Flask
from flask_restful import Resource, Api, reqparse
import config as cf
from  pathlib import Path
class TextModeration(Resource):
    def __init__(self,BERT_Processor,BERT_Transformer,modelWeightPath: str,thresh: float,preloadModel: bool=True) -> None:
        super().__init__()
        self.PD = profane_detection(BERT_Processor,BERT_Transformer,modelWeightPath,thresh)
        if preloadModel:
            self.PD.load_model()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text",type= str, location='args', required=True)
        text = parser.parse_args()['text']
        if len(text) > cf.Minimimum_length:
            profane_score,profane_req = self.PD.isModerationRequire(text)
            return {
                    "StatusCode": 200,
                    "ModerationRequire":profane_req,
                    "scores":[str(profane_score)]
                }
        else:
            return {
                    "StatusCode": 200,
                    "Response": "Invalida Text ( Require minimum Text length 5)"
                }
    def post(self):
        pass


class TextModeration_preload(Resource):
    def __init__(self,model) -> None:
        super().__init__()
        self.PD = model
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text",type= str, location='args', required=True)
        text = parser.parse_args()['text']
        if len(text) > cf.Minimimum_length:
            profane_score,profane_req = self.PD.isModerationRequire(text)
            return {
                    "StatusCode": 200,
                    "ModerationRequire":profane_req,
                    "scores":[str(profane_score)]
                }
        else:
            return {
                    "StatusCode": 200,
                    "Response": "Invalida Text ( Require minimum Text length 5)"
                }
    def post(self):
        pass


if __name__ == "__main__":
    # Model Load EveryTime
    # parent_path = Path(__file__).parent.absolute()
    # bert_parent_path = parent_path.joinpath(cf.BERT_MODEL_PARENT)
    # myapp = Flask("Text Moderation")
    # api = Api(myapp)
    # arguments = {
    #     "BERT_processor":str(bert_parent_path.joinpath(cf.BERT_PROCESSOR)),
    #     "BERT_transformer":str(bert_parent_path.joinpath(cf.BERT_TRANSFORMER)), 
    #     "modelWeighPath":cf.profane_Model_Path,"thresh":cf.profane_thresh}
    # api.add_resource(TextModeration,"/index",resource_class_args = arguments.values())
    # myapp.run()

    # Model Load in main (not load every request)
    parent_path = Path(__file__).parent.absolute()
    bert_parent_path = parent_path.joinpath(cf.BERT_MODEL_PARENT)
    arguments = {
        "BERT_processor":str(bert_parent_path.joinpath(cf.BERT_PROCESSOR)),
        "BERT_transformer":str(bert_parent_path.joinpath(cf.BERT_TRANSFORMER)), 
        "modelWeighPath":cf.profane_Model_Path,"thresh":cf.profane_thresh}
    model = profane_detection(arguments["BERT_processor"],arguments["BERT_transformer"],arguments["modelWeighPath"],arguments["thresh"])
    myapp = Flask("Text Moderation")
    api = Api(myapp)
    api.add_resource(TextModeration_preload,"/index",resource_class_args = [model])
    myapp.run()
