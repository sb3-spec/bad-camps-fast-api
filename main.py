import os
import json
from types import SimpleNamespace
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates

from algoliasearch.search_client import SearchClient

from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

origins = [
    'http://localhost:5173',
    'http://localhost'
]

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = SearchClient.create(
    os.getenv("ALGOLIA_APP_ID"), os.getenv("ALGOLIA_ADMIN_API_KEY")
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except ConnectionError as err:
        print(err.args)
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/add")
async def add(request: Request, db: Session = Depends(get_db)):
    
    try:
        body = await request.body()
    except TypeError as err:
        print(err.args)
    
    
    try:
        new_camp = json.loads(body, object_hook=lambda d: models.Camp(**d))
    except ValueError as err:
        print(err.args)

    
    db.add(new_camp)
    db.commit()

    return {"message": "Camp added successfully."}


@app.get("/createIndex")
async def create_index(request: Request, db: Session = Depends(get_db)):
    index = client.init_index("dev_CAMPS")

    camps = db.query(models.Camp).all()

    new_camps = [{"name": camp.name, "description": camp.description} for camp in camps]

    index.replace_all_objects(new_camps, {"autoGenerateObjectIDIfNotExist": True})

    return camps


@app.get("/camps")
async def get_camps(request: Request, db: Session = Depends(get_db)):
    camps = db.query(models.Camp).all()

    return camps


@app.get("/camps/{camp_id}")
async def get_camp_by_id(camp_id: int, request: Request, db: Session = Depends(get_db), ):
    
    camps = db.query(models.Camp).get(camp_id)

    return camps
