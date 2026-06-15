import os
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(BASE_DIR,"data","faiss_ifab_local_db")


MODEL_CACHE_DIR = os.path.join(BASE_DIR,"model_cache")

LOCAL_MODEL_NAME = "BAAI/bge-m3"

class LocalHuggingFaceEmbeddings(Embeddings):

    def __init__(self,model_name: str = LOCAL_MODEL_NAME):

        import torch

        device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading embedding model: {model_name} ({device})")

        self._model = SentenceTransformer(
            model_name,
            device=device,
            trust_remote_code=True,
            cache_folder=MODEL_CACHE_DIR
        )

    def embed_documents(self,texts: list[str]) -> list[list[float]]:

        embeddings = self._model.encode(texts,normalize_embeddings=True)

        return embeddings.tolist()

    def embed_query(self,text: str) -> list[float]:

        embedding = self._model.encode(text,normalize_embeddings=True)

        return embedding.tolist()

_embeddings = None
_vector_db = None
_retriever = None

def get_embeddings():

    global _embeddings

    if _embeddings is None:

        _embeddings = LocalHuggingFaceEmbeddings()

    return _embeddings

def get_vector_db():

    global _vector_db

    if _vector_db is None:

        print("Loading FAISS database...")

        _vector_db = FAISS.load_local(DB_PATH,get_embeddings(),allow_dangerous_deserialization=True)

        print("FAISS loaded successfully.")

    return _vector_db

def get_retriever():

    global _retriever

    if _retriever is None:

        _retriever = get_vector_db().as_retriever(search_kwargs={"k": 5})

    return _retriever


def retrieve_law_documents(question: str):

    retriever = get_retriever()

    docs = retriever.invoke(question)

    return docs

def query_law(question: str) -> str:

    docs = retrieve_law_documents(question)

    if not docs:

        return "Không tìm thấy điều luật phù hợp."

    results = []

    for idx, doc in enumerate(docs,start=1):

        metadata = doc.metadata

        source_file = metadata.get("source_file", "Unknown")

        printed_page = metadata.get("printed_page", "?")


        results.append(f"""
==============================
NGUỒN {idx}
==============================
Tài liệu      : {source_file}
Trang in      : {printed_page}
NỘI DUNG:

{doc.page_content}
""".strip()
        )

    return "\n\n".join(results)


def debug_metadata(question: str):

    docs = retrieve_law_documents(question)

    print(f"\nTìm thấy {len(docs)} chunk.\n")

    for idx, doc in enumerate(docs,start=1):

        print("=" * 80)
        print(f"CHUNK {idx}")
        print("=" * 80)

        print("\nMETADATA:")
        print(doc.metadata)

        print("\nCONTENT:")
        print(doc.page_content[:1000])

        print("\n")


if __name__ == "__main__":

    print("STEP 1")

    embeddings = get_embeddings()

    print("STEP 2")

    db = get_vector_db()

    print("STEP 3")

    retriever = get_retriever()

    print("STEP 4")

    docs = retriever.invoke(
        "Luật việt vị là gì?"
    )

    print("STEP 5")

    print("Docs found:", len(docs))