import os
import json
from types import SimpleNamespace
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request
from starlette.templating import Jinja2Templates

from algoliasearch.search_client import SearchClient

from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

load_dotenv()

app = FastAPI()

client = SearchClient.create(
    os.getenv("ALGOLIA_APP_ID"), os.getenv("ALGOLIA_ADMIN_API_KEY")
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/add")
async def add(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    
    
    try:
        new_camp = json.loads(body, object_hook=lambda d: models.Camp(**d))
    except:
        return {"error": "Could not add to db"}

    
    db.add(new_camp)
    db.commit()

    return new_camp


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
