from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend running on Vercel 🚀"}

handler = Mangum(app)
 