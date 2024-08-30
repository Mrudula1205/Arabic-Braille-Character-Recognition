from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

from msrest.authentication import CognitiveServicesCredentials
from io import BytesIO
from msrest.authentication import ApiKeyCredentials
import os

# Azure Custom Vision credentials
# retrieve environment variables

prediction_key = os.environ["VISION_PREDICTION_KEY"]
ENDPOINT = os.environ["VISION_TRAINING_ENDPOINT"]
project_id = '4c7bbaaa-2bc4-497a-bb4f-28e3ed79c4b6'
iteration_name = os.environ['VISION_ITERATION_NAME']

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

def classify_image(image_data):
    results = predictor.classify_image(project_id, iteration_name, image_data)
    # Parse the prediction result (e.g., highest probability)
    prediction = max(results.predictions, key=lambda x: x.probability)
    print("Hey3")
    return prediction.tag_name
