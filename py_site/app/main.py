from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import random
from prometheus_client import Gauge, make_asgi_app
import time
import requests

app = FastAPI(title="Proposal", version="0.5.0")
TEXT = "Alfred proposes to Florina 3+ times"
favicon_path = "./app/static/icon.png"

templates = Jinja2Templates(directory="./app/static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


""" 
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
    return Response(content=image_bytes, media_type="image/jpeg") """


g = Gauge("test_guage", "description for the test_guage")


@app.get("/api")
async def api():
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term": "set"}
    headers = {
        "X-RapidAPI-Key": "e15cce8cedmsh829310d4a331963p1ca8fdjsnd643b41e3b65",
        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com",
    }
    return requests.get(url, headers=headers, params=querystring).json()


@app.get("/working")
async def working():
    g.set(random.random())
    return {"working": "ok", "language": "python", "time": time.strftime("%X %x %Z")}


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=3000)
