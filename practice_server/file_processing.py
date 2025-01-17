from fastapi import APIRouter, File, UploadFile
from PIL import Image
import csv
import io


file_router = APIRouter(prefix="/file-processing", tags=["Files"])

@file_router.post("/upload")
async def upload_image(file: UploadFile = File(...)):  # 비동기 함수
    image = Image.open(io.BytesIO(await file.read()))
    save_path = f"./{file.filename}"
    # buf = io.BytesIO()
    image.save(save_path, format="PNG")
    return f"{file.filename} 이미지 저장 완료"

@file_router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):  # 비동기 함수
    contents = file.file.read()
    save_path = f"./{file.filename}"
    buf = io.StringIO(contents.decode('utf-8'))  # 인코딩 에러 발생
    # buf = io.StringIO(contents.decode())
    # csvReader = csv.DictReader(buf)
    # data = csv.reader(buf)
    data = list(csv.reader(buf))
    
    with open(save_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    for row in data:  
        print(row)
    buf.close()
    file.file.close()
    return f"{file.filename} 파일 저장 완료\t컬럼명:{' '.join(data[0])}"


@file_router.post("/upload_files")
async def upload_files(file: UploadFile = File(...)):  # 비동기 함수
    print(file.filename)
    print(file.content_type)
    print(file.headers)
    print(file.size)
    
    save_path = f"./test_{file.filename}"
    file_content = await file.read()
    
    with open(save_path, "wb") as f:
        f.write(file_content)
    
    return f"{file.filename} 파일 저장 완료\t컬럼명:{' '.join(list(file_content))[0]}"
    