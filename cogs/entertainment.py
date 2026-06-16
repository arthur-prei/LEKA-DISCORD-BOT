from utility import create_image, load_data, save_data
from datetime import datetime, timezone
from discord.ext import commands
from asyncio import sleep
from typing import Literal
import aiohttp
import hashlib
import discord
import random
import csv
import os
import io



with open(os.getenv("CONDITIONAL_PHRASES"), encoding="utf-8") as file:
    reader = list(csv.reader(file, delimiter=","))
    leka_selfdraw_msg = [i for i in reader if i[0] == "leka"]
    common_draw_msg = [i for i in reader if i[0] == "sorteio"]
    bot_draw_msg = [i for i in reader if i[0] == "sorteio_bot"]
    followup_msg = [i for i in reader if i[0] == "sorteio_followup"]
    interaction_msg = [i for i in reader if i[0] == "interacao"]
    random_msg = [i for i in reader if i[0] == "aleatorio"]
    broken_ship_leka_msg = [i for i in reader if i[0] == "ship_leka15"]
    mended_ship_leka_msg = [i for i in reader if i[0] == "ship_leka65"]
    normal_ship_leka_msg = [i for i in reader if i[0] == "ship_leka95"]
    burning_ship_leka_msg = [i for i in reader if i[0] == "ship_leka100"]
    broken_couple_msg = [i for i in reader if i[0] == "ship15"]
    mended_couple_msg = [i for i in reader if i[0] == "ship65"]
    normal_couple_msg = [i for i in reader if i[0] == "ship95"]
    burning_couple_msg = [i for i in reader if i[0] == "ship100"]
    hyper_couple_msg = [i for i in reader if i[0] == "ship200"]
    low_leka_selflove_msg = [i for i in reader if i[0] == "leka_self15"]
    medium_leka_selflove_msg = [i for i in reader if i[0] == "leka_self65"]
    high_leka_selflove_msg = [i for i in reader if i[0] == "leka_self95"]
    max_leka_selflove_msg = [i for i in reader if i[0] == "leka_self100"]
    low_selflove_msg = [i for i in reader if i[0] == "self15"]
    medium_selflove_msg = [i for i in reader if i[0] == "self65"]
    high_selflove_msg = [i for i in reader if i[0] == "self95"]
    max_selflove_msg = [i for i in reader if i[0] == "self100"]

with open(os.getenv("DEMOTIVATIONAL_PHRASES"), encoding="utf-8") as file:
    demotivational_phrases = list(csv.reader(file, delimiter=","))[1:]

