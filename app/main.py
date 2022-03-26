from fastapi import FastAPI
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, post, auth, vote
from . import models

models.Base.metadata.create_all(bind = engine)
app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {'msg':'Hello World'}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


