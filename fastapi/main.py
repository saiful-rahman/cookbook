from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import json
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

with open("../config/native-app.json", "r") as config_file:
    cfg = json.load(config_file)

templates = Jinja2Templates(directory="templates")


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


@app.get("/config")
async def config(request: Request):
    pretty_json = json.dumps(cfg, indent=2)
    print(pretty_json)
    return templates.TemplateResponse("config.html", {"request": request, "pretty_json": pretty_json})


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

