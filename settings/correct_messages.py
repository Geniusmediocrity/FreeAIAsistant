from settings.tokn import Tokns
import requests


class CorrectMessages:
    
    @staticmethod
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
                    "content": f"Translate this text from Russian into English {text}. Print only the translated text and nothing else."
                }
        ]}
        response = requests.post(Tokns.URL, json=data, headers=Tokns.HEADERS)
        data = (response.json())['choices'][0]['message']['content'].split('</think>\n\n')[1]
        return data

    @staticmethod
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
                    "content": f"Переведи данный текст на русский язык: {text}. Выведи только переведенный текст и нечего больше"
                }
        ]}
        
        response = requests.post(Tokns.URL, json=data, headers=Tokns.HEADERS)
        data = (response.json())['choices'][0]['message']['content'].split('</think>\n\n')[1]
        return data
    
    @staticmethod
    def split_message(message: str, limit=4096):
        """Разбивает текст на части, не превышающие limit."""
        return [message[i: i+limit] for i in range(0, len(message), limit)]