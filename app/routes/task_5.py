from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

import zipfile
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
    """
    Input:
    file: UploadFile - файл, который нужно сохранить и заархивировать.
    Output:
    {"file_id": file_id, "zip_file_id": zip_file_id}: {"file_id": int, "zip_file_id": int} - 
    id файла, id архива.
    """

    file_id: int
    zip_file_id: int

    try:
        file_name = file.filename
        file_path = "app\\files\\"
        p = path.abspath(file_path+file_name)

        with open(p, "wb") as f:
            f.write(file.file.read())

        with zipfile.ZipFile(p + '.zip', 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(p, arcname=p.split("\\")[-1])


        file_id = int(popen(fr'fsutil file queryfileid "{p}"').read().split(":")[-1].strip(), 16)
        zip_file_id = int(popen(fr'fsutil file queryfileid "{p}.zip"').read().split(":")[-1].strip(), 16)
        return {"file_id": file_id, "zip_file_id": zip_file_id}
    except Exception as e:
        return {"message": e.args}
    

@router.get("/download_file/{file_id}", description="Задание_5. API для хранения файлов")
async def download_file(file_id: int):
    """
    Input:
    file_id: int - id файла
    Output: 
    file: FileResponse - файл для скачивания.

    """

    file: FileResponse =  None
    file_path = "app\\files\\"
    try:
        for file_name in listdir(file_path):
            full_path = file_path + file_name
            if file_id == int(popen(fr'fsutil file queryfileid "{full_path}"').read().split(":")[-1].strip(), 16):
                file = FileResponse(full_path, filename=file_name, media_type='application/octet-stream')
                return file
        return {"message": "Файл не найден."}
    except Exception as e:
        return {"message": e.args}