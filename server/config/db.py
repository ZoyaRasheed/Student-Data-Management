import os
import pymongo  # type: ignore
from dotenv import load_dotenv # type: ignore
load_dotenv()

url = str(os.getenv('MONGO_DB_URL'))

try:
    client = pymongo.MongoClient(url, tlsAllowInvalidCertificates=True)
    db = client['marks'] 
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
