from flask import Flask, request
import requests

app = Flask(__name__)

SECRET = "some-secret" # this is a test, the real one will be on ocp secrets...
EVENT_NEW_IMAGE = "new-image"

# expected payload
# {
#     "event" : "new-image",
#     "eventid" : "1234",
#     "namespace" : "rht-webapp-devel",
#     "secret" : "..."
# }

@app.route('/build-notification', methods=['POST'])
def build_notification():
    request_data = request.get_json()
    
    # authorization, this should be improved.
    # For now a hardcoded secret will do.
    secret = request_data['secret']
    if (secret != SECRET):
        return ('not authorized', 404)
    
    # if payload is not as expected
    if not _process_incoming_data(request_data):
        return ("error processing incoming data", 500)

    # processing
    event = request_data['event']
    if event == EVENT_NEW_IMAGE:
        _process_new_image_event()

    return ("ok", 200) 

def _process_incoming_data(request_data):
    try:
        event = request_data['event']
        eventid = request_data['eventid']
        namespace = request_data['namespace']
        # ...
    except(KeyError):
        return False
    return True

def _process_new_image_event():
    return requests.get('http://example.com').content

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_reloader=True, port=5000)