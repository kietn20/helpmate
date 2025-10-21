import os
import discord
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if DISCORD_BOT_TOKEN is None:
    print("Error: DISCORD_BOT_TOKEN is not set.")
    exit()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)



# --- defining Bot events ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    # have ignore messages sent by the bot itself to prevent loops
    if message.author == bot.user:
        return

    # check if the bot was mentioned in the message
    if bot.user.mentioned_in(message):
        await message.channel.send("I am online and I heard you!")




# --- running the Bot ---
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)