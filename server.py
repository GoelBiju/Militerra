from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
import httpx
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
import time
import random

import threading
import queue

import random

app = FastAPI()

update_queue = queue.Queue()

class LatLong(BaseModel):
    latitude: float
    longitude: float

# replace this with the root url for your app,
# http://127.0.0.1:8000 if you're doing it locally or
# use ngrok to generate a link like the one below :)
base_url = 'https://4ee9-79-78-211-126.ngrok-free.app'
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


@app.get("/ui_soldiers")
async def get_ui_soldiers():
    # Assuming 'external_api_url' is the URL where you fetch soldier data from
    external_api_url = f"{base_url}/soldiers"
    async with httpx.AsyncClient() as client:
        response = await client.get(external_api_url)
        # Perform error handling as necessary
        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content={"message": "Failed to fetch soldiers"})
        return response.json()
    
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

# https://dashboard.tryterra.co/api/tools/debug/users/data?type=activity&dev_id=militerra-testing-Zbf5Rx4BcZ&user_id=550e6fea-60ab-44d9-90f7-77414c8f1b40&start_date=2024-02-03&end_date=2024-02-04&to_webhook=false

# Generic endpoint for TerraAPI consumption
@app.post('/consume')
async def consume(request: Request):
    data = await request.json()

    # you can now do whatever you want with the data
    # checkout https://docs.tryterra.co/reference/v2
    # to see what the data would look like.

    print("Adding to queue:", data)
    # need to pick out the right data...    
    picked_data = {
        "soldier": data["user"]["reference_id"],
        "heart_rate": random.randint(70, 90),
        "temperature": random.randint(24, 30),
        "hydration": random.randint(500, 1500), # constant
        "muscle_mass": random.randint(80, 90), # constant
        "body_fat": random.randint(10, 20), # constant
        "max_speed": random.randint(8, 10),
        "sleep": random.randint(7, 12), # constant
        "stress": random.randint(80, 90)
    }
    
    print(picked_data)
    update_queue.put(picked_data)

    return { 'success': 'updated soldier' } 

class Soldier():
    def __init__(self, name, mission_name, location, health, mission_commands, needs_support):
        self.name = name
        self.mission_name = mission_name
        self.location = location
        self.health = health
        self.mission_commands = mission_commands
        self.needs_support = needs_support
        self.overall_score = 0


    def set_location(self, loc):
        self.location = loc

    def set_health(self, health):
        self.health = health

    def set_mission_commmands(self, mission_commands):
        self.mission_commands = mission_commands

    def needs_support(self, needs_support):
        self.needs_support = needs_support


    def calculate_overall_score(self):
        max_score = 1548
        return ((-4 * int(self.health["stress"]) +
                2 * int(self.health["heart_rate"]) +
                2 * int(self.health["muscle_mass"]) +
                3 * int(self.health["max_speed"]) +
                3 * int(self.health["body_fat"]) +
                3 * int(self.health["temperature"]) +
                1 * int(self.health["hydration"]) +
                4 * int(self.health["sleep"]))/max_score) * 100


default_health = {
            "heart_rate": random.randint(70, 90),
            "temperature": random.randint(24, 30),
            "hydration": random.randint(500, 1500),
            "max_speed": random.randint(8, 10),
            "stress": random.randint(80, 90),
            "muscle_mass": random.randint(12, 25),
            "body_fat": random.randint(3, 14),
            "sleep": random.randint(1, 24)
        }


soldier1 = Soldier("Abraham Mathew", "SouthWest-2024-TRAIN", [51.8833, -3.4333], default_health, [""], False)
soldier2 = Soldier("Kevin Thomas", "SouthWest-2024-TRAIN", [51.8892, -3.437], default_health, [""], True)
soldier3 = Soldier("Ellie Thomas", "SouthWest-2024-TRAIN", [51.882, -3.493], default_health, [""], False)
soldier4 = Soldier("John Yu", "SouthWest-2024-TRAIN", [51.889, -3.430], default_health, [""], False)
soldiers_data = [soldier1, soldier2, soldier3, soldier4]

# Personel Dashboard

# Polled and viewed statically afterwards
@app.get('/analytics') # {soldier_id}
async def analytics(): # soldier_id: str
    print(soldier4.name)
    return soldier4.health


# Polled regularly
@app.post('/location') # {soldier_id}
async def location(lat_long: LatLong): # soldier_id: str
    # Update the soldier location
    print(lat_long.latitude, lat_long.longitude)
    soldier3.location = [lat_long.latitude, lat_long.longitude]
    return { 'success': 'ok' }


# Command Dashboard

@app.get('/soldiers')
async def soldiers():
    return [soldier1, soldier2, soldier3, soldier4]


def process_overall_score(soldier):
    return soldier.health["overall_score"]


# Takes in the soldier data one by one in the queue
# and processes it as it is
def soldiers_processing():
    # Take latest info and process it
    while True:
        for soldier in soldiers_data:
            if soldier.name != "John Yu":
                soldier.health = {
                    # "overall_score": process_overall_score(soldiers_data[soldier]),
                    "heart_rate": str(random.randint(70, 90)),
                    "temperature": str(random.randint(24, 30)),
                    "hydration": str(random.randint(500, 1500)),
                    "max_speed": str(random.randint(8, 10)),
                    "stress": str(random.randint(80, 90)),
                    "muscle_mass": random.randint(12, 25),
                    "body_fat": random.randint(3, 14),
                    "sleep": random.randint(1, 24)
                }
            else:
                if (int(soldier.health["heart_rate"]) > 4):
                    soldier.health["heart_rate"] = str(int(soldier.health["heart_rate"]) - random.randint(0, 4))
                if (int(soldier.health["max_speed"]) > 4) :
                    soldier.health["max_speed"] = str(int(soldier.health["heart_rate"]) - random.randint(0, 4))    

                soldier.location[0] += 0.00001
                soldier.location[1] += 0.0005


        time.sleep(2)
        soldier.calculate_overall_score()
                
                # If the user is "john", then exhibit poorer performance
                # high chance he will need support, so slowly deteriorating performance...

threading.Thread(target=soldiers_processing, daemon=True).start()


# 1. health metrics.. averaged compared to the group...

# After your done, go to {base_url}/login to start using your
# app.
# Can't wait to see what you build!!!