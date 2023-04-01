from starlite import Starlite, get
import uvicorn

@get("/")
def index() -> dict[str, str]:
    return {"hello": "world"}


app = Starlite(route_handlers=[index])

uvicorn.run(app, host='0.0.0.0', port=3000)