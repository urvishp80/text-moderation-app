if __name__ == "__main__":
    from utils import preprocess_text
else:
    from .utils import preprocess_text


from abc import abstractmethod, ABC
from transformers import BertTokenizer,TFBertForSequenceClassification
from loguru import logger
import numpy as np


class Model(ABC):
    def __init__(self, modelWeightPath, TokenizerPath) -> None:
        self.modelWeightPath = modelWeightPath
        self.model = None
        self.isModelLoad = False
        self.tokenizer = BertTokenizer.from_pretrained(TokenizerPath)

    @abstractmethod
    def create_model(self, preTrained_ModelPath: str):
        raise NotImplementedError

    def load_model(self):
        try:
            if not self.model and not self.isModelLoad:
                self.model = self.create_model()
                self.model.load_weights(self.modelWeightPath)
                self.isModelLoad = True
        except Exception as e:
            self.isModelLoad = False
            raise e

    def make_prediction(self, input: str) -> list:
        try:
            if not self.isModelLoad:
                self.load_model()
            text = preprocess_text(input)
            encoding = self.tokenizer.encode_plus(
            text['Text'],
            add_special_tokens=True,
            max_length=100,
            return_token_type_ids=False,
            pad_to_max_length=True,
            return_attention_mask=True,
            )
            pred = self.model.predict([encoding['input_ids'],encoding['attention_mask']])
            return pred
        except Exception as e:
            logger.error(e)
            return [[-1]]


class profane_detection(Model):
    def __init__(self,TokenizerPath, modelWeighPath,Bert_pretrain_path) -> None:
        super().__init__(modelWeighPath, TokenizerPath)
        
        self.preTrained_ModelPath = Bert_pretrain_path
    # Override Method for create model
    def create_model(self):
        model = TFBertForSequenceClassification.from_pretrained(self.preTrained_ModelPath)
        return model

    def isModerationRequire(self, input: str) -> list:
        try:
            pred_score = super().make_prediction(input)
            pred = np.argmax(pred_score[0], axis=1)
            if pred[0] != -1:
                if pred[0] == 1 and pred[1] == 1:
                    return [1, True]
                else:
                    return [0, False]
            else:
                return [-1, False]
        except Exception as e:
            logger.error(e)
            return [-1, False]

