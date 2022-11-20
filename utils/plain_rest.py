from fastapi import Body, FastAPI
import uvicorn

app = FastAPI()


@app.post("/insert")
async def insert(payload: dict = Body(...)):
    print(f'Log: {payload}')	

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
