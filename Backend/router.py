from flask import Flask, request, jsonify
from flask_cors import CORS
from KEY import KEY
from AES import AES
import numpy as np

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'



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
        if type =="Encryption":

            key_instance = KEY(Key)
            aes = AES(Text , "")
            ciphertext = aes.encrypt_block(key_instance)
            Steps =  aes.Steps 
        print("Data Sent") 
        print(Steps)
        return jsonify({"ciphertext": ciphertext, "Steps": Steps}), 200
    except Exception as e:
        app.logger.error("Error processing request: %s", str(e))
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    # Run Flask development server for testing
    app.run(host='0.0.0.0', port=5000, debug=True)
