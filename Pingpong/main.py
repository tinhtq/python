from fastapi import FastAPI
import uvicorn

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/")
def default():
    return {"message": "default"}

if __name__ == "__main__":
    # Start Uvicorn server when running this file
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
