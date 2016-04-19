#!/usr/bin/env python

import optparse
import json

from bottle import Bottle, run, response, request
from jira import JIRA

from sljira import commands, db


app = Bottle()
keyvalstore = db.KeyValStore()


JIRA_HOST = None


@app.post('/')
def jira():
    user_name = request.forms.get("user_name")
    user_id = request.forms.get("user_id")
    args = request.forms.get("text").split(" ")

    response_data = {
        "response_type": "in_channel",
        "text": ""
    }
    response.content_type = "application/json"

    # ensure a command has been issued
    try:
        command = args[0]
        function_args = args[1:]
    except IndexError:
        response_data["text"] = "You may need help: `/jira help`"
        return json.dumps(response_data)

    # create user if login command is issued
    if command == "login":
        jira_username = keyvalstore.set(
            "%s_username" % (user_id), function_args[0]
        )
        jira_password = keyvalstore.set(
            "%s_password" % (user_id), function_args[1]
        )
        response_data["text"] = "You have successfully logged in"
        return json.dumps(response_data)

    else:
        jira_username = keyvalstore.get("%s_username" % user_id)
        jira_password = keyvalstore.get("%s_password" % user_id)

    if jira_username and jira_password:
        jira = JIRA(JIRA_HOST, basic_auth=(jira_username, jira_password))

        function = getattr(commands, command, None)
        if function:
            response_data["text"] = function(jira, *function_args)
        else:
            response_data["text"] = "Command _%s_ doesn't exist" % (command)

    else:
        response_data["text"] = "Please login to continue: `/jira login \
                                <username> <password>`"

    return json.dumps(response_data)


if __name__ == "__main__":

    # parse through the system argumants
    usage = "Usage: %prog [options] jirahost"
    parser = optparse.OptionParser()

    options, args = parser.parse_args()

    # ensure the query argument has been passed, else fail
    try:
        JIRA_HOST = args[0]
    except IndexError:
        exit(usage)

    run(app, host="0.0.0.0", port=5001)
