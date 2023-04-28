from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route("/check-fact", methods=['POST'])
def ask():
    reqJson = request.get_json()
    print(reqJson)
    print("Page url: " + reqJson['pageUrl'])
    print(reqJson['factList'])
    print(reqJson['factList'][0])
    sampleDict = {
        "success": "true",
        "hotel": "trivago",
        "pageUrl": reqJson['pageUrl']
    }
    return jsonify(sampleDict)


if __name__ == '__main__':
    print("Running app on port 8080...")
    from waitress import serve
    serve(app, host="127.0.0.1", port=8080)
