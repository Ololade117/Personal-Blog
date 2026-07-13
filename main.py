from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def home():
    return {"message:" "Personal Blog API is running"}