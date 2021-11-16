import requests, json, os
from flask import Flask, request

import logging; log = logging.getLogger(__name__)
DEBUG=log.debug; INFO=log.info; WARN=log.warning; ERROR=log.error

app = Flask(__name__)

# stored as a secret in ocp...
SECRET = os.environ['SECRET']

loaded_configurations = None

@app.route('/build-notification', methods=['POST'])
def build_notification():
    request_data = request.get_json()
    
    # authorization, this should be improved.
    # For now a hardcoded secret will do.
    secret = request_data['secret']
    if (secret != SECRET):
        return ('not authorized', 404)

    # if payload is not as expected
    if not _process_incoming_data(request_data, request.path):
        return ("error processing incoming data", 500)

    # processing
    _process_new_image_event_for(
        eventid=request_data['eventid'],
        event=request_data['event'],
        pipeline=request_data['pipeline'],
        namespace=request_data['namespace']
        )

    return ("ok", 200) 

def _load_manifest():
    """
    Loads manifest file
    """
    with open('manifest.json') as json_file:
        return json.load(json_file)

def _load_attr_fqn(fqn):
    """
    Loads mandatory attributes for FQN from manifest file
    """
    for n in loaded_configurations["routes"]:
        if n["fqn"] == fqn:
            return n["attributes"]

def _process_incoming_data(request_data, fqn):
    """
    Sanity check if expected keys defined for the requested FQN are there based on the 
        manifest file
    """
    expected_attr = _load_attr_fqn(fqn)
    a = []
    for k in request_data.keys():
        a.append(k)
    if all (k in a for k in expected_attr):
        return True
    return False

def _get_event_listener_url_for(event, pipeline, namespace):
    """
    Gets the URL from the manifest file for the loaded configuration
    """
    for n in loaded_configurations["event_listeners"]:
        if ((n["event"] == event) and (n["namespace"] == namespace) and (n["pipeline"] == pipeline)):
            return n["url"]

def _process_new_image_event_for(event, eventid, pipeline, namespace):
    """
    Performs the actual request to the OCP event listener
    """
    payload = {"eventid" : eventid, "event" : event, "namespace" : namespace, "pipeline": pipeline}
    headers = {'Content-Type': 'application/json'}
    url = _get_event_listener_url_for(event, pipeline, namespace)
    return requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    loaded_configurations = _load_manifest()
    app.run(host="0.0.0.0", debug=True, use_reloader=True, port=5000)