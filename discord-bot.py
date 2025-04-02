import discord
from discord.ext import commands
import dotenv
from scriptify import make_quote_image
import os 
# Load .env file
dotenv.load_dotenv()

# Get the token
TOKEN = dotenv.get_key('.env', 'TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

# Create bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def quote(ctx, *, quote_input):
    # Ensure the folder exists
    save_folder = "images"
    os.makedirs(save_folder, exist_ok=True)
    
    # Define the file path
    output_path = os.path.join(save_folder, f"{ctx.author.id}.jpg")
    
    try:
        make_quote_image(quote_input, output_path=output_path)
        await ctx.send(file=discord.File(output_path))
    except Exception as e:
        await ctx.send(f"Error creating image: {str(e)}")

bot.run(TOKEN)
