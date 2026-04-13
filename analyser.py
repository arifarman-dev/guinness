
from openai import OpenAI

import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1"
MODEL = "meta-llama/llama-3.1-8b-instruct"
client = OpenAI(base_url=OPENROUTER_URL, api_key=OPENROUTER_API_KEY)
prompt = """
        You are a highly precise sentiment analysis engine. Your task is to analyze the provided text for emotional tone, intensity and mood.

        Rules:
        - Return ONLY a valid JSON object. Do not include any conversational text or explanations.
        - Classify sentiment as: POSITIVE, NEGATIVE, NEUTRAL, or MIXED.
        - Detect sarcasm or irony.
        Output Format:
        {
            "sentiment": "string",
            "confidence_score": 0.00,
            "sarcasm_detected": boolean,
        }
        """
def analyse_sentiment(comment):
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user",   "content": comment},
            ],
            response_format={"type": "json_object"},
            max_tokens=150,
            temperature=0,
        )
        
        data = json.loads(resp.choices[0].message.content)
        return data
        
    except Exception as e:
        return {"error": str(e), "sentiment": "UNKNOWN"}
    
if __name__ == "__main__":
    with open('./data/stories.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    comments = [comment['text'] for comment in data[0]['comments']]
    result = {}
    for comment in comments:
        print(comment)
        detected_sentiment = analyse_sentiment(comment)
        print(detected_sentiment)
        if detected_sentiment['sentiment'] not in result:
            result[detected_sentiment['sentiment']] = 1
        else:
            result[detected_sentiment['sentiment']] += 1
    print(result)
