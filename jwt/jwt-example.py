import typer
import jwt
import json

app = typer.Typer()

with open("config/native-app.json", "r") as config_file:
    cfg = json.load(config_file)


# $ python jwt/jwt-example.py encode '{"username": "ringo", "pin": 1676261200}'
@app.command()
def encode(data):
    payload = eval(data)
    encoded_payload = jwt.encode(payload, cfg['jwt_secret'], algorithm=cfg['jwt_algorithm'])
    print(encoded_payload)


# $ python jwt/jwt-example.py decode blurb
@app.command()
def decode(encoded_payload):
    decoded_payload = jwt.decode(encoded_payload, cfg['jwt_secret'], algorithms=cfg['jwt_algorithm'])
    print(decoded_payload)


if __name__ == "__main__":
    app()
