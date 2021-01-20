from flask import Flask, redirect
from flask import request
from flask import Response
import json
import os


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
    't-content': input_url,
    'status': 1
    })   

    if index < 5:
        pass
    else:
        data["teleport-clipboard"].pop(0)

        for x in data["teleport-clipboard"]:
            x["id"] -= 1        

    #json_file.close()

    with open('teleport.json', 'w+') as outfile:
        json.dump(data, outfile)

    outfile.close()

    if request.headers.get('Teleport-Sequence') == 'b70cb0151b08596a6349e3887fb4a2e465b1d4730fa9e5874061d2c04ba92514':
        return Response(status=200)
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

@app.route('/teleport/clipboard/update/id=<int:input_id>')
def teleportClipboardUpdate(input_id):
    
    try:
        #Open telport clipboard file
        with open('teleport.json') as json_file:
            data = json.load(json_file)

        data["teleport-clipboard"][input_id]["status"] -= 1

        with open('teleport.json', 'w+') as outfile:
            json.dump(data, outfile)

        outfile.close()
        json_file.close()
    
    except:
        pass

    return data

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8088)))