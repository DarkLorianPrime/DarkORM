from libraries.database.async_database import DatabaseORM
import fastapi

app = fastapi.FastAPI()


@app.on_event("startup")
async def startup():
    await DatabaseORM().connect()


@app.on_event("shutdown")
async def shutdown():
    await DatabaseORM().disconnect()


@app.get("/")
async def getter():
    return {"response": DatabaseORM().is_connected()}
