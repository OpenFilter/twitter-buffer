import sys
import requests
import json
import config


class TwitterBuffer(object):

    def __init__(self, api_host=config.API_HOST, api_port=config.API_PORT):
        self.api_host=api_host
        self.api_port=api_port

    def create_stream(self, stream_dict):
        return self.perform_post('streams/', stream_dict)

    def record(self, stream_name, command):
        data = {
            'stream_name': stream_name,
            'command': command
        }
        return self.perform_post('streams/recorder/', data)

    def get_stream_tweets(self, stream_name, since_id=None, max_id=None, count=config.TWEETS_PER_PAGE):
        params = {
            since_id: since_id,
            max_id: max_id,
            count: count
        }
        return self.perform_get('streams/%s/tweets' % stream_name, params)

    def perform_get(self, resource, params={}):
        response = None
        sys.stderr.write('Getting: ' + self.endpoint(resource) + '\n')
        r = requests.get(self.endpoint(resource), params=params)
        if r.status_code == 200:
            response = r.json()
        return response 

    def perform_post(self, resource, data):
        response = None
        data_json =  json.dumps(data)
        sys.stderr.write('Posting: ' +  resource + ' Data: ' + data_json)
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.endpoint(resource), data_json, headers=headers)
        if r.status_code == 200:
            response = r.json()
        return response

    def perform_put(self, resource, data):
        response = None
        data_json =  json.dumps(data)
        sys.stderr.write('Puting: ' +  resource + ' Data: ' + data_json)
        headers = {'Content-Type': 'application/json'}
        r = requests.put(self.endpoint(resource), data_json, headers=headers)
        if r.status_code == 200:
            response = r.json()
        return response

    def endpoint(self, resource):
        return 'http://%s:%d/%s' % (self.api_host, self.api_port, resource)

