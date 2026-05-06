from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary storage
items = []

# GET API
@app.route('/depots', methods=['GET'])
def get_items():
    return jsonify(items)

# POST API
@app.route('/depots', methods=['POST'])
def add_item():
    data = request.json
    items.append(data)
    return jsonify(data)
# post method to write down the rules for the given tasks 

# Start server
if __name__ == '__main__':
    app.run(debug=True)
server.add_init_function(lambda: print("Server is starting..."))
