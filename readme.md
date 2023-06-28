# Text Moderation App

## Project Setup:
1. Clone Repository
2. Download the BERT Model and Model Weights from [here](https://drive.google.com/drive/folders/18EDGBBVLvzaK17UqD-fEaqpsIHk00Dvt?usp=sharing)
3. Followe Below steps to paste the Downloaded model and weights.
   1. Paste the Models folder in Root directory
   2. create weights Directory in root directory
   3. paste dowloaded spam weights and profane weights directory in this weights directory.
4. Install the dependencies using following command:
   1. open python terminal in root directory
   2. run the following command  `pip install -r requirements.txt`
5. Run the command `python app.py` in the terminal (it will create local server at 127.0.0.1).
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

# Traninng The Model

## Use Training Notebook Directory to train spam and profane detection model

1. open the jupyter notebook
2. if you not installed require library yet, run the first cell to installed require library.
3. Config Cell
   1. set the training dataset file path
   2. set the Column index for input column and target column (i.e if column 1 use for input  text and column 2 represent spam or not spam then set INPUT_DATA_COLUMN_NAME as C1 and TARGET_DATA_COLUMN_NAME as C2 in notebook).
   3. if you want you can update the number of epochs and batch size else leave as default values
   4. set the weight location path (where trained model weights being stored).
4. run all other cell (model training will start and after model training finish it will save the weights of the model).
