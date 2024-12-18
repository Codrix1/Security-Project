from flask import Flask, request, jsonify
from flask_cors import CORS
from KEY import KEY
from AES import AES
import numpy as np

app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
    return "Welcome to the AES Testing Server!", 200

@app.route('/submit/<string:type>', methods=['POST'])
def handle_submit(type):
    try:
        data = request.get_json()
        print("Received payload:", data)  # Log the payload for debugging
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload."}), 400
        
        Text = data.get("text")
        Key = data.get("key")
        #input_type= data.get("base")
        print(f"text: {Text}, Key: {Key}")
        if type =="encryption":

            key_instance = KEY(Text)
            aes = AES(Key)
            ciphertext = aes.encrypt_block(key_instance)
            Steps =  aes.Steps 

        return jsonify(ciphertext , Steps ), 200
    except Exception as e:
        app.logger.error("Error processing request: %s", str(e))
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    # Run Flask development server for testing
    app.run(host='0.0.0.0', port=5000, debug=True)