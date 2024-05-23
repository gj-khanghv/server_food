import pymongo
from bson import ObjectId

def connect_mongo(top_predictions):
    client = pymongo.MongoClient("mongodb+srv://thienphamchi060200:CGlRxGHgmxPNmUfe@imagefood.skf4i1y.mongodb.net/?retryWrites=true&w=majority&appName=ImageFood")  # Local connection example
    database = client["InfoFood"]
    collection = database["InfoFood"]
    object_ids = [ObjectId(oid) for oid in top_predictions]
    matching_documents = collection.find({'_id': {'$in': object_ids}})
    json_documents = []
    for document in matching_documents:
        # Convert ObjectId to string for serialization
        document['_id'] = str(document['_id'])
        # Append the JSON representation of the document to the list
        tmp_d = {
            "id": str(document['_id']),
            "Ten_mon_an": document["Ten_mon_an"],
            "mo_ta": document['mo_ta'],
            "nguyen_lieu": document['nguyen_lieu'],
            "so_che": document['so_che'],
            "thuc_hien": document['thuc_hien'],
            "cach_dung": document['cach_dung'],
            "mach_nho": document.get('mach_nho', []),
        }
        json_documents.append(tmp_d)
        
    client.close()
    return json_documents

# # Replaceith your connection details
# # For MongoDB Atlas, use your connection string

# # Access the database
# database = client["mydatabase"]

# # Access a collection within the database
# collection = database["mycollection"]

# # Example operations:

# # Insert a document
# new_document = {"name": "Alice", "age": 30}
# collection.insert_one(new_document)

# # Find documents with "name" as "John"
# documents = collection.find({"name": "John"})

# # Print the retrieved documents (modify as needed)
# for doc in documents:
#     print(doc)

