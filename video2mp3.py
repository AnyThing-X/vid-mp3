import logging
import random
import string
import os
import traceback
import subprocess
from os import environ
from moviepy.editor import *
from telethon import TelegramClient, events, errors
from telethon.tl.types import DocumentAttributeVideo
logging.basicConfig(level=logging.WARNING)
api_id = 17349
api_hash = "344583e45741c457fe1862106095a5eb"
client = TelegramClient("video2mp3", api_id, api_hash)
client.start(bot_token='925523949:AAHv7u7vYkqlq7TACCM25S8VNUlJjobkSDQ')
api_id = environ["api_id"]
api_hash = environ["api_hash"]
client = TelegramClient("video2mp3", api_id, api_hash)
client.start(bot_token=environ["bot_token"])
rand = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
in_use = False


@client.on(events.NewMessage(func=lambda e: e.is_private, pattern="/start"))
async def start_it(event):
    await event.reply("✋ Welcome I Can Convert 📽 Video To ⏯ Mp3 File :")


@client.on(events.NewMessage(func=lambda e: e.is_private and e.media))
async def tint_it(event):
    try:
        global in_use
        if in_use:
            await event.reply(f"البوت حاليا مستخدم من شخص")
            return
        in_use = True
        message = await event.reply("🔄 Processing : 📥 Downloading ...")
        media = await client.download_media(event.media)
        await message.edit("🔄 Processing : Converting to Mp3 file 🎙")
        subprocess.run(
            f'ffmpeg -i {media} -vn -ac 2 -ar 44100 -ab 200k -f mp3 {rand}.mp3', shell=True)
        await message.edit("🔄 Processing : 📤 Uploading ... ⏳")
        await client.send_file(event.chat_id, f"{rand}.mp3", supports_streaming=True, reply_to=event.message.id)
        await message.delete()
        os.remove(media)
        os.remove(f"{rand}.mp3")
    except:
        traceback.print_exc()
        os.remove(media)
        await event.reply("🚫 Something went wrong please try again.")
    finally:
        in_use = False
client.run_until_disconnected()
