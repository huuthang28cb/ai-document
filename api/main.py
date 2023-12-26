from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
import requests

from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Endpoint for the webhook
@app.get("/webhook")
async def webhook(request: Request):
    # Access query parameters using the Request object
    mode = request.query_params.get("hub.mode")
    verify_token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    # Check if mode and token are in the query string of the request
    if mode and verify_token:
        # Check the mode and token sent is correct
        if mode == "subscribe" and verify_token == '79797979':
            # Respond with the challenge token from the request
            return PlainTextResponse(content=challenge, status_code=200)
        else:
            # Respond with '403 Forbidden' if verify tokens do not match
            raise HTTPException(status_code=403, detail="Forbidden: Verify tokens do not match")
    else:
        # Respond with '400 Bad Request' if mode or token missing from query parameters
        raise HTTPException(status_code=400, detail="Bad Request: Mode or token missing from query parameters")
    

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']

    if 'text' in message:
        text = message.get('text')
        # call api chatbot, put text => resutl: text ==> requests.post(graph.facebook.com) reply user
        resultFromAiDocument = 'Hello, i am bot!'
        
        request_body = {
            'recipient': {
                'id': sender_id
            },
            'message': {"text": "hello, world!"}
        }
    #     response = requests.post(f'https://graph.facebook.com/v5.0/me/messages?access_token=EAAMwid1T74ABO6OJiOXBl6UAEOXxha3spZCYgJkepsBaRWEX22TnEv3OPkXE71EYUwSu4mRTZARnIYFVV7JUPHMhVMUMla5KpYUkuMgXOZAhvqFbKT9s4CjAUp1POFMwO5NZBIs1ZC47GUgS5XpEX7sMZBs7Ttjwtw8rHTMgwpy8kN0pgWm3asFyilp11ZBjpUD', json=request_body).json()
    #     return JSONResponse(content=response)
    
    return JSONResponse(content={"result": resultFromAiDocument})
