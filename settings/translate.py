from settings.tokn import HEADERS, URL
import requests


def translate_to_english(text):
    data = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {
                "role": "system",
                "content": "You're a helpful AI assistant"
            },
            {
                "role": "user",
                "content": f"Translate this text from Russian into English {text}"
            }
    ]}
    response = requests.post(URL, json=data, headers=HEADERS)
    data = (response.json())['choices'][0]['message']['content'].split('</think>\n\n')[1]
    return data


def translate_to_rus(text):
    data = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {
                "role": "system",
                "content": "Ты очень полезный высокоуровневый помощник"
            },
            {
                "role": "user",
                "content": f"Переведи данный текст на русский язык: {text}"
            }
    ]}
    
    response = requests.post(URL, json=data, headers=HEADERS)
    data = (response.json())['choices'][0]['message']['content'].split('</think>\n\n')[1]
    return data