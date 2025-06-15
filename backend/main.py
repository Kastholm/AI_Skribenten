from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.prompt_router import router as prompt_router
from router.user_router import router as user_router
from router.site_router import router as site_router
from router.article_router import router as article_router
from router.admin.admin_router import router as admin_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "You're connected to the backend"}

app.include_router(user_router)
app.include_router(site_router)
app.include_router(prompt_router)
app.include_router(article_router)
app.include_router(admin_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)