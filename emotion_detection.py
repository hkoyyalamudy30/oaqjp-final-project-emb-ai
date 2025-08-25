import requests
import json

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def extract_emotions(resp):
    if isinstance(resp, dict):  # make sure the response is actually a dictionary
        if resp.get("emotionPredictions"):
            first = resp["emotionPredictions"][0] 
            if isinstance(first, dict) and "emotion" in first:  
                return first["emotion"]  
    return {}

def emotion_detector(text_to_analyze):
    payload = {"raw_document": {"text": text_to_analyze}}
    res = requests.post(URL, headers=HEADERS, json=payload)
    data = json.loads(res.text)

    # getting all the emotions so we can format the response json
    emotions = extract_emotions(data)
    anger = float(emotions.get("anger", 0))
    disgust = float(emotions.get("disgust", 0))
    fear = float(emotions.get("fear", 0))
    joy = float(emotions.get("joy", 0))
    sadness = float(emotions.get("sadness", 0))

    # makin and returning the response json 
    scores = {"anger": anger, "disgust": disgust, "fear": fear, "joy": joy, "sadness": sadness}
    dom_e = max(scores, key=scores.get) if scores else None

    return {"anger": anger, "disgust": disgust, "fear": fear, "joy": joy, "sadness": sadness, "dominant_emotion": dom_e}

    #return res.text