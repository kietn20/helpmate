import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

if os.getenv("GOOGLE_API_KEY") is None:
  print("Error: GOOGLE_API_KEY is not set.")
  exit()

print("API Key Loaded Successfully.")


# --- 1. define the knowledge base path ---
# The path to the directory containing our knowledge base (Streamlit docs)
DATA_PATH = "../data/streamlit_docs"

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