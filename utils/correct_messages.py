from translate import Translator


class CorrectMessages:
    
    @staticmethod
    def is_russian(text: str) -> bool:
        """Check is text russian"""
        for let in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
            if let in text:
                return True
        return False        
        
    @staticmethod
    def translate_text(text: str) -> str:
        """Translate rus text to eng or vice a versa"""
        
        if CorrectMessages.is_russian(text=text):
            translator = Translator(from_lang="ru", to_lang="en")
        else:
            translator = Translator(from_lang="en", to_lang="ru")

        return translator.translate(text=text)
    
    @staticmethod
    def split_message(message: str, limit=4096):
        """Splits the text into parts that do not exceed the limit."""
        return [message[i: i+limit] for i in range(0, len(message), limit)]