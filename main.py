from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

    return { 'user_id': user_id, 'ref': reference_id, 'data': data  }



# This is what a webhook looks like!
#
# But it won't work if it is localhost or http://127.0.0.1
# Try use ngrok to make it public and provider the url for
# the webhook to our https://dashboard.tryterra.co/connections :)

@app.post('/consume')
async def consume(request: Request):
    data = await request.json()

    # you can now do whatever you want with the data
    # checkout https://docs.tryterra.co/reference/v2
    # to see what the data would look like.

    print(data)

    return { 'success': 'ok' }


# After your done, go to {base_url}/login to start using your
# app.
# Can't wait to see what you build!!!