import chromadb
from datetime import datetime
import uuid

DB_PATH = "./chroma_db/hr_data"
client = chromadb.PersistentClient(path=DB_PATH)

# Collections
hr_collection = client.get_or_create_collection("hr_collection")
applicant_collection = client.get_or_create_collection("applicant_collection")


def save_hr_to_db(hr_data: dict):
    hr_id = f"hr_{uuid.uuid4().hex[:8]}"
    doc = f"{hr_data['name']} from {hr_data['company']} is hiring for {hr_data['position']}."

    hr_collection.add(
        documents=[doc],
        metadatas=[hr_data],
        ids=[hr_id],
    )
    return hr_id


def save_applicant_to_db(applicant_data: dict, resume_text: str):
    app_id = f"app_{uuid.uuid4().hex[:8]}"
    doc = f"{applicant_data['name']} has {applicant_data['yoe']} years of experience from {applicant_data['institute']}.\n\nResume:\n{resume_text}"

    applicant_collection.add(
        documents=[doc],
        metadatas=[applicant_data],
        ids=[app_id],
    )
    return app_id


def get_all_open_positions():
    return hr_collection.get(include=["metadatas", "documents"])


def search_hr_by_email(email):
    results = hr_collection.query(query_texts=[email], n_results=1)
    return results["metadatas"][0][0] if results["metadatas"] else None


def get_all_applicants():
    return applicant_collection.get(include=["metadatas", "documents"])

def get_latest_hr_entry():
    all_entries = hr_collection.get(include=["metadatas", "documents"])
    if not all_entries["metadatas"]:
        return {}
    latest_index = -1  # Last entry added
    return all_entries["metadatas"][latest_index]

def get_latest_applicant_entry():
    all_entries = applicant_collection.get(include=["metadatas", "documents"])
    if not all_entries["metadatas"]:
        return {}
    latest_index = -1  # Last entry added
    return all_entries["metadatas"][latest_index]
