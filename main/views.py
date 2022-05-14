from starlette.requests import Request
from starlette.responses import JSONResponse


async def main(request: Request) -> JSONResponse:
    test = request.path_params.get("test", "ok")
    return JSONResponse({"monitoring__gate": test})
