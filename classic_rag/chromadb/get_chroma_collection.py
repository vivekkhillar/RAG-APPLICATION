import chromadb

client = chromadb.HttpClient(
    host="localhost",
    port=8001
)

collections = client.list_collections()

for collection in collections:
    print(collection.name)

