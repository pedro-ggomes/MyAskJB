from langchain_community.embeddings import OllamaEmbeddings

def get_embedding_function() -> OllamaEmbeddings:
    embeddings = OllamaEmbeddings(model="mistral",show_progress=True)
    return embeddings 