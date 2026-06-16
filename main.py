import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

class Leka(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

        with open("./json/guild_config.json", "r") as file:
            self.guild_config = json.load(file)
    

    async def load_cogs(self):
        
        try:
            print("Carregando Utils...")
            for file in os.listdir("./utils"):
                print("Arquivo encontrado: ", file)
                if file.endswith(".py"):
                    print("Carregando: ", file)
                    await self.load_extension(f"utils.{file[:-3]}")

            print("Carregando Cogs...")
            for file in os.listdir("./cogs"):
                print("Arquivo encontrado: ", file)
                if file.endswith(".py"):
                    print("Carregando: ", file)
                    await self.load_extension(f"cogs.{file[:-3]}")
            
            for guild_id in self.guild_config:    
                guild = discord.Object(id=int(guild_id))
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)

        except discord.ext.commands.errors.ExtensionAlreadyLoaded:
            print("Cogs já carregadas!")


    async def on_ready(self):
        await self.load_cogs()
        print(self.user.name, "inicializada com sucesso!")

bot = Leka()

if __name__ == "__main__":
    bot.run(TOKEN)