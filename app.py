import os
import requests
from bottle import route, post, run, abort, static_file, redirect, request

current_path = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(current_path, 'static')

@route("/")
def hello_world():
    return static_file('enghouse.html', root=static_path)

@route("/UihrciyWuERWuomBzHnpyt")
def serve_form():
    return static_file('form.html', root=static_path)

@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=static_path)

@route('/.well-known/acme-challenge/<filepath:path>')
def serve_static2(filepath):
    return """fSHu9WGZjlVWLgZxdwdPqhLFOupBm5g0n0XCNkz5D5A.816jpOxBpafSbLnQc2hx-1fpOGFg_uMIvHrTRKHgP9g"""

@post("/join/")
def join_session():
    # lookup session based on pincode
    # redirect to sessionurl
    pincode = request.forms.get('sessionid')
    security = request.forms.get('sec')
    if security != "UihrciyWuERWuomBzHnpyt":
        return abort(403, "Forbidden")
    r = requests.get('https://api.surfly.com/v2/sessions/?api_key=b89956927c6349908b9f2405324462f7&active_session=true')
    for session in r.json():
        if session['pin'] == pincode:
            return redirect(session['viewer_link'])
    return abort(404, "Session not found")

run(server='gunicorn', host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
