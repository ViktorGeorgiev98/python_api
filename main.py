from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():  # async is optional, it is used for asynchronous programming
    return {"message": "Hello World!"}
