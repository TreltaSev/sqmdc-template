import pymongo
import pymongo.collection
import pymongo.database
from utils.helper.config import Yaml
from utils.console import console

class MongoClient:
    
    user = Yaml().get("database.username")
    passw = Yaml().get("database.password")
    uri = f"mongodb://{user}:{passw}@database:29345/localbulk"
    
    client: pymongo.MongoClient = pymongo.MongoClient(uri)
    
    console.info("Mongo Uri:", uri)
    
    database: pymongo.database.Database = client["localbulk"]
    
    # Collections
    sessions: pymongo.collection.Collection = database["sessions"]
    file_metas: pymongo.collection.Collection = database["file_metas"]