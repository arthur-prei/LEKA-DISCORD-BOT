from utility import load_data, save_data
from discord.ext import commands
import discord
import os

TARGET_ROLE = os.getenv("TARGET_ROLE_ID")

class LekaStore(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild_config = bot.guild_config
    
    @discord.app_commands.command(name="leka_store_introduction")
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def leka_store_intro(self, interact: discord.Interaction):
        
        text = (
        "Olá! Sejam muito bem-vindos à minha lojinha! 🛒\n\n"
        "Aqui vocês vão poder comprar várias coisinhas divertidas pra usar no servidor,\n"
        "como comandos e cargos especiais somente pra você! >///<\n\n"
        "Aqui também será possível visualizar o ranking de pontos do servidor,\n"
        "onde todos estarão rankeados 👀"
    )

        guild_id = str(interact.guild.id)
        if guild_id not in self.guild_config:
            return
        config = self.guild_config[guild_id]

        channel = interact.guild.get_channel(config["leka_store"])

        if channel:
            await channel.send(text)

            await interact.response.send_message("Mensagem enviada na Lojinha!")
    

    @discord.app_commands.command(name="target", description="faz a Leka responder as próximas 10 mensagens do membro")
    @discord.app_commands.describe(humor="como a Leka vai tratar essa pessoa")
    @discord.app_commands.checks.has_role(TARGET_ROLE)
    async def target(self, interact: discord.Interaction, membro: discord.Member, humor: str):
        
        users = load_data("./json/targeted_users.json")
        
        member = str(membro.id)
        if member == str(self.bot.user.id):
            return await interact.response.send_message("Ei! Você não pode me marcar não, querido!")

        server = str(membro.guild.id)

        if server not in users:
            users[server] = {}
        
        if member not in users[server]:
            users[server][member] = {}

        users[server][member]["mood"] = humor
        users[server][member]["message_count"] = 10

        save_data("./json/targeted_users.json", users)
        await interact.response.send_message("Já tá marcado!")
        

async def setup(bot):
    print("Cog LekaStore carregada!")
    await bot.add_cog(LekaStore(bot))