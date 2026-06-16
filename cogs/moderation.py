# LEKA MODERATION COMMANDS
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import discord
import random
import csv
import os

with open(os.getenv("CONDITIONAL_PHRASES"), encoding="utf-8") as file:
    reader = list(csv.reader(file, delimiter=","))
    ban_msg = [i for i in reader if i[0] == "ban"]
    kick_msg = [i for i in reader if i[0] == "kick"]
    leave_msg = [i for i in reader if i[0] == "left"]
    unban_msg = [i for i in reader if i[0] == "unban"]

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild_config = bot.guild_config
        

    # ON MEMBER REMOVE - Everytime a member left, was kicked/banned
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):

        guild_id = str(member.guild.id)
        if guild_id not in self.guild_config:
            return
        config = self.guild_config[guild_id]

        channel = member.guild.get_channel(config["exit_channel"])
        current_time = datetime.now(timezone.utc)
        log_found = False

        if channel:
            async for entry in member.guild.audit_logs(limit=5):
                if entry.target.id == member.id:
                    if current_time - entry.created_at < timedelta(seconds=5):
                        log_found = True
                        if entry.action == discord.AuditLogAction.kick:
                            message = random.choice(kick_msg)[1]
                            await channel.send(message.replace("{user}", member.mention))
                            break

                        elif entry.action == discord.AuditLogAction.ban:
                            message = random.choice(ban_msg)[1]
                            await channel.send(message.replace("{user}", member.mention))
                            break
        if not log_found:
            if channel:
                message = random.choice(leave_msg)[1]
                await channel.send(message.replace("{user}", member.mention))


    # ON MEMBER UNBAN - Everytime a user is unbanned from the server
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):

        guild_id = str(guild.id)
        if guild_id not in self.guild_config:
            return
        config = self.guild_config[guild_id]

        channel = guild.get_channel(config["unban_channel"])
        if channel:
            message = random.choice(unban_msg)[1]
            await channel.send(message.replace("{user}", user.mention))


async def setup(bot):
    print("Cog Moderation carregada!")
    await bot.add_cog(Moderation(bot))
    