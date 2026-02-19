from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.auth_routes import router as auth_router
from src.api.routes.search_routes import router as search_router
from src.api.routes.ticket_routes import router as ticket_router

app = FastAPI()


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://sistema-de-chamados-d8tf.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(search_router)
app.include_router(ticket_router)


@app.get("/ping")
def ping():
    return {"ok": True}
