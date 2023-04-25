from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/getisfact/', methods=['GET'])
def respond():
    # Retrieve the name from the url parameter /getmsg/?name=
    # name = request.args.get("name", None)

    # For debugging
    # print(f"Received: {name}")

    # response = {}

    # Check if the user sent a name at all
    # if not name:
    #     response["ERROR"] = "No name found. Please send a name."
    # # Check if the user entered a number
    # elif str(name).isdigit():
    #     response["ERROR"] = "The name can't be numeric. Please send a string."
    # else:
    #     response["MESSAGE"] = f"Welcome {name} to our awesome API!"
    response = jsonify({'message': 'This is 99& facts!'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    # Return the response in json format
    return response

@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to OTT Fact Checker!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)