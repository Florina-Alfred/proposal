import base64
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response, StreamingResponse
import nicegui as ui
import uvicorn
import io
import cv2

app = FastAPI(title="Proposal", version="0.3.0")
TEXT = "Alfred proposes to Florina 5 times"
favicon_path = "./app/static/icon.png"


@app.get("/")
def root():
    img = cv2.imread("./app/static/images.jpeg")
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


@app.get("/working")
def health():
    return {"health": True}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=3000, reload=True, workers=2)
