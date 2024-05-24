import requests
import json


def rephrase(text):
    url = "http://localhost:11434/api/generate"

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "model": "mistral",
        "prompt": f"Rephrase this text in a simpler way: {text}",
        "stream": False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        pass
    else:
        print("Error: ", response.status_code, response.text)

    # return the part between "response" and "done"
    return response.text.split("response")[1].split("done")[0][4:-3]


#print(rephrase("The quick brown fox eats its proper feces."))
