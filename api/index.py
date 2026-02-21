from fastapi import FastAPI, Response
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root(response: Response):
    response.headers["Content-Type"] = "application/json"
    return {"message": "Backend running on Vercel 🚀"}

handler = Mangum(app)  