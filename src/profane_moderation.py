if __name__ == "__main__":
    from Utils import preprocess_text
else:    
    from .Utils import preprocess_text


from pathlib import Path
from abc import abstractmethod,ABC
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text

class Model(ABC):
    def __init__(self,modelWeightPath) -> None:
        self.modelWeightPath = modelWeightPath
        self.model = None
        self.isModelLoad = False
    @abstractmethod        
    def creat_model(self):
        raise NotImplementedError
    def load_model(self):
        try:
            if not self.model and not self.isModelLoad:
                self.model = self.creat_model()
                self.model.load_weights(self.modelWeightPath)
                self.isModelLoad = True
        except Exception as e:
            self.isModelLoad = False
            raise e
    
    def make_prediction(self,input: str) -> list:
        try:
            if not self.isModelLoad:
                self.load_model()
            text = preprocess_text(input)
            pred = self.model.predict([text["Text"]])
            return pred
        except Exception as e:
            print(e)
            return [-1]







class profane_detection(Model):
    def __init__(self,BERT_processor,BERT_transformer,modelWeighPath,thresh) -> None:
        super().__init__(modelWeighPath)
        self.threshhold = thresh
        self.BERT_processor = BERT_processor
        self.BERT_transformer = BERT_transformer        
    
    # Override Methon for create model
    def creat_model(self):
        bert_preprocessor = hub.KerasLayer(self.BERT_processor)
        bert_encoder = hub.KerasLayer(self.BERT_transformer)
        text_input = tf.keras.layers.Input(shape = (), dtype = tf.string, name = 'Inputs')
        preprocessed_text = bert_preprocessor(text_input)
        embeed = bert_encoder(preprocessed_text)
        dropout = tf.keras.layers.Dropout(0.1, name = 'Dropout')(embeed['pooled_output'])
        outputs = tf.keras.layers.Dense(1, activation = 'sigmoid', name = 'Dense')(dropout)
        # creating final model
        model = tf.keras.Model(inputs = [text_input], outputs = [outputs])
        return model
    
    def isModerationRequire(self,input: str) -> list:
        try:
            pred = super().make_prediction(input)
            if pred[0] != -1:
                pred_score = pred[0][0]
                if pred_score > self.threshhold:
                    return [pred_score,True]
                else:
                    return [pred_score,False]
            else:
                return [-1, False]
        except Exception as e:
            print(e)
            return [-1,False]


if __name__ == "__main__":
    
    
    # Profane Model Path
    profane_Model_Path = r"A:\CJ_Personal\Upwork\Text Moderation\Programming\Text-Moderation\profane_model_weight"
    #Profane Model Threshhold
    profane_thresh = 0.5

    #profane Model Path
    bert_preprocessor = r"A:\CJ_Personal\Upwork\Text Moderation\Programming\Text-Moderation\models\Bert_model\Preprocessor"
    bert_transformer = r"A:\CJ_Personal\Upwork\Text Moderation\Programming\Text-Moderation\models\Bert_model\bert_en_uncased_L-12_H-768_A-12_4"
    profane = profane_detection(bert_preprocessor,bert_transformer,profane_Model_Path,profane_thresh)
    print(profane.isModerationRequire("Hello world"))