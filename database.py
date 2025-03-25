# Database Handler
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class IncidentDB:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["Incident_Response"]
        self.collection = self.db["Incident_Details_1"]
    
    def store_incident(self, error_message, root_cause, solution_steps):
        document = {
            "error_message": error_message,
            "root_cause": root_cause,
            "solution_steps": solution_steps,
            "timestamp": datetime.utcnow()  # Fixed: Removed extra .datetime
        }
        return self.collection.insert_one(document).inserted_id
    
    def search_errors(self, error_message, limit=5):
        return list(self.collection.find(
            {"$text": {"$search": error_message}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(limit))