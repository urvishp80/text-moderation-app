"""
Utils function for datapreprocessing and model inferences

@author 
"""
import pandas as pd
from nltk.corpus import stopwords
import string
import tensorflow as tf
import tensorflow_text
import numpy as np


def remove_html_tags_special_character(col: str) -> str:
    tags_list = ['<p>' ,'</p>' , '<p*>',
                 '<ul>','</ul>',
                 '<li>','</li>',
                 '<br>',
                 '<strong>','</strong>',
                 '<span*>','</span>',
                 '<a href*>','</a>',
                 '<em>','</em>','<br>','<br />','<div>','</div>','\\n','~']
    for tag in tags_list:
        #col.replace(to_replace=tag,value='',regex=False,inplace=True)
        col.replace(tag,'')
    return col


def remove_punctuations(text: str):
    punctuations_list = string.punctuation
    temp = str.maketrans('', '', punctuations_list)
    text = str(text)
    return text.translate(temp)


def remove_stopwords(text: str):
    stop_words = stopwords.words('english')
 
    imp_words = []
 
    # Storing the important words
    for word in str(text).split():
        word = word.lower()
 
        if (word not in stop_words) and 'br' not in word:
            imp_words.append(word)
 
    output = " ".join(imp_words) 
    return output


def preprocess_text(text: str) -> dict:
    try:
        text = remove_html_tags_special_character(text)
        text = remove_punctuations(text)
        text = remove_stopwords(text)
        return {
            "StatusCode": 200,
            "Text": text
            }
    except Exception as e:
        print(e)

        return {
            "StatusCode": 500,
            "Text": ""
                }

def convert_model_to_tf(model_path,tf_model_path) -> bool:
    try:
        converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
        converter.target_spec.supported_ops = [
            tf.lite.OpsSet.TFLITE_BUILTINS,
            tf.lite.OpsSet.SELECT_TF_OPS
        ]
        converter._experimental_lower_tensor_list_ops = True
        converter.experimental_new_converter = True
        print(tf.lite.experimental.Analyzer(model_content = converter))
        tfliteModel =converter.convert()
        with open(tf_model_path,"wb") as file:
            file.write(tfliteModel)
        return True
    except FileNotFoundError as e:
        print("Please enter Valid Model Path!!!")
        print(e)
        return False
    except Exception as e:
        print(f"Error While Converting The mode File -> {e}")
    
def load_tflitemodel(path):
    interpreter = tf.lite.Interpreter(model_path=path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], np.array(["Hello world"]))
    interpreter.invoke()
    output_details = interpreter.get_tensor(output_details[-1]['index'])



if __name__ == "__main__":
    model_path = r"A:\CJ_Personal\Upwork\Text Moderation\Programming\Text-Moderation\models\profane_model"
    output_tflite_model_path = r"A:\CJ_Personal\Upwork\Text Moderation\Programming\Text-Moderation\models\profane_model\model.tflite"
    if convert_model_to_tf(model_path,output_tflite_model_path):
        print("Model Converted.")
    else:
        print("Error WHile Converting!!")
    #model = load_tflitemodel(output_tflite_model_path)