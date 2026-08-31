import os
import pymongo
import pandas as pd
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

uri = "mongodb+srv://shahbazkhan0246_db_user:crs1SGdhEKXOVcev@cluster0.p53cuqw.mongodb.net/?appName=Cluster0"

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

# Test connection
try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print(e)

# Push data
df = pd.read_csv(r'Network_Data\phishing.csv')  # ✅ your path
records = df.to_dict(orient="records")

db = client["NetworkSecurity"]
collection = db["Networkdata"]

collection.insert_many(records)
print(f"Inserted {len(records)} records into NetworkSecurity.Networkdata")