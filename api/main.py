from typing import Union

from fastapi import FastAPI, status, Response
from pydantic import BaseModel

from producer import Producer

producer = Producer()
producer.connect()

LOG_TYPES = ("info", "warning", "error")

app = FastAPI()

class Log(BaseModel):
    type: str
    message: str


@app.get("/")
def read_root():
    return "running"

@app.post("/log", status_code=status.HTTP_200_OK)
def send_message(log: Log, response: Response):
    try:
        if log.type not in LOG_TYPES:
            return Response(
                content='Invalid log type. Use either "info", "warning" or "error".',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            "type": log.type,
            "message": log.message
        }

        producer.handleLog(str(data))

        return {"log_type": log.type, "log_message": log.message}
    except Exception as e:
        exceptionType, exceptionMessage = e.args
        print("EXCEPTION TYPE: {}".format(exceptionType))
        print("EXCEPTION MESSAGE: {}".format(exceptionMessage))

        return Response(
            content="Error processing the message",
            status_code=status.HTTP_400_BAD_REQUEST
        )