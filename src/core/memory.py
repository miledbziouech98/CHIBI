import os
import chromadb
from datetime import datetime

class YozuMemory:
    def __init__(self, memory_path="memory/"):
        self.memory_path = memory_path
        if not os.path.exists(self.memory_path):
            os.makedirs(self.memory_path)

        self.client = chromadb.PersistentClient(path=os.path.join(self.memory_path, "chroma"))
        self.collection = self.client.get_or_create_collection(name="yozu_thoughts")

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
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception:
            return None

    def search_obsidian(self, keyword):
        """Search specifically in the markdown files of the vault."""
        matches = []
        for root, dirs, files in os.walk(self.memory_path):
            for file in files:
                if file.endswith(".md"):
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        if keyword.lower() in content.lower():
                            matches.append({"file": file, "preview": content[:100]})
        return matches
