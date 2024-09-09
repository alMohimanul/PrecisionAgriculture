from fastapi import FastAPI
from detect import router as detect_app
from login import router as login_app
from db_connect import router as db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## API
app.include_router(login_app)
app.include_router(detect_app)
app.include_router(db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8081, reload=True)
