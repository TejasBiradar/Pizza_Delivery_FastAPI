from fastapi import FastAPI,Depends
from routers.auth_routers import auth_router
from routers.order_routers import order_router
from schemas import Settings,LoginModel


from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

# Configure templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, tags=["DEFAULT"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(auth_router)
app.include_router(order_router)
