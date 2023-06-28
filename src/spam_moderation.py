if __name__ == '__main__':
    from profane_moderation import Model
else:
    from .profane_moderation import Model

from transformers import TFBertForSequenceClassification
import numpy as np    
from loguru import logger

class spamDetection(Model):
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


