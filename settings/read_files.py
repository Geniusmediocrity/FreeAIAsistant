from docx import Document  # Для чтения .docx
from win32com import client  # Для чтения .doc (только на Windows)
import os


class ReadFiles:
    
    def __read_txt(file_path):
        """Чтение .txt файлов."""
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        os.remove(file_path)    
        return text
        
        
    def __read_docx(file_path):
        """Чтение .docx файлов."""
        try:
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(e)
        finally:
            os.remove(file_path)
            
            
    def __read_doc(file_path):
        """Чтение .doc файлов"""
        try:
            word = client.Dispatch("Word.Application")
            word.visible = False
            doc = word.Documents.Open(file_path)
            text = doc.Content.Text
            doc.Close()
            word.Quit()
            return text
        except Exception as e:
            print(e)
        finally:
            os.remove(file_path)


    def read_file(self, file_path):
        """Чтение файла в зависимости от его расширения."""
        if file_path.endswith('.txt'):
            return self.__read_txt(file_path=file_path)
        elif file_path.endswith('.docx'):
            return self.__read_docx(file_path=file_path)
        elif file_path.endswith('.doc'):
            return self.__read_doc(file_path=file_path)
