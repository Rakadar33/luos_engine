from fastapi import FastAPI
from app.api import ping, regression, asyncr

# Main API declaration
#'''
#aqua_api_version= '/api/v1'
#aqua_app = FastAPI(root_path=aqua_api_version)
#'''
aqua_app = FastAPI()

# Route APIs
aqua_app.include_router(ping.router)
aqua_app.include_router(regression.router)
aqua_app.include_router(asyncr.router)
