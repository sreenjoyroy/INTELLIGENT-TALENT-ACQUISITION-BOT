import chromadb
from chromadb.utils import embedding_functions
import os

client = chromadb.PersistentClient(path="./chroma_db/hr_data")

collection = client.get_or_create_collection("hr_collection")

# Example HR entries
dummy_hrs = [
    {
        "name": "Alice Johnson",
        "recruiter_id": "HR101",
        "email": "alice@techcorp.com",
        "company": "TechCorp",
        "position": "Software Engineer"
    },
    {
        "name": "Bob Smith",
        "recruiter_id": "HR102",
        "email": "bob@greenai.io",
        "company": "GreenAI",
        "position": "AI Research Intern"
    },
    {
        "name": "Carol Lee",
        "recruiter_id": "HR103",
        "email": "carol@finboost.net",
        "company": "FinBoost",
        "position": "Backend Developer"
    }
]

def seed_hr_data():
    for idx, hr in enumerate(dummy_hrs):
        doc_id = f"hr_{idx}"
        metadata = {
            "name": hr["name"],
            "recruiter_id": hr["recruiter_id"],
            "email": hr["email"],
            "company": hr["company"],
            "position": hr["position"]
        }

        content = f"{hr['name']} from {hr['company']} is hiring for {hr['position']}."
        collection.add(documents=[content], metadatas=[metadata], ids=[doc_id])

    print("✅ Dummy HRs seeded to ChromaDB.")

if __name__ == "__main__":
    seed_hr_data()
