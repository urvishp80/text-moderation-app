"""
Utils function for data preprocessing and model inferences

@author 
"""
import pandas as pd
from nltk.corpus import stopwords
import string



def remove_html_tags_special_character(col: str) -> str:
    tags_list = ['<p>', '</p>', '<p*>',
                 '<ul>', '</ul>',
                 '<li>', '</li>',
                 '<br>',
                 '<strong>', '</strong>',
                 '<span*>', '</span>',
                 '<a href*>', '</a>',
                 '<em>', '</em>', '<br>', '<br />', '<div>', '</div>', '\\n', '~']
    for tag in tags_list:
        col.replace(tag, '')
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

