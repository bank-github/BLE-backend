from app.database import db_instance

registered_tags = []

def getTags_mac():
    global registered_tags # Ensure the global variable is modified
    tags = []
    doc = db_instance.get_collection("tags").find({})
    if doc:
        for rs in doc:
            tags.append(rs["tagMac"])
    registered_tags = tags
    
def get_registered():
    return registered_tags