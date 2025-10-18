import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector

load_dotenv()

if os.getenv("GOOGLE_API_KEY") is None:
  print("Error: GOOGLE_API_KEY is not set.")
  exit()

print("API Key Loaded Successfully.")


# --- 1. define the knowledge base path ---
# The path to the directory containing our knowledge base (Streamlit docs)
DATA_PATH = "../data/streamlit_docs"

# PostgreSQL connection details
CONNECTION_STRING = "postgresql+psycopg2://admin:password@localhost:5432/helpmate"
COLLECTION_NAME = "streamlit_docs"

# --- 2. load the docs ---
# use DirectoryLoader to load all .md files from the specified path
# It uses UnstructuredMarkdownLoader for each file by default
loader = DirectoryLoader(DATA_PATH, glob="**/*.md", show_progress=True)
documents = loader.load()

# --- 3. chunk the Documents ---
# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1000,
  chunk_overlap=100,
)

# split the documents into chunks
chunked_documents = text_splitter.split_documents(documents)




# --- 4. print a confirmation ---
print(f"Successfully split {len(documents)} documents into {len(chunked_documents)} chunks.")

# optional: print the first chunk to see the result
if chunked_documents:
    print(f"First chunk content snippet: \n'{chunked_documents[0].page_content}'")
    print(f"\nMetadata of the first chunk: \n{chunked_documents[0].metadata}")


# --- 5. initialize Embeddings and Vector Store ---
print("Initializing embeddings model...")

# initialize the Google Generative AI embeddings model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

print("Initializing vector store...")
# initialize the PGVector store. This will create the table and store the embeddings if it doesn't exist
vectorstore = PGVector.from_documents(
    documents=chunked_documents,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)

# --- 6. Final Confirmation ---
print(f"Successfully embedded and stored {len(chunked_documents)} chunks in the '{COLLECTION_NAME}' collection.")