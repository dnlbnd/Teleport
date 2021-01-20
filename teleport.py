from flask import Flask, redirect
from flask import request
import json


app = Flask(__name__)
@app.route('/')
def default():
    return "Working..."

@app.route('/teleport/send/url=<path:input_url>')
def teleportSend(input_url):
    
    try:
        #Open telport clipboard file
        with open('teleport.json') as json_file:
            data = json.load(json_file)

    except: 
        data = {"teleport-clipboard": []}

    #get the number of objects in the clipboard for use when assigning ids
    index = len(data["teleport-clipboard"])

    data["teleport-clipboard"].append({
    'id': index,
    't-content': input_url
    })   

    if index < 5:
        pass
    else:
        data["teleport-clipboard"].pop(0)

        for x in data["teleport-clipboard"]:
            x["id"] -= 1        

    json_file.close()

    with open('teleport.json', 'w+') as outfile:
        json.dump(data, outfile)

    outfile.close()

    if request.headers.get('Teleport-Sequence') == 'b70cb0151b08596a6349e3887fb4a2e465b1d4730fa9e5874061d2c04ba92514':
        return data
    else:
        return 'Unauthorised Access.'

@app.route('/teleport/clipboard')
def teleportClipboard():

    try:
        #Open telport clipboard file
        with open('teleport.json') as json_file:
            data = json.load(json_file)
    except:
        pass

    return data

if __name__ == '__main__':
    app.run(debug=True)