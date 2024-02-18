from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
import json

from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
import requests

with open("../config/native-app.json", "r") as config_file:
    cfg = json.load(config_file)

templates = Jinja2Templates(directory="templates")

token_auth_scheme = HTTPBearer()

app = FastAPI()


@app.get("/api/private")
def private(token: str = Depends(token_auth_scheme)):
    result = {
        "status": "success",
        "msg": "hello private!"
    }
    return result


@app.get("/api/public")
def public():
    result = {
        "status": "success",
        "msg": "hello public!"
    }
    return result


@app.get("/login")
def login():
    auth_url = f"{cfg['authorize_url']}" \
               f"?response_type=code&client_id={cfg['client_id']}" \
               f"&scope=openid profile email"
    return RedirectResponse(auth_url)


@app.get("/logout")
def logout():

    payload = {
        'client_id': cfg['client_id'],
        "post_logout_redirect_uri": cfg['redirect_uri']
    }
    return RedirectResponse(payload)
    response = requests.get(cfg['logout_url'], data=payload)
    print(f"status_code:{response.status_code}")

    if response.status_code == 200:
        print("success")
    else:
        print(f"failed: status-code:{response.status_code}, error-text:{response.text}")


@app.get(f"/config/{config_file}")
async def config(request: Request, config_file: str):
    return {"test": "test123"}


@app.get("/config_old")
async def config_old(request: Request):
    pretty_json = json.dumps(cfg, indent=2)
    print(pretty_json)
    return templates.TemplateResponse("config.html", {"request": request, "pretty_json": pretty_json})


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

