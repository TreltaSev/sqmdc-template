# === Core ===
import sys
import uvicorn
sys.dont_write_bytecode = True

# === Utils ===
from utils.console import console
from utils.mongo.Client import MongoClient

from utils.app import App
app = App(__file__)

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/items/{item_id}")
def read_items(item_id: int):
    return {"item_id": item_id, "ok": "hi again"}

app.register_routers()

console.info("Starting app...")
uvicorn.run(app, **app.config)
