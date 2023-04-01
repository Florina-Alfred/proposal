import base64
from fastapi.responses import FileResponse, Response, StreamingResponse
import io
from fastapi import FastAPI
import cv2
import uvicorn

app = FastAPI()
TEXT = "Alfred prposes to Florina 3 times"


@app.get("/")
def root():
    img = cv2.imread("./app/static/images.jpeg")
    img_y, img_x, _ = img.shape

    cv2.putText(img=img,
                text=TEXT,
                org=(img_x//2 - (len(TEXT)//2)*18, img_y//5),
                fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                fontScale=1,
                color=(0, 0, 255),
                thickness=1)
    _, img_jpeg = cv2.imencode(".jpeg", img)
    return StreamingResponse(io.BytesIO(img_jpeg.tobytes()),
                             media_type="image/jpeg")


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0",
                port=3000, reload=True, workers=2)
