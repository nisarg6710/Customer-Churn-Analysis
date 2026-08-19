from pathlib import Path

# from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge_base"

VECTORSTORE_DIR = BASE_DIR / "data" / "vectorstore"


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# def build_retriever():

#     documents = []

#     # Load all business knowledge documents
#     for file in KNOWLEDGE_DIR.glob("*.txt"):

#         loader = TextLoader(
#             str(file),
#             encoding="utf-8"
#         )

#         documents.extend(loader.load())

#     if not documents:
#         raise ValueError(
#             "No knowledge-base documents found."
#         )

#     # Split documents into smaller chunks
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=700,
#         chunk_overlap=100
#     )

#     chunks = splitter.split_documents(documents)

#     print(f"Loaded documents: {len(documents)}")
#     print(f"Created chunks: {len(chunks)}")

#     # Local HuggingFace embedding model
#     embeddings = get_embeddings()

#     # Create FAISS vector store
#     vectorstore = FAISS.from_documents(
#         chunks,
#         embeddings
#     )

#     # Save vector store locally
#     VECTORSTORE_DIR.mkdir(
#         parents=True,
#         exist_ok=True
#     )

#     vectorstore.save_local(
#         str(VECTORSTORE_DIR)
#     )

#     print(
#         f"Vector store saved to: {VECTORSTORE_DIR}"
#     )

#     return vectorstore.as_retriever(
#         search_kwargs={"k": 4}
#     )



def load_retriever():

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )