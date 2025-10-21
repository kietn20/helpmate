import os
import discord
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores.pgvector import PGVector
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if DISCORD_BOT_TOKEN is None:
    print("Error: DISCORD_BOT_TOKEN is not set.")
    exit()


# connection string to PostgreSQL database
CONNECTION_STRING = "postgresql+psycopg2://admin:password@localhost:5432/helpmate"
COLLECTION_NAME = "streamlit_docs"

# initialize the embeddings model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# initialize the PGVector store
vectorstore = PGVector(
    connection_string=CONNECTION_STRING,
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
)

# create a retriever from the vector store
retriever = vectorstore.as_retriever()

# initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.3)

template = """You are 'Helpmate,' a friendly and expert support agent for Streamlit.
Using the following CONTEXT from the official documentation, please provide a clear and helpful answer to the user's QUESTION.
If the context is not sufficient, say that you don't have enough information to answer. Do not make up information.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])





intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)



# --- Defining Bot events ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')



# defining the RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        # have to extract the user's question aka removing the bot's mention part
        user_question = message.content.replace(f'<@!{bot.user.id}>', '').strip()
        
        # show a "typing..." indicator to the user
        async with message.channel.typing():
            try:
                # invoke the RAG chain
                response = rag_chain.invoke(user_question)
                
                # for discord message length limit
                if len(response) > 2000:
                    # split the response into chunks of 2000 characters
                    chunks = [response[i:i + 2000] for i in range(0, len(response), 2000)]
                    for i, chunk in enumerate(chunks):
                        # send the first message as a reply to the user's question
                        if i == 0:
                            await message.reply(chunk)
                        # send subsequent messages in the channel
                        else:
                            await message.channel.send(chunk)
                else:
                    await message.reply(response)

            except Exception as e:
                await message.channel.send(f"Sorry, an error occurred: {e}")
                print(f"Error invoking RAG chain: {e}")




# --- running the Bot ---
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)