# ALL LEKA EVENTS
from utility import load_data, save_data
from discord.ext import commands
from datetime import datetime
from openai import OpenAI
import discord
import random
import os

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.message_history = {}
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.guild_config = bot.guild_config


    # ON MEMBER JOIN - Every time a new member joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_id = str(member.guild.id)
        if guild_id not in self.guild_config:
            return
        config = self.guild_config[guild_id]

        channel = member.guild.get_channel(config["entrance_channel"])
        if channel:
            welcome_embed = discord.Embed(
                title="Bem vindo(a)! 🎉",
                description=f"Olá {member.mention}! Seja muito bem vindo(a) à {member.guild.name}! ❤️",
                color=discord.Color.dark_purple()
            )

            welcome_embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            welcome_embed.set_image(url=member.display_avatar.url)
            welcome_embed.set_footer(text=f"~ {self.bot.user.name} te manda beijinhos de boas vindas!")

            await channel.send(embed=welcome_embed)
        
        role = member.guild.get_role(config["role1"])
        
        if role:
            await member.add_roles(role)
    
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):

        if msg.author.bot:
            return

        today = datetime.now().strftime("%d-%m-%Y %H:%M")

        user = load_data("./json/user_points.json")
        server = str(msg.guild.id)
        user_id = str(msg.author.id)

        if server not in self.message_history:
            self.message_history[server] = []

        self.message_history[server].append(
            f"{msg.author.name}: {msg.content}"
        )
        
        self.message_history[server] = self.message_history[server][-15:]

        target = load_data("./json/targeted_users.json")
        user_data = target.get(server, {}).get(user_id)
        mood = ""

        if user_data:
            mood = user_data.get("mood")
            user_data["message_count"] -= 1
            
            if user_data["message_count"] <= 0:
                target[server].pop(user_id, None)

            save_data("./json/targeted_users.json", target)

        if server not in user:
            user[server] = {}

        if user_id not in user[server]:
            user[server][user_id] = 0
        
        user[server][user_id] += 2

        save_data("./json/user_points.json", user)

        history = self.message_history.get(server, [])

        with open("personality.txt", "r") as file:
            personality = file.read();
                
        trigger = random.randint(1, 100)

        content = msg.content.lower()

        extra = ""
        
        messages = [
            {"role": "system", "content": personality + extra}
        ]

        for i in history:
            messages.append({"role": "user", "content": i})
        
        messages.append({
            "role": "user",
            "content": f"[{today}] {msg.author.name}: {msg.content}"
        })
        

        if mood:
            extra = f"\nPRIORIDADE: Você tem um comportamento especial com este usuário: {mood}"
            should_reply = True

        elif "leka" in content:
            should_reply = True
        
        elif trigger <= 2:
            should_reply = True
        
        else:
            should_reply = False

        if should_reply:
            await msg.channel.typing()

            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )

            reply = response.choices[0].message.content
            
            await msg.reply(reply)


async def setup(bot):
    print("Cog Events carregada!")
    await bot.add_cog(Events(bot))