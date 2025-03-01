from flask import Flask, request
import zipfile
import os
import json

app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB limit
user_data_json_path = '../user.json'

def get_folder_name(user_name:str) -> tuple[str, int]: 
    with open(user_data_json_path, 'r') as f:
        f_str = f.read()
    user_json = json.loads(f_str)
    if user_name in user_json:
        return user_json[user_name], 200
    else:
        return 'Zip file not uploaded', 400

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename[:-4]
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(f'../data/{filename}')
    personal_information_json_path = f'../data/{filename}/personal_information/personal_information/personal_information.json'
    with open(personal_information_json_path, 'r') as f:
        f_str = f.read()
    personal_information_json = json.loads(f_str) 
    user_name = personal_information_json['profile_user'][0]['string_map_data']['Username']['value']
    if user_entry(user_name, filename) == 200:
        return 'File uploaded successfully', 200
    else:
        return 'Data entry side error'

def user_entry(user_name:str, folder_name:str) -> int:
    with open(user_data_json_path, 'r') as f:
        f_str = f.read()
    user_json = json.loads(f_str)
    user_json[user_name] = folder_name
    with open(user_data_json_path, 'w') as f:
        json.dump(user_json, f)
    return 200

@app.route('/feature-1', methods=['POST'])
def get_feature_1(): # Feature-1 --> List the people who are all not following back user
    user_name = request.form.get('user_name')
    folder_name, response_code = get_folder_name(user_name)
    if response_code == 200:
        folder_path = f'../data/{folder_name}'
        
        pass
    else:
        return folder_name, 200


if __name__ == "__main__":
    app.run(debug=True)
