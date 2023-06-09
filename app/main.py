import base64
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response, StreamingResponse
import nicegui as ui
import uvicorn
import io
import cv2
import numpy as np
import glob
import random
from prometheus_client import make_asgi_app

app = FastAPI(title="Proposal", version="0.3.0")
TEXT = "Alfred proposes to Florina 3+ times"
favicon_path = "./app/static/icon.png"


@app.get("/")
def root():
    img_name = random.choice(glob.glob("./app/static/image_*"))
    img = cv2.imread(img_name)
    img_y, img_x, _ = img.shape

    cv2.putText(
        img=img,
        text=TEXT,
        org=(img_x // 2 - (len(TEXT) // 2) * 18, img_y // 5),
        fontFace=cv2.FONT_HERSHEY_TRIPLEX,
        fontScale=1,
        color=(0, 0, 255),
        thickness=1,
    )
    _, img_jpeg = cv2.imencode(".jpeg", img)
    return StreamingResponse(io.BytesIO(img_jpeg.tobytes()), media_type="image/jpeg")


def gen_frames():
    vid = cv2.VideoCapture(0)
    while True:
        _, frame = vid.read()
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/video")
async def frame_fn():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


@app.get("/image",
         responses = {200: {"content": {"image/jpeg": {}}}},
         response_class=Response
)
def get_image():
    img_name = random.choice(glob.glob("./app/static/image_*"))
    img = cv2.imread(img_name)
    img_y, img_x, _ = img.shape

    cv2.putText(
        img=img,
        text=TEXT,
        org=(img_x // 2 - (len(TEXT) // 2) * 18, img_y // 5),
        fontFace=cv2.FONT_HERSHEY_TRIPLEX,
        fontScale=1,
        color=(0, 0, 255),
        thickness=1,
    )
    _, img_jpeg = cv2.imencode(".jpeg", img)
    image_bytes: bytes = img_jpeg.tobytes()
    return Response(content=image_bytes, media_type="image/jpeg")


@app.get("/working")
def health():
    return {"health": True}



metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=3000, reload=True, workers=2)
