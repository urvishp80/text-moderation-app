# CV based Profile Moderation

## Project Setup:
1. Clone Repository
2. Download the BERT Model and model weight from this link -> https://drive.google.com/drive/folders/1OtgUWcQxecRx-fJr2BefIjywVuV9othy?usp=drive_link
3. Moev the folders inside the main directory (where app.py file is located) 
4. Install Requirement using following command (pip install -r requirements.txt)
5. update the BERT Model and model weights paths in config file as per requirements.
6. Run the app.py will create a local server at 127.0.0.0:8000
7. send request on 127.0.0.0:8000/index
    GET Request:
      parameter: text: (input text for moderation detection)
      i.e 127.0.0.0:8000/index?text="input text"
    POST Request:
      parameter:
        UserId : defaule 12121 (you can update from config file)
        token  : default abc123abc123abc (you can update from config file)
        text   :'input Text'

        i.e Post request with body json {
          'UserID': 12121,
          'token' : 'abc123abc123abc',
          'text'  : 'Input Text'
        }
        please set content-type : application/json in request header
