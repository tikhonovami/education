from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from shutil import make_archive
from os import popen, path, listdir

router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_5. API для хранения файлов

a.	Написать API для добавления(POST) "/upload_file" и скачивания (GET) "/download_file/{id}" файлов. 
В ответ на удачную загрузку файла должен приходить id для скачивания. 
b.	Добавить архивирование к post запросу, то есть файл должен сжиматься и сохраняться в ZIP формате.
с*.Добавить аннотации типов.
"""
@router.post("/upload_file", description="Задание_5. API для хранения файлов")
async def upload_file(file: UploadFile):
    """Описание."""

    file_id: int
    
    try:
        file_name = file.filename
        file_path = "app\\files\\"
        p = path.abspath(file_path+file_name)
        with open(p, "wb") as f:
            f.write(file.file.read())
            file_id = int(popen(fr'fsutil file queryfileid "{p}"').read().split(":")[-1].strip(), 16)
            #make_archive(file_name, format='zip')
            return {"file_id": file_id}
    except Exception as e:
        return {"message": e.args}
    

@router.get("/download_file/{file_id}", description="Задание_5. API для хранения файлов")
async def download_file(file_id: int):
    """Описание."""
    file =  None
    file_path = "app\\files\\"

    for file_name in listdir(file_path):
        full_path = file_path + file_name
        if file_id == int(popen(fr'fsutil file queryfileid "{full_path}"').read().split(":")[-1].strip(), 16):
            file = FileResponse(full_path)
            return file
    return {"message": "Файл не найден."}
