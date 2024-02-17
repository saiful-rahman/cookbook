import typer
import jwt

SECRET_KEY = "top-secret"
ALGORITHM = "HS256"

app = typer.Typer()


# $ python jwt/jwt-example.py encode '{"username": "ringo", "pin": 1676261200}'
@app.command()
def encode(data):
    payload = eval(data)
    encoded_payload = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_payload)


# $ python jwt/jwt-example.py decode eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJpbmdvIiwicGluIjoxNjc2MjYxMjAwfQ.CKXUe2U0Hv0DuIXnYCvoZONaEGx2JJ7jxxRPIikn1fg
@app.command()
def decode(encoded_payload):
    decoded_payload = jwt.decode(encoded_payload, SECRET_KEY, algorithms=ALGORITHM)
    print(decoded_payload)


if __name__ == "__main__":
    app()
