from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

import threading
import queue

app = FastAPI()

update_queue = queue.Queue()

class LatLong(BaseModel):
    latitude: float
    longitude: float

# replace this with the root url for your app,
# http://127.0.0.1:8000 if you're doing it locally or
# use ngrok to generate a link like the one below :)
base_url = 'https://fd82-2a0c-5bc0-40-3e3a-f866-b6b3-8188-5317.ngrok-free.app'
# base_url = "http://127.0.0.1:8000"


dev_id = 'militerra-testing-Zbf5Rx4BcZ'
api_key = 'roLM-wTfZOpwjaa8hlsWPcr-W4cB0X24'

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This is for demonstration; specify your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOMINATIM_API_URL = "https://nominatim.openstreetmap.org/search"

@app.get("/geocode")
def geocode(q: str):
    params = {
        "q": q,
        "format": "json"
    }
    response = requests.get(NOMINATIM_API_URL, params=params)
    return response.json()


@app.get('/login')
async def auth():    
    # generates a widget to be shown to the user
    res = requests.post('https://api.tryterra.co/auth/generateWidgetSession',
        headers={ 
            'dev-id': dev_id, 
            'x-api-key': api_key
        },
        json={
            'reference_id': 'john',
            'auth_success_redirect_url': f'{base_url}/on_auth_success' # after the user finishes connecting, we send em here
        }
    )

    data = res.json()
    url = data['url']
    return RedirectResponse(url)


# The user will be sent here after auth

@app.get('/on_auth_success')
async def auth_success(user_id: str, reference_id: str):

    # test getting data for the new user_id
    # you can also just store the user_id for later

    res = requests.get('https://api.tryterra.co/v2/daily',
        params={
            'user_id': user_id, 
            'start_date': '2024-01-25', 
            'end_date': '2024-02-03', 
            'with_samples': True, 
            'to_webhook': False             # set this to true if you prefer we send the data to your database or to the webhook you can setup below
        },
        headers={
            'dev-id': dev_id, 
            'x-api-key': api_key 
        }
    )

    data = res.json()
    print(data)
    return { 'user_id': user_id, 'ref': reference_id, 'data': data  
}



# This is what a webhook looks like!
#
# But it won't work if it is localhost or http://127.0.0.1
# Try use ngrok to make it public and provider the url for
# the webhook to our https://dashboard.tryterra.co/connections :)

# Generic endpoint for TerraAPI consumption
@app.post('/consume')
async def consume(request: Request):
    data = await request.json()

    # you can now do whatever you want with the data
    # checkout https://docs.tryterra.co/reference/v2
    # to see what the data would look like.

    print("Adding to queue:", data)
    # need to pick out the right data...    
    update_queue.put(data)

    return { 'success': 'updated soldier' } 


soldiers_data = {
    "soldier-1": {
        "name": "Abraham Mathew",
        "mission_name": "MiddleEast-2024-TRAIN",
        "location": [51.877234, -3.435486],
        "health": {
            "overall_score": "N/A",
            "heart_rate": "N/A",
            "temperature": "N/A", # prevent against heat-stress/temp related issues
            "overall_score": "N/A",
            "hydration": "N/A",
            "muscle_mass": "N/A",
            "body_fat": "N/A",
            "max_speed": "N/A",
            "sleep": "N/A",
            "stress": "N/A"
        },
        "mission_commands": [""],
        "needs_support": False
    },
    "soldier-2": {
        "name": "Kevin Thomas",
        "mission_name": "MiddleEast-2024-TRAIN",
        "location": [51.887223, -3.451453],
        "health": {
            "overall_score": "N/A",
            "heart_rate": "N/A",
            "temperature": "N/A", # prevent against heat-stress/temp related issues
            "overall_score": "N/A",
            "hydration": "N/A",
            "muscle_mass": "N/A",
            "body_fat": "N/A",
            "max_speed": "N/A",
            "sleep": "N/A",
            "stress": "N/A"
        },
        "mission_commands": [""],
        "needs_support": True
    },
    "john": {
        "name": "John Yu",
        "mission_name": "MiddleEast-2024-TRAIN",
        "location": [51.887223, -3.42],
        "health": {
            "overall_score": "N/A",
            "heart_rate": "N/A",
            "temperature": "N/A", # prevent against heat-stress/temp related issues
            "overall_score": "N/A",
            "hydration": "N/A",
            "muscle_mass": "N/A",
            "body_fat": "N/A",
            "max_speed": "N/A",
            "sleep": "N/A",
            "stress": "N/A"
        },
        "mission_commands": [""],
        "needs_support": False
    },
}

# Personel Dashboard

# Polled and viewed statically afterwards
@app.get('/analytics') # {soldier_id}
async def analytics(): # soldier_id: str
    print(soldiers_data['john'])
    return {
        "overall_score": soldiers_data["john"]["health"]["overall_score"],
        "hydration": soldiers_data["john"]["health"]["hydration"],
        "muscle_mass": soldiers_data["john"]["health"]["muscle_mass"],
        "body_fat": soldiers_data["john"]["health"]["body_fat"],
        "max_speed": soldiers_data["john"]["health"]["max_speed"],
        "sleep": soldiers_data["john"]["health"]["sleep"],
        "stress": soldiers_data["john"]["health"]["stress"]
    }


# Polled regularly
@app.post('/location') # {soldier_id}
async def location(lat_long: LatLong): # soldier_id: str
    # Update the soldier location
    print(lat_long.latitude, lat_long.longitude)
    soldiers_data["john"]["location"] = [lat_long.latitude, lat_long.longitude]
    return { 'success': 'ok' } 


# Command Dashboard

@app.get('/soldiers')
async def soldiers():
    return soldiers_data


# Takes in the soldier data one by one in the queue
# and processes it as it is
def soldiers_processing():
    # Take latest info and process it
    while True:
        soldier_update = update_queue.get()
        print("Processing: ", soldier_update)

        soldiers_data["john"] = {
                "overall_score": "N/A",
                "heart_rate": "N/A",
                "temperature": "N/A", # prevent against heat-stress/temp related issues
                "overall_score": "N/A",
                "hydration": "N/A",
                "muscle_mass": "N/A",
                "body_fat": "N/A",
                "max_speed": "N/A",
                "sleep": "N/A",
                "stress": "N/A"
        }


threading.Thread(target=soldiers_processing, daemon=True).start()


# 1. health metrics.. averaged compared to the group...

# After your done, go to {base_url}/login to start using your
# app.
# Can't wait to see what you build!!!