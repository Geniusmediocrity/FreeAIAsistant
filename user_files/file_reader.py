import asyncio

# uv pip install aiofiles PyPDF2 python-docx pandas
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
    if file_path.endswith(('.txt', '.js', '.py', '.java', '.css', '.html', '.log', '.c', '.c++', '.cc', '.Cs', '.cs', '.Csharp', '.csharp', '.xml', '.json', '.csv')):
        return await __read_text_file(file_path)
    elif file_path.endswith('.docx'):
        return await __read_docx_file(file_path)
    elif file_path.endswith('.pdf'):
        return await __read_pdf_file(file_path)
    elif file_path.endswith('.xlsx'):
        return await __read_xlsx_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

# Пример использования
async def main():
    file = 'test.csv'
    result = await read_file(file)
    print(result)

# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())
    
#* GOOD:
# 1. css
# 2. txt
# 3. html
# 4. json
# 5. py
# 6. js
# 7. java
# 8. log
# 9. c
# 10. c++
# 11. cs
# 12. csharp
# 13. xlsx
# 14. csv
# 15. docx
# 16. xml

#? DONT KNOW:
# 16. PDF
