if __name__ == '__main__':
    from profane_moderation import Model
else:
    from .profane_moderation import Model
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text

if __name__ == "__main__":
    from utils import preprocess_text
else:
    from .utils import preprocess_text


class spamDetection(Model):
    def __init__(self, BERT_processor, BERT_transformer, modelWeighPath, thresh) -> None:
        super().__init__(modelWeighPath)
        self.threshold = thresh
        self.BERT_processor = BERT_processor
        self.BERT_transformer = BERT_transformer

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
            pred = self.model.predict([text["Text"]])
            return pred
        except Exception as e:
            print(e)
            return [-1]

    # Override Method for create model
    def create_model(self):
        bert_preprocessor = hub.KerasLayer(self.BERT_processor)
        bert_encoder = hub.KerasLayer(self.BERT_transformer)
        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='Inputs')
        preprocessed_text = bert_preprocessor(text_input)
        embeed = bert_encoder(preprocessed_text)
        dropout = tf.keras.layers.Dropout(0.1, name='Dropout')(embeed['pooled_output'])
        outputs = tf.keras.layers.Dense(1, activation='sigmoid', name='Dense')(dropout)
        # creating final model
        model = tf.keras.Model(inputs=[text_input], outputs=[outputs])
        return model

    def isModerationRequire(self, input: str) -> list:
        try:
            pred = super().make_prediction(input)
            if pred[0] != -1:
                pred_score = pred[0][0]
                if pred_score > self.threshold:
                    return [pred_score, True]
                else:
                    return [pred_score, False]
            else:
                return [-1, False]
        except Exception as e:
            print(e)
            return [-1, False]


if __name__ == "__main__":
    # Spam Model weight Path
    spam_Model_weight_Path = r'A:\CJ_Work\Text-Moderation\text-moderation-app\weights\spam model weights\spam weight'
    # Spam Model Threshold
    Spam_thresh = 0.5
    # Spam Mode Path
    bert_preprocessor = r"A:\CJ_Personal\Upwork\Text Moderation\Programming\Text-Moderation\models\Bert_model\Preprocessor"
    bert_transformer = r"A:\CJ_Personal\Upwork\Text Moderation\Programming\Text-Moderation\models\Bert_model\bert_en_uncased_L-12_H-768_A-12_4"
    SD = spamDetection(bert_preprocessor, bert_transformer, spam_Model_weight_Path, Spam_thresh)
    print(SD.isModerationRequire("Hello world"))
