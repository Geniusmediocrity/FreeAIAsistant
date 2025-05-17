from os import remove as os_remove_file

import aiofiles
from docx import Document # Для чтения .docx
from PyPDF2 import PdfReader
import pandas as pd


async def __read_text_file(file_path: str) -> str:
    """Асинхронная функция для чтения текстовых файлов"""
    
    async with aiofiles.open(file_path, mode='rt', encoding='utf-8') as file:
        return await file.read()


async def __read_docx_file(file_path: str) -> str:
    """СИНХРОННАЯ функция для чтения .docx файлов"""

    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


async def __read_pdf_file(file_path: str) -> str:
    """Асинхронная функция для чтения .pdf файлов"""
    
    async with aiofiles.open(file_path, mode='rb') as file:
        data = await file.read()
    reader = PdfReader(data)
    return "\n".join([page.extract_text() for page in reader.pages])
    

async def __read_xlsx_file(file_path: str) -> str:
    """Асинхронная функция для чтения .xlsx файлов"""
    
    async with aiofiles.open(file_path, mode='rb') as file:
        data = await file.read()
    df = pd.read_excel(data)
    return df.to_string(index=False)


async def read_file(file_path: str) -> str:
    """Основная функция для выбора типа файла и его чтения"""
    
    if file_path.endswith(('.txt', '.js', '.py', '.java', '.css', '.html', '.log', '.xml', '.json', '.csv')):
        result = await __read_text_file(file_path)
    elif file_path.endswith('.docx'):
        result = await __read_docx_file(file_path)
    elif file_path.endswith('.pdf'):
        result = await __read_pdf_file(file_path)
    elif file_path.endswith('.xlsx'):
        result = await __read_xlsx_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
    os_remove_file(path=file_path)
    return result
    
#* GOOD:
# 1.  css
# 2.  txt
# 3.  html
# 4.  json
# 5.  py
# 6.  js
# 7.  java
# 8.  log
# 9. xlsx
# 10. csv
# 11. docx
# 12. xml

#? DONT KNOW:
# 13. PDF
