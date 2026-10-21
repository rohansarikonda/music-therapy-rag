import ollama, json, chromadb

chroma_client = chromadb.PersistentClient(path='./chroma-db')
coll = chroma_client.get_or_create_collection("music-therapy-papers")
#ollama.embed(model="qwen3-embedding:0.6b", input="This is a test embedding")
with open("chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)
    for i in range(0, len(chunks), 32):
        chunk_batch = chunks[i:i+32]
        texts = [c["text"] for c in chunk_batch]
        emb = ollama.embed(model="qwen3-embedding:0.6b", input=texts)
        coll.upsert(
            ids=[c["id"] for c in chunk_batch],
            embeddings=emb['embeddings'],
            metadatas=[{
                "title": c["title"],
                "paper": c["paper"],
                "year": c["year"] if c["year"] else int(c["paper"][-4:]),
                "index": c["index"]
            } for c in chunk_batch],
            documents=texts
        )
        print(f"Inserted {i+len(chunk_batch)} chunks into ChromaDB")

print(coll.count())