from fastapi import BackgroundTasks, FastAPI, Query, Request, status, Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app import functions
from app.settings import env

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Hello, World!"},
    )

@app.post("/log/{service}")
async def log(
    background_tasks: BackgroundTasks,
    service: str = Path(description="Service name"),
):
    background_tasks.add_task(functions.generate_log, service)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Log generated!"},
    )


@app.post("/log/{service}/{count}")
async def log_with_count(
    background_tasks: BackgroundTasks,
    service: str = Path(description="Service name"),
    count: int = Path(description="Number of logs to generate"),
):
    background_tasks.add_task(functions.generate_log, service, count)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Log generated!"},
    )


@app.get("/log/{service}")
async def stream_log(
    service: str,
    limit: int = Query(20, gt=0, le=env.stream_max_length),
    last_id: str = Query("-", description="Last ID of the previous batch of logs"),
):
    stream_objects, last_id = await functions.retrieve_log(
        service=service,
        last_id=last_id,
        count=limit,
    )

    stream_dicts = [obj.dict() for obj in stream_objects]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"logs": stream_dicts, "last_id": last_id},
    )


# render html template
@app.get("/log/{service}/html", response_class=HTMLResponse)
async def stream_log_html(request: Request, service: str):
    return templates.TemplateResponse(
        "stream.html",
        {"request": request, "service": service},
    )


@app.get("/log/{service}/string")
async def stream_log_string(
    service: str,
    limit: int = Query(20, gt=0, le=env.stream_max_length),
    last_id: str = Query("-", description="Last ID of the previous batch of logs"),
):
    string_logs, last_id = await functions.retrieve_log_as_string(
        service=service,
        last_id=last_id,
        count=limit,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"logs": string_logs, "last_id": last_id},
    )