class Entertainment(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(name="frase_desmotivacional")
    async def tell_joke(self, interact: discord.Interaction):
        phrase = random.choice(demotivational_phrases)[1]

        await interact.response.send_message(phrase)
    

    # DRAW MEMBER - selects a random member in the server
    @discord.app_commands.command(name="sortear")
    async def draw_member(self, interact: discord.Interaction):
        all_members = interact.guild.members
        member = random.choice(all_members)
        if member.bot:
            if member.id == self.bot.user.id:
                message = random.choice(leka_selfdraw_msg)[1]
                await interact.response.send_message(message.replace("{user}", member.mention))
            else:
                message = random.choice(bot_draw_msg)[1]
                await interact.response.send_message(message.replace("{user}", member.mention))
            not_bots = [
                m for m in all_members if not m.bot
            ]
            await sleep(3)
            new_member = random.choice(not_bots)
            fp_message = random.choice(followup_msg)[1]
            await interact.followup.send(fp_message.replace("{user}", new_member.mention))
        else:
            message = random.choice(common_draw_msg)[1]
            await interact.response.send_message(message.replace("{user}", member.mention))
    


    @discord.app_commands.command(name="interação")
    async def draw_two_members(self, interact: discord.Interaction):
        all_members = [
            m for m in interact.guild.members if not m.bot
        ]
        member1 = random.choice(all_members)
        member2 = random.choice(list([m for m in all_members if not m == member1]))
        
        message = random.choice(interaction_msg)[1]
        await interact.response.send_message(message.replace("{user}", member1.mention).replace("{user2}", member2.mention))

                
    
    @discord.app_commands.command(name="ship")
    async def ship_members(
        self,
        interact: discord.Interaction,
        membro: discord.Member,
        membro2: discord.Member = None
    ):

        today = datetime.now(timezone.utc).strftime("%d-%m-%Y")

        if not membro2:
            combined = f"{membro.id}-{today}"
            is_self = True
            is_bot_self = is_self and membro.id == self.bot.user.id
        else:
            if membro.id == membro2.id:
                is_self = True
                is_bot_self = is_self and membro.id == self.bot.user.id
                combined = f"{membro.id}-{today}"
            else:
                is_self = False
                is_bot_self = False
                members = sorted([membro.id, membro2.id]) # sorted grants that member-member2 == member2-member
                combined = f"{members[0]}-{members[1]}-{today}" # Creates a variable that keeps the info between the members percentage and day
        
        
        # sha256 - fix hash value
        # % 101 limit between 0 and 100
        hash_value = hashlib.sha256(combined.encode()).hexdigest() # hexdigest returns a hash as a legible hexadecimal 
        percentage = int(hash_value, 16) % 101


        broken_heart = os.getenv("BROKEN_HEART")
        mended_heart = os.getenv("MENDED_HEART")
        normal_heart = os.getenv("NORMAL_HEART")
        flame_heart = os.getenv("FLAME_HEART")
        iridescent_heart = os.getenv("IRIDESCENT_HEART")
        perfect_couple = str(os.getenv("PERFECT_COUPLE"))

        try:
            if str(membro.id)+str(membro2.id) in perfect_couple or str(membro2.id)+str(membro.id) in perfect_couple:
                percentage = 200
        except AttributeError:
            pass

        if membro2:
            is_leka_chosen = membro.id == self.bot.user.id or membro2.id == self.bot.user.id

        if percentage < 15:
            emoji = broken_heart
            
            if is_bot_self:
                message_list = low_leka_selflove_msg
            elif is_self:
                message_list = low_selflove_msg
            else:
                if is_leka_chosen:
                    message_list = broken_ship_leka_msg
                else:
                    message_list = broken_couple_msg
            
        elif percentage < 65:
            emoji = mended_heart

            if is_bot_self:
                message_list = medium_leka_selflove_msg
            elif is_self:
                message_list = medium_selflove_msg
            else:
                if is_leka_chosen:
                    message_list = mended_ship_leka_msg
                else:
                    message_list = mended_couple_msg
            
        elif percentage < 95:
            emoji = normal_heart

            if is_bot_self:
                message_list = high_leka_selflove_msg
            elif is_self:
                message_list = high_selflove_msg
            else:
                if is_leka_chosen:
                    message_list = normal_ship_leka_msg
                else:
                    message_list = normal_couple_msg
        
        elif percentage == 200:
            emoji = iridescent_heart
            message_list = hyper_couple_msg
            
        else:
            emoji = flame_heart

            if is_bot_self:
                message_list = max_leka_selflove_msg
            elif is_self:
                message_list = max_selflove_msg
            else:
                if is_leka_chosen:
                    message_list = burning_ship_leka_msg
                else:
                    message_list = burning_couple_msg
        
        message = random.choice(message_list)[1]

        if not membro2 or membro.id == membro2.id:
            selflove_embed = discord.Embed(
                title="Vamos falar um pouco sobre amor próprio?",
                description=f"O amor próprio dessa pessoa é de: {percentage}%",
                color=discord.Color.pink()
            )
            selflove_embed.set_image(url=membro.display_avatar.url)
            selflove_embed.set_footer(text=message.replace("{user}", membro.name))
            return await interact.response.send_message(embed=selflove_embed)

        
        async with aiohttp.ClientSession() as session:
            async with session.get(membro.display_avatar.url) as r1, session.get(membro2.display_avatar.url) as r2:
                member_image = io.BytesIO(await r1.read())
                member2_image = io.BytesIO(await r2.read())


        buffer = create_image(
            image=member_image,
            image2=member2_image,
            emoji=emoji,
            base_height=300,
            padding_px=20
        )
        
        text = message.replace("{user1}", membro.name).replace("{user2}", membro2.name)
        ship_embed = discord.Embed(
            title="Sobre esses dois pombinhos...",
            description=f"Chance de sucesso do relacionamento: {percentage}%",
            color=discord.Color.pink()
            )
        
        file = discord.File(fp=buffer, filename="ship.png")
        ship_embed.set_footer(text=text)
        ship_embed.set_image(url="attachment://ship.png")
        await interact.response.send_message(embed=ship_embed, file=file)

        servers_list = load_data("./json/servers_ship.json")
        current_server = str(membro.guild.id)

        if current_server not in servers_list:
            servers_list[current_server] = {}
        
        if today not in servers_list[current_server]:
            servers_list[current_server][today] = []
        
        if members in servers_list[current_server][today]:
            return
        
        servers_list[current_server][today].append({
            "ship": members,
            "percentage": percentage
        })
        
        save_data("./json/servers_ship.json", servers_list)
    

    @discord.app_commands.command(name="depositar")
    async def deposit(self, interact: discord.Interaction, membro: discord.Member, nivel: Literal["leve", "media", "alta", "muito alta"]):   
        if membro.bot:
            return
    
        data = load_data("./json/user_points.json")
        server = str(interact.guild.id)

        if server not in data:
            data[server] = {}
            
        user_id = str(membro.id)

        if user_id not in data[server]:
            data[server][user_id]["current_points"] = 0
            data[server][user_id]["all_time_points"] = 0

        if nivel == "leve":
            data[server][user_id]["current_points"] += 5
            data[server][user_id]["all_time_points"] = 5
        
        elif nivel == "media":
            data[server][user_id]["current_points"] += 10
            data[server][user_id]["all_time_points"] = 10
        
        elif nivel == "alta":
            data[server][user_id]["current_points"] += 25
            data[server][user_id]["all_time_points"] = 25
        
        else:
            data[server][user_id]["current_points"] += 50
            data[server][user_id]["all_time_points"] = 50

        await interact.response.send_message(f"{membro.name.title()} recebeu uma quantidade **{nivel}** de pontos de luxúria")

        save_data("./json/user_points.json", data)


    @discord.app_commands.command(name="ver_pontos")
    async def check_points(self, interact: discord.Interaction, membro: discord.Member):
        if membro.bot:
            return
        
        data = load_data("./json/user_points.json")
        user_id = str(membro.id)
        server = str(interact.guild.id)

        if user_id not in data[server]:
            await interact.response.send_message("Parece que este usuário ainda não está na lista de depósitos. Tente /deposito e adicione pontos!")
            return

        await interact.response.send_message(f"No momento, {membro.name.title()} tem **{data[server][user_id]}** ponto(s) de luxúria!")


    @discord.app_commands.command(name="resenha")
    async def check_resenha(self, interact: discord.Interaction):
        await interact.response.send_message("Só um momento, deixa eu ver se a resenha tá liberada...")
        await sleep(5)
        chance = random.randint(1, 100)
        if chance <= 25:
            await interact.followup.send("Resenha liberada! ✨")
        else:
            await interact.followup.send("Resenha não liberada, desculpa gente 💔")
        


async def setup(bot):
    print("Cog Entertainment carregada!")
    await bot.add_cog(Entertainment(bot))
