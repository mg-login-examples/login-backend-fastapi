from appFactory import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8018, log_level="debug", reload=True, workers=2)
