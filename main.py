import requests
import os
from datetime import datetime

GENDER = 'male'
WEIGHT_KG = 80
HEIGHT_CM = 193
AGE = 21

APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
AUTH = os.environ['AUTH']

headers = {
   'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    'Authorization': AUTH,
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ["sheety_endpoint"]

user_response = {
    'query': f'{input("what did you do?").lower()}',
    'gender': GENDER,
    'weight_kg': WEIGHT_KG,
    'height_cm': HEIGHT_CM,
    'age': AGE,
}

response = requests.post(url=exercise_endpoint, json=user_response, headers=headers, timeout=60)
result = response.json()

today = datetime.now()
time = today.time().strftime("%X")
date = today.strftime("%d/%m/%Y")

for exercise in result['exercises']:
    sheet_inputs = {
        'workout': {
            'date': date,
            'time': time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }

sheety_response = requests.post(url=sheety_endpoint, json=sheet_inputs, headers=headers, timeout=60)
print(sheety_response.text)
