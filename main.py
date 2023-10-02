from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Request
import requests


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/getWorkbooks/")
async def get_Workbooks(info: Request):
    req_info = await info.json()
    print(req_info)
    userName = req_info["user_name"]
    pageStart = req_info["start"]
    pageCount = req_info["count"]

    url = f"https://public.tableau.com/public/apis/workbooks?profileName={userName}&start={pageStart}&count={pageCount}&visibility=NON_HIDDEN"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was not successful

        data = response.json()

        return data
    except requests.RequestException as e:
        return {"error": f"Failed to fetch data from the external API: {str(e)}"}


@app.post("/getProfile/")
async def get_Profile(info: Request):
    req_info = await info.json()
    print(req_info)
    # userName = req_info.user_name
    userName = req_info["user_name"]

    url = f"https://public.tableau.com/profile/api/{userName}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was not successful

        data = response.json()
        return data
    except requests.RequestException as e:
        return {"error": f"Failed to fetch data from the external API: {str(e)}"}
