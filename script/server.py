from flask import Flask, request
import zipfile
import os
import json

app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB limit
user_data_json_path = '../user.json'

def read_json(path:str) -> json:
    with open(path, 'r') as f:
        f_str = f.read()
    return(json.loads(f_str))

def get_folder_name(user_name:str) -> tuple[str, int]: 
    user_json = read_json(user_data_json_path)
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
    personal_information_json = read_json(personal_information_json_path) 
    user_name = personal_information_json['profile_user'][0]['string_map_data']['Username']['value']
    if user_entry(user_name, filename) == 200:
        return 'File uploaded successfully', 200
    else:
        return 'Data entry side error'

def user_entry(user_name:str, folder_name:str) -> int:
    user_json = read_json(user_data_json_path)
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
        following_json_path = f'{folder_path}/connections/followers_and_following/following.json'
        followers_json_path = f'{folder_path}/connections/followers_and_following/followers_1.json'
        following_json = read_json(following_json_path)
        followers_json = read_json(followers_json_path)
        following_set = set()
        followers_set = set()
        for i in following_json['relationships_following']:
            following_set.add(i['string_list_data'][0]['value'])
        for i in followers_json:
            followers_set.add(i['string_list_data'][0]['value'])
        return {'feature-1':list(following_set - followers_set)}, 200
    else:
        return folder_name, 200
    

@app.route('/feature-2', methods=['POST'])
def get_feature_2(): # Feature-2 --> List the pending request ids
    user_name = request.form.get('user_name')
    folder_name, response_code = get_folder_name(user_name)
    if response_code == 200:
        folder_path = f'../data/{folder_name}'
        pending_follow_request_json_path = f'{folder_path}/connections/followers_and_following/pending_follow_requests.json'
        pending_follow_request_json = read_json(pending_follow_request_json_path)
        pending_follow_request_ids = []
        for i in pending_follow_request_json['relationships_follow_requests_sent']:
            pending_follow_request_ids.append(i['string_list_data'][0]['value'])
        return {'feature-2': pending_follow_request_ids}, 200
    else:
        return folder_name, 200
    

@app.route('/feature-3', methods=['POST'])
def get_feature_3(): # Feature-3 --> List the people who are all removed from user in suggestion
    user_name = request.form.get('user_name')
    folder_name, response_code = get_folder_name(user_name)
    if response_code == 200:
        folder_path = f'../data/{folder_name}'
        removed_suggestions_json_path = f'{folder_path}/connections/followers_and_following/removed_suggestions.json'
        removed_suggestions_json = read_json(removed_suggestions_json_path)
        removed_suggestions_ids = []
        for i in removed_suggestions_json['relationships_dismissed_suggested_users']:
            removed_suggestions_ids.append(i['string_list_data'][0]['value'])
        return {'feature-3': removed_suggestions_ids}, 200
    else:
        return folder_name, 200


if __name__ == "__main__":
    app.run(debug=True)
