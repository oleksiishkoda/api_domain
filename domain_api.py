from flask import Flask, jsonify, request, abort, make_response
import json, re


app = Flask(__name__)

def isValidDomain(domain):
    regex = "^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}$"
    pattern = re.compile(regex)
    if domain != None and re.search(pattern, domain):
        return True
    return False

def read_file():
    with open("config.json", "r") as f:
        data = json.load(f)
    return data

def write_file(data):
    with open("config.json", "w") as f:
        json.dump(data, f)

@app.errorhandler(400)
def invalid_domain(error):
    return make_response(jsonify({'error': 'Invalid domain'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/domains/', methods=['GET', 'POST', 'DELETE'])
def get_post_domains():
    data = read_file()
    if request.method == 'POST':
        if not isValidDomain(request.json.get("url")):
            abort(400)
        new_domain = request.json
        if len(data["domains"])>0:
            new_domain["id"] = data["domains"][-1]["id"]+1
        else:
            new_domain["id"] = 1
        data["domains"].append(new_domain)
        write_file(data)
    if request.method == 'DELETE':
        data["domains"].clear()
        write_file(data)
    return jsonify(data)

@app.route('/api/domains/<int:domain_id>', methods=['GET', 'DELETE'])
def get_one_domain(domain_id):
    data = read_file()
    domain = {}
    for dom in data["domains"]:
        if dom["id"] == domain_id:
            domain = dom
    if len(domain) == 0:
        abort(404)
    if request.method == 'GET':
        return jsonify({"domain": domain})
    if request.method == 'DELETE':
        data["domains"].remove(domain)
        write_file(data)
        return jsonify({'result': f'Domain {domain["name"]} has been deleted!'})

@app.route('/api/domains/<int:domain_id>', methods=['PUT'])
def update_domain(domain_id):
    if not isValidDomain(request.json.get("url")):
        abort(400)
    data = read_file()
    for dom in data["domains"]:
        if dom["id"] == domain_id:
            dom['name'] = request.json.get('name', dom['name'])
            dom['url'] = request.json.get('url', dom['url'])
    write_file(data)
    return jsonify({"result":"Domain has been updated!"})
        

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)