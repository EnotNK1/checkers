from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api import router

app = FastAPI()
app.include_router(router)

# origins = [
#     "http://localhost:3000",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
#     allow_headers=["*"]
# )

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8080)