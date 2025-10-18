import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader


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


print(f"Successfully loaded {len(documents)} documents.")



# print the first few chars of the first document to verify
if documents:
  print(f"First document content snippet: \n'{documents[0].page_content[:200]}'")