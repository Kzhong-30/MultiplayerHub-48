from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, pets, posts, comments, matches, encyclopedia, nearby, services

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="宠物社交平台 API",
    description="一个完整的宠物社交平台后端服务",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(pets.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(matches.router)
app.include_router(encyclopedia.router)
app.include_router(nearby.router)
app.include_router(services.router)


@app.get("/")
def root():
    return {
        "message": "欢迎来到宠物社交平台 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
