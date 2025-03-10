from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from book_agent import send_bookinfo

app = FastAPI()

class Message(BaseModel):
    msg: str
    
@app.get('/book_info')
async def bookinfo(chatmsg: Message):
    response = send_bookinfo(chatmsg)
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


