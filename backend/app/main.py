import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import db

# origins = ["http://localhost:3000",
#            "http://localhost:8888",
#            "http://172.26.49.209:3000",
#            "http://172.26.49.209:8888"
#            ]

origins = [
                "http://192.168.56.1:3000",
                "http://192.168.56.1:8000",
                "http://192.168.56.1:8888"
           ]

def init_app():
    db.init()

    app = FastAPI(
        title="FTF WebView",
        description="List and control devices",
        version="1.0"
    )


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from app.controller import test
    from app.controller import tests
    from app.controller import stand
    from app.controller import props

    app.include_router(test.router)
    app.include_router(tests.router)
    app.include_router(stand.router)
    app.include_router(props.router)

    return app


app = init_app()


def start():
    """ Launched with 'poetry run start' at root level  """
    uvicorn.run("app.main:app", host="192.168.56.1", port=8000, reload=True)
