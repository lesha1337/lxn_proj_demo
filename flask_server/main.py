from flask import Flask, Response, request, send_from_directory, jsonify
from video_render.run_processing import get_barcode_time
from flask_cors import CORS, cross_origin
from process_video import process_video
import requests
import os.path
import json

video_path = '/lxn/data/' #slash at the end
node_add_url = 'http://backend:5000/api/videos/add_vid_from_flask'

app = Flask(__name__)

@app.route('/render_new_video/', methods=['POST'])
def init_render():
    print('INIT')
    data = request.get_data()
    dataDict = json.loads(data)
    print('>>>', dataDict)

    for fname in dataDict['data']:
        file_path = video_path+fname
        timeline = process_video(file_path)
        
        print('timeline >>>', timeline)
        headers = {'content-type': 'application/json'}
        data = json.dumps({'title': 'DOCKERdefaultTitle', 'timeData': timeline, 'video': file_path})
        requests.post(node_add_url, headers=headers, data=data)
    return '200'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='10228')