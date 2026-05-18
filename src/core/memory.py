import os
import chromadb
from datetime import datetime

class ChibiMemory:
    def __init__(self, memory_path="memory/"):
        self.memory_path = memory_path
        if not os.path.exists(self.memory_path):
            os.makedirs(self.memory_path)

        self.client = chromadb.PersistentClient(path=os.path.join(self.memory_path, "chroma"))
        self.collection = self.client.get_or_create_collection(name="chibi_thoughts")

    def save_thought(self, title, content, tags=None):
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{title.replace(' ', '_')}.md"
        filepath = os.path.join(self.memory_path, filename)

        with open(filepath, "w") as f:
            f.write(f"# {title}\n")
            f.write(f"Date: {datetime.now()}\n")
            if tags:
                f.write(f"Tags: {', '.join(tags)}\n")
            f.write("\n")
            f.write(content)

        # Add to semantic search
        self.collection.add(
            documents=[content],
            metadatas=[{"title": title, "tags": str(tags)}],
            ids=[filename]
        )

    def retrieve_relevant(self, query, n_results=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
