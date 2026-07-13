import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


DATA_PATH = "data"
DB_PATH = "vectorstore"

# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def build_vector_database():
    """
    Loads all documents from the data folder,
    splits them into chunks,
    and stores them in ChromaDB.
    """

    loader = DirectoryLoader(
        DATA_PATH,
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )

    print(f"Indexed {len(chunks)} document chunks.")

    return vectordb


def load_vector_database():
    """
    Loads an existing ChromaDB database.
    """

    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )


def search_documents(query, k=3):
    """
    Searches the vector database for relevant documents.
    """

    vectordb = load_vector_database()

    results = vectordb.similarity_search(query, k=k)

    return results