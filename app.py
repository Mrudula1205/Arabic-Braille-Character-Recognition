from flask import Flask, render_template, url_for, request, jsonify
import base64, classify
import os, io, base64, random, json
from io import BytesIO
from PIL import Image
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

#credentials = CognitiveServicesCredentials(os.environ['arabic_api_key'])
#char_client = ComputerVisionClient(os.environ['arabic_api_endpoint'], credentials= credentials)


app = Flask(__name__)

def load_braille_data():
    with open('braille_data.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/game')
def game():
    braille_data = load_braille_data()
    braille_character = random.choice(braille_data['braille_images'])
    image_path = braille_character['image_path']
    correct_tag = braille_character['tag']
    return render_template('game.html', image_path=url_for('static', filename="Image/"+image_path), correct_tag=correct_tag)

@app.route('/evaluate', methods=['POST', 'GET'])
def evaluate():
    try:
        # Get the JSON data from the request
        data = request.get_json()
    
        image_data = data.get('image_data')
        correct_tag = data.get('correct_tag')
   
        # Decode the image data
        image_data = image_data.split(',')[1]  # Remove the data URL part
        image_data = base64.b64decode(image_data)

        # Convert the image data to an image object
        image = Image.open(BytesIO(image_data))

        # Save image to binary stream
        image_binary = BytesIO()
        image.save(image_binary, format='PNG')
        image_binary.seek(0)

        # Perform your evaluation here (replace classify.classify_image with your function)
        predicted_letter = classify.classify_image(image_binary)  # Ensure classify_image is defined

        # Return the result
        if predicted_letter == correct_tag:
            return jsonify({"result": "correct"})
        else:
            return jsonify({"result": "incorrect"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)