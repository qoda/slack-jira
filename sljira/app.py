import json

from bottle import Bottle, run, response, request

app = Bottle()


@app.route('/')
def jira():
    user_name = request.forms.get("user_name")
    args = request.forms.get("text").split(" ")
    response.content_type = "application/json"
    return json.dumps({
        "response_type": "in_channel",
        "text": "%s" % (user_name, " ".join(args))
    })


run(app, host="0.0.0.0'", port=5001)
