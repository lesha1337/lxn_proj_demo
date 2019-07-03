import requests;
import json;
import sys

files = sys.argv[1].replace('>f+++++++++ ', '').split(' ')
camera_id = sys.argv[2] #array insted of string

file_names = [camera_id + '/' + files[i] for i in range(len(files))]

try:
    r = requests.post('http://0.0.0.0:10228/render_new_video/', data=json.dumps({'data': file_names, 'id': camera_id}))
except Exception as e:
    print('>>>', e)