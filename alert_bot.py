import discord
import os
import time
import asyncio
from discord.ext import tasks

TOKEN = 'SENIN_BOT_TOKENIN_BURAYA_GELECEK'
CHANNEL_ID = (CHANNEL_ID)
LOG_FILE_PATH = 'latest.log' 

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_pos = 0

@client.event
async def on_ready():
    print(f'{client.user} olarak giriş yapıldı!')
    check_logs.start()

@tasks.loop(seconds=5)
async def check_logs():
    global last_pos
    try:
        if not os.path.exists(LOG_FILE_PATH):
            print(f"Hata: {LOG_FILE_PATH} bulunamadı.")
            return

        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as file:
            file.seek(last_pos)
            new_lines = file.readlines()
            last_pos = file.tell()

            if new_lines:
                channel = client.get_channel(CHANNEL_ID)
                if channel:
                    for line in new_lines:
                        if "Vulcan" in line or "Grim" in line or "GrimAAC" in line:
                            formatted_message = f"🚨 **Hile Uyarısı!**\n```{line.strip()}```"
                            await channel.send(formatted_message)
                            await asyncio.sleep(0.5)

    except Exception as e:
        print(f"Log okuma hatası: {e}")

client.run(TOKEN)
