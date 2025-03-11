from fastapi import FastAPI, File, UploadFile
import uvicorn
from pydantic import BaseModel
from book_agent import send_bookinfo
import os
import shutil
import whisper

import subprocess

try:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
    print(result.stdout)  # ffmpeg 버전 정보 출력
except FileNotFoundError:
    print("Python에서 ffmpeg 실행 파일을 찾을 수 없습니다.")


app = FastAPI()

class Message(BaseModel):
    msg: str

stt_model = whisper.load_model('base')

@app.get('/book_info')
async def bookinfo(chatmsg: Message):
    response = send_bookinfo(chatmsg)
    return response


@app.post('/send_wav')
def send_wav(file: UploadFile=File(...)):
    folder_path = "sound"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = stt_model.transcribe(file_path)
    
    return {'result': result}
    
    
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


