import requests
import json

url="http://localhost:1234/v1/chat/completions"
headers={
    "Content-Type": "application/json"
}
payload={
    "model" : "gemma-3-4b-it-qat-int4",
    "messages":[
        {
            "role":"system",
            "content":"help me  in ml"
        },
        {
            "role":"user",
            "content":"hello"
        }
    ],
    "temprature":0.7,
    "max_tokens":256,
    "top_p":0.9,
    "top_k":40,
    "presence_penalty":0.0,
    "frequency_penalty":0.0,
    "stop":["\n"]
}

response=requests.post(url,headers=headers,data=json.dumps(payload))
print(response.json())