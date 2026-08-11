import chromadb

class Delete_chroma_db:

    def __init__(self):

        self.client = chromadb.HttpClient(
            host="localhost",
            port=8001
        )

        self.collection_name = "rag_docs"

    def delete_collection(self):

        try:
            self.client.delete_collection(
                name="rag_docs"
            )

            return f"Deleted collection: {self.collection_name}"
            
        except Exception as e:
            return f"Collection delete failed: {e}"


if __name__ == "__main__":
    delete_db = Delete_chroma_db()
    print(delete_db.delete_collection())