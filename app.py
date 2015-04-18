import os
from flask import Flask, request
import requests
import json

app = Flask(__name__)

SLACK_ENDPOINT_URL = os.environ.get('SLACK_ENDPOINT_URL')
GOOGLE_MAPS_ENDPOINT_URL = 'http://maps.googleapis.com/maps/api/staticmap'


def generate_payload_from_request(request):
    if request.args.get('location'):  # Yo location
        coordinate = request.args.get('location').replace(';', ',')
        params_dict = {
            'center': coordinate,
            'zoom': '14',
            'format': 'png',
            'sensor': 'false',
            'size': '640x640',
            'maptype': 'roadmap',
            'markers': coordinate
        }
        url_params = generate_url_params_from_dictionary(params_dict)
        text = GOOGLE_MAPS_ENDPOINT_URL + url_params
    elif request.args.get('link'):  # Yo link
        text = request.args.get('link')
    else:  # Ordinary Yo
        text = 'Yo'

    return {
        'text': text,
        'username': request.args.get('username')
    }


def generate_url_params_from_dictionary(params):
    return '?' + '&'.join([key + '=' + value for key, value in params.items()])


@app.route('/')
def index():
    headers = {'content-type': 'application/json'}
    payload = generate_payload_from_request(request)
    data = json.dumps(payload)
    requests.post(SLACK_ENDPOINT_URL, data=data, headers=headers)

    return 'Yo'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(port=port)
