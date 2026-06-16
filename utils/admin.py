from discord.ext import commands
import discord
import asyncio
import os

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild_config = bot.guild_config


    @discord.app_commands.command(name="synccogs")
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interact: discord.Interaction):
        await interact.response.send_message("Sincronizando...")
        guild_id = str(interact.guild.id)
        if guild_id not in self.guild_config:
            return await interact.followup.send("Servidor não encontrado! Sincronização não concluída.")
        
        guild = discord.Object(id=int(guild_id))
        self.bot.tree.copy_global_to(guild=guild)
        await self.bot.tree.sync(guild=discord.Object(id=int(guild_id)))
        await interact.followup.send("Sincronização concluída!")
    

    @discord.app_commands.command(name="reloadcogs")
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def reload(self, interact: discord.Interaction, cog:str = None):
        await interact.response.defer() # no timeout
        if cog:
            await self.bot.reload_extension(f"cogs.{cog}")
            return await interact.followup.send(cog, "recarregado!")
        
        results = list()
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                try:
                    await self.bot.reload_extension(f"cogs.{file[:-3]}")
                    results.append(f"✅ {file}")
                except Exception as error:
                    results.append(f"❌ {file} → {error}")
        await interact.followup.send("\n".join(results))
    

    @discord.app_commands.command(name="loadcogs")
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def load(self, interact: discord.Interaction, cog:str = None):
        await interact.response.defer() # no timeout
        if cog:
            await self.bot.load_extension(f"cogs.{cog}")
            return await interact.followup.send(cog, "carregado!")
        results = list()
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                try:
                    await self.bot.load_extension(f"cogs.{file[:-3]}")
                    results.append(f"✅ {file}")
                except Exception as error:
                    results.append(f"❌ {file} → {error}")
        await interact.followup.send("\n".join(results))
   
   
    @discord.app_commands.command(name="unloadcogs")
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def unload(self, interact: discord.Interaction, cog:str = None):
        await interact.response.defer() # no timeout
        if cog:
            await self.bot.unload_extension(f"cogs.{cog}")
            return await interact.followup.send(cog, "descarregado!")
        results = list()
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                try:
                    await self.bot.unload_extension(f"cogs.{file[:-3]}")
                    results.append(f"✅ {file}")
                except Exception as error:
                    results.append(f"❌ {file} → {error}")
        await interact.followup.send("\n".join(results))
    

    @discord.app_commands.command(name="deletefrom")
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def delete_user_messages(self, interact: discord.Interaction, user_id: str):
        
        await interact.response.defer(ephemeral=True, thinking=True)
        
        guild = interact.guild
        int_user_id = int(user_id)

        try:
            user = await self.bot.fetch_user(int_user_id)
            username = user.name
        except discord.NotFound:
            await interact.followup.send("ID inválido!")

        if guild is None:
            await interact.followup.send("Esse comando só pode ser executado dentro de um servidor.")
            return


        status = await interact.followup.send(
            "Começando a limpar mensagens...",
            wait=True
        )

        deleted_messages = 0
        for channel in guild.text_channels:
            try:
                async for msg in channel.history(limit=None, oldest_first=True):
                    if msg.author.id == user.id:
                        await msg.delete()
                        deleted_messages += 1

                        await status.edit(
                            content=f"{deleted_messages} mensagens deletadas"
                        )

                        await asyncio.sleep(0.5)
            except Exception as e:
                await interact.followup.send(f"Desculpe, ocorreu um erro ao tentar executar a função. {e}")
                return
        
        await interact.followup.send(f"Deletei {deleted_messages} mensagens enviadas por {username} em todos os canais do servidor!")
                        

                


async def setup(bot):
    print("Cog Admin carregada!")
    await bot.add_cog(Admin(bot))