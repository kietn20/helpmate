# Helpmate: A RAG-Powered Autonomous Support AI Agent

Helpmate is an end-to-end, containerized AI agent that provides intelligent, context-aware support in Discord. It leverages a Retrieval-Augmented Generation (RAG) pipeline to answer user questions based on a custom knowledge base, ensuring accurate, relevant, and trustworthy responses without human intervention.

This project is a complete demonstration of building and deploying a production-grade AI system, from data ingestion to a live, interactive user interface with a full feedback loop.

## Live Demo

![Demo Image](https://github.com/kietn20/helpmate/blob/main/demo.gif)

## Key Features

-   **🤖 Intelligent RAG Pipeline:** Goes beyond standard chatbots by retrieving relevant information from a custom knowledge base *before* generating an answer, preventing hallucination and providing sourced responses.
-   **💬 Live Discord Integration:** Seamlessly integrates into a Discord server, listening for mentions and replying to user questions in real-time.
-   **🧠 Swappable Knowledge Base:** Easily adaptable to any set of documents. While built with the Streamlit documentation, it can be configured to use your own notes, product docs, or any text-based content.
-   **🔌 Pluggable AI Models:** Designed for flexibility. Easily switch between different LLMs like Google Gemini, OpenAI's GPT, or Anthropic's Claude with minimal code changes.
-   **👍 Real-Time Feedback Loop:** After every answer, the bot adds 👍/👎 reactions, listens for user clicks, and logs the feedback to a PostgreSQL database for future analysis and model improvement.
-   **🐳 Fully Containerized:** The entire application stack (Python bot, PostgreSQL database) is managed by Docker and Docker Compose, allowing for one-command startup, consistent environments, and easy deployment.

## Technical Architecture

![Diagram](https://github.com/kietn20/helpmate/blob/main/diagram.png)

User Interaction Workflow:
1. User asks a question by mentioning @Helpmate in Discord.
2. The Bot generates a vector embedding of the user's question.
3. The Bot queries the PostgreSQL database with this embedding.
4. The Database returns the most relevant document chunks (context).
5. The Bot sends the question and context to the Gemini LLM to generate an answer.
6. The Bot posts the final answer to Discord and adds (👍/👎) reactions.
7. The User clicks a reaction, which is logged back to the database.


The system follows a modern RAG architecture:

1.  **Data Ingestion (Offline):** A Python script reads source documents, splits them into manageable chunks, generates vector embeddings using an AI model, and stores them in a `pgvector` enabled PostgreSQL database.
2.  **Live Inference (Online):**
    -   A user asks a question by mentioning the bot in Discord.
    -   The bot performs a similarity search on the user's question against the vector database to retrieve the most relevant document chunks (the "context").
    -   The bot injects the user's question and the retrieved context into a carefully crafted prompt.
    -   The complete prompt is sent to an LLM (e.g., Google Gemini) to generate a final, context-aware answer.
    -   The answer is sent back to the user in Discord.
3.  **Feedback Loop:**
    -   The bot adds reactions to its own answer.
    -   An event listener logs any user reactions (👍/👎) to a separate `feedback` table in the database, linking the feedback to the original question and answer.

## Tech Stack

-   **AI & Machine Learning:** LangChain, Google Gemini, `pgvector`
-   **Backend:** Python, `discord.py`
-   **Database:** PostgreSQL
-   **DevOps:** Docker, Docker Compose

---

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
-   A Discord account with a server you can manage.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/helpmate.git
cd helpmate
```

### 2. Set Up the Discord Bot

1.  Navigate to the [Discord Developer Portal](https://discord.com/developers/applications) and create a **New Application**.
2.  Go to the **"Bot"** tab and click **"Add Bot"**.
3.  **Reset the Token** to get your `DISCORD_BOT_TOKEN`.
4.  Enable the **MESSAGE CONTENT INTENT** under "Privileged Gateway Intents".
5.  Go to the **"OAuth2" -> "URL Generator"** tab. Select the `bot` scope and grant the `View Channels`, `Send Messages`, and `Add Reactions` permissions.
6.  Copy the generated URL and use it to invite the bot to your server.

### 3. Configure Environment Variables

Create a file named `.env` in the root of the project and add your secret keys.

```env
# .env file

# Get this from the Discord Developer Portal
DISCORD_BOT_TOKEN="your-discord-bot-token"

# Get this from Google AI Studio or your chosen provider
GOOGLE_API_KEY="your-google-api-key"
```

### 4. Ingest the Knowledge Base

This is a one-time setup step to populate the database.

1.  **Start the database container:**
    ```bash
    docker-compose up -d db
    ```
2.  **Create a Python virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Run the ingestion script:**
    ```bash
    python3 src/ingest_data.py
    ```    This will read the files in `data/`, create embeddings, and store them in the database.

### 5. Run the Full Application

Now, run the entire containerized application stack.

```bash
docker-compose up --build
```

The Helpmate bot should now be online and ready to answer questions in your Discord server!

---

## Flexibility & Customization

### Using a Different Knowledge Base

Helpmate is designed to be data-agnostic. To use your own knowledge base:

1.  **Add Your Files:** Place your source documents (e.g., `.md`, `.txt` files) into a new folder inside the `data/` directory.
2.  **Update the Path:** In `src/ingest_data.py`, change the `DATA_PATH` variable to point to your new folder.
3.  **Re-ingest:** Shut down the containers (`docker-compose down`), clear the database volume (`docker volume rm helpmate_pg_data`), and re-run the ingestion steps from above.

### Using a Different LLM (e.g., OpenAI, Claude)

Thanks to LangChain, swapping models is simple. For example, to switch to OpenAI's GPT-4:

1.  **Install the Library:** Add `langchain-openai` to your `requirements.txt` file.
2.  **Update Environment:** Add your `OPENAI_API_KEY` to the `.env` file.
3.  **Modify the Code:** In `src/ingest_data.py` and `src/bot.py`, replace the Google initializations with the OpenAI equivalents:

    ```python
    # from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI

    # ...

    # embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    embeddings = OpenAIEmbeddings()

    # llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", temperature=0.3)
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3)
    ```

4.  **Rebuild and Run:** `docker-compose up --build`.

## Future Improvements

-   **Conversational Memory:** Allow users to ask follow-up questions.
-   **Source Citing:** Include links to the source documents from which the answer was derived.
-   **Web UI:** Build a simple Streamlit or Flask front-end to interact with the RAG agent outside of Discord.
-   **Cloud Deployment:** Deploy the Docker Compose stack to a cloud provider like AWS EC2 or DigitalOcean.
