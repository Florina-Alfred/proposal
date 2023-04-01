from starlite import Starlite, MediaType, get
import uvicorn

@get(path="/", media_type=MediaType.TEXT)
def index() -> str:
    return "hello Florina"


app = Starlite(route_handlers=[index])

uvicorn.run(app, host='0.0.0.0', port=3000)