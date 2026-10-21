import ollama, chromadb

coll = chromadb.PersistentClient(path='./chroma-db').get_or_create_collection("music-therapy-papers")


def main():
    print("ask a question")
    s = input()
    print(search(s, k=20))


def search(question, k=5):
    emb = ollama.embed(model="qwen3-embedding:0.6b", input=question)
    results = coll.query(
        query_embeddings=emb['embeddings'],
        n_results=k,
        include=['metadatas', 'documents']
    )
    docs = results['documents'][0]
    metas = results['metadatas'][0]

    blocks = []
    for text, meta in zip(docs, metas):
        blocks.append(f"from {meta['paper']}:{text} ({meta['year']})")

    cont = "\n\n".join(blocks)
    res = generate(cont, question)
    return(res)

def generate(context, question):
    response = ollama.chat(
        model = "qwen3.5:9b",
        messages = [
            {
                "role": "system",
                "content": "For each claim that you make, cite the paper you got that information from. If there is no related information in the studies, do not make up information; just say that. Keep the answer as concise as possible. When sourcing the claim, you do not need to provide the quote as well, just the paper and year."
            },
            {
                "role": "user",
                "content": f"Using only the context, answer: {question}\nText: “{context}”."
            },
        ],
        think=False,
        options={"num_ctx": 8192}
    )
    return response['message']['content']

if __name__ == "__main__":
    main()