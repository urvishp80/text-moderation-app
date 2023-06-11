# Text Moderation App

## Project Setup:
1. Clone Repository
2. Download the BERT Model and Model Weights from [here](https://drive.google.com/drive/folders/1OtgUWcQxecRx-fJr2BefIjywVuV9othy?usp=drive_link)
3. Paste both the folders (i.e., models, weights) in the root directory.
4. Install the dependencies using following command:  
   `pip install -r requirements.txt`
5. Run the with `python app.py`
6. Send the request on `http://127.0.0.1:5000/index` 
   1. GET Request:  
        :param text: input text for moderation detection
        i.e., `http://127.0.0.1:5000/index?text="your input text"`

   2. POST Request: with JSON body  
         :param **userID**: default '12121' - can be configured from `config.py` file  
         :param **token**: default 'abc123abc123abc' - can be configured from `config.py` file  
         :param **text**: 'your input text'  
   - Set the key `Content-Type` : `application/json` in request Headers
   ```
   {
       "userID": "12121",
       "token" : "abc123abc123abc",
       "text"  : "Let's go on a dinner date. My friend owns a sea-facing restaurant."
   }
   ```
7. You should receive a successful response such as:  
   ```
   {
       "StatusCode": 200, 
       "Response": {
           "Spam_moderation_Require": spam_req,
           "Spam_moderation_score": str(spam_score),
           "Profane_moderation_require": profane_req,
           "Profane_moderation_score": str(profane_score)
           }
   }
    ```
   