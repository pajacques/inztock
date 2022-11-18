from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from datetime import datetime
import json
import random
import secrets

app = Flask('FinTechExplained WebServer')
CORS(app)

sessionIds = {}
subscriptions = {}
record_per_page = 10

with open('./data/subscription.json') as f:
    data = f.read()

subscriptions={}
if len(data) > 0:
    subscriptions = json.loads(data)

@app.route('/')
def get_data():
    return "Yahoo, en route vers InZtock"


@app.route('/ping', methods=['POST', 'GET'])
def ping():
    return {
        "message": "Server heartbeat operation",
        "data": None,
        "response": {"code": 200, "description": 'OK'}
    }


@app.route('/login', methods=['POST'])
def login():
    try:
        print(request)
        if request.is_json:
            print('Is JSON format')
        else:
            print('is NOT JSON format')
        variable_name = request.get_json(force=True)
        email = variable_name['email']
        password = variable_name['password']
        if email in subscriptions and subscriptions[email] == password:
            session = [session[0] for session in sessionIds.items() if session[1]["email"] == email]
            if len(session) == 1:
                session_id = session[0]
            else:
                session_id = secrets.token_urlsafe()
                sessionIds[session_id] = {"email": email, "last_log_in": datetime.now(), "name": "Stephanie",
                                          "last_name": "Rodriguez"}
            return {
                "message": "Logged successfully",
                "data": {"session_id": session_id},
                "response": {"code": 200, "description": 'OK'}
            }
        else:
            print('#10')
            return {
                       "message": "Invalid credential",
                       "data": None,
                       "response": {"code": 401, "description": "Unauthorized"}
                   }, 401
    except Exception as e:
        print(str(e))
        return {
                   "message": "Something went wrong",
                   "data": None,
                   "response": {"code": 500, "description": str(e)}
               }, 500


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if "session_id" in request.headers:
        print('#1')
        session_id = request.headers.get('session_id')
        print('#2', session_id)
        if session_id not in sessionIds:
            return {
                       "message": "Invalid Authentication token",
                       "data": None,
                       "response": {"code": 401, "description": "Unauthorized"}
                   }, 401
        else:
            sessionIds[session_id] = None
            return {
                "message": "Logout successfully",
                "data": None,
                "response":  {"code": 200, "description": "OK"}
            }
    else:
        return {
                   "message": "Authentication Token is missing",
                   "data": None,
                   "response": {"code": 401, "description": "Unauthorized"}
               }, 401


@app.route('/subscribe', methods=['POST'])
def subscribe():
    variable_name = request.get_json(force=True)
    email = variable_name['email']
    password = variable_name['password']
    if email in subscriptions:
        return {
                   "message": "Account already exists",
                   "data": None,
                   "response": {"code": 401, "description": "Unauthorized"}
               }, 401
    else:
        subscriptions[email] = password
        with open('./data/subscription.json', 'w') as f:
            json.dump(subscriptions, f)
        return {
            "message": "Subscription created successfully",
            "data": None,
            "response": {"code": 200, "description": "OK"}
        }


@app.route('/success/<name>')
def success(name):
    return '' % name


@app.route('/info/<id>', methods=['GET'])
def info(id):
    return {"item_full_description": "PA-0009173;;connecteurs à compression emt 1  "
                                     "c15810-It;3;Connecteur;Électrique;;C - VERT;FRAEMP-14101 - FRANKLIN EMPIRE;01 - "
                                     "MM3-A13-R05;;",
            "general": {"subscription_date": "2000-01-05"},
            "contact": {"id": 10009, "company": "TransQuebec", "title": "Warehouse manager",
                        "fullname": "Stephanie Bolduc",
                        "phone": "+1 (418) 774-9876",
                        "address": {"street": "1478 du Breton",
                                    "state": "Québec", "country": "Canada", "box": "F9F 9D9"}},
            "last_update": "2022-11-08",
            "similar": [{"id": "12345",
                         "item_full_description": "PA-0009175;;connecteurs à compression emt 2 po "
                                                  "c15816-It;2;Connecteur;Électrique;;C - VERT;FRAEMP-14101 - FRANKLIN "
                                                  "EMPIRE;01 - MM3-A13-R05;;"}],
            "carrier": [{"id": 1245, "name": "Purolator", "address": {"street": "555 du Cap",
                                                                      "state": "Québec", "country": "Canada",
                                                                      "box": "F9F 181"}, "phone": "(418) 789-5568",
                         "shipping_description": "ship within 2 business days"},
                        {"id": 8741, "name": "FedEx", "address": {"street": "666 du Gilbert",
                                                                  "state": "Québec", "country": "Canada",
                                                                  "box": "F9F 181"},
                         "phone": "(418) 777-9987",
                         "shipping_description": "ship within 4-5 business days"}
                        ]}


@app.route('/search')
def search():
    query = request.args.get('q')
    start = request.args.get('start', default=0, type=int)
    qid = request.args.get('qid')
    f = open('./data/results.json')
    data = json.load(f)
    last_index_of_page = min(len(data["results"]) - start, record_per_page)
    results = data["results"][start:start + last_index_of_page]
    page = 0 if len(results) == 0 else int(start / record_per_page) + 1
    return {"results": 16, "page": page, "results": results}


@app.route('/isearch')
def isearch():
    query = request.args.get('q')
    f = open('./data/results.json')
    data = json.load(f)
    results = data["results"]
    # results = random.sample(results, 6)
    results = sorted(results, key=lambda x: x["id"])
    return {"results": results}


@app.route('/save', methods=['POST'])
def save():
    variable_name = request.get_json()
    key_variable = variable_name['name']
    auth = request.headers.get('Authorization')
    return 'save.... %s' % auth

# @app.route('/save', methods = ['POST'])
# def search():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name=user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name=user))
