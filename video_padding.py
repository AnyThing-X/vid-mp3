import logging
import tempfile
import traceback
import subprocess
import os
from os import environ
from time import time

from moviepy.editor import *
from telethon import TelegramClient, events, errors
from telethon.tl.types import DocumentAttributeVideo

logging.basicConfig(level=logging.WARNING)

api_id = environ["api_id"]
api_hash = environ["api_hash"]

client = TelegramClient("videoaddpic", api_id, api_hash)
client.start(bot_token=environ["bot_token"])


class Timer():
    def __init__(self, current):
        self.current = current
        self.action = "downloading"

    def set_current(self, current):
        self.current = current

    def get_current(self):
        return self.current

    def set_action(self, action):
        self.action = action

@client.on(events.NewMessage(func=lambda e: e.is_private, pattern="/start"))
async def start_it(event):
    await event.reply("✋ Welcome I Can Convert Video To Mp3 File :")
    
@client.on(events.NewMessage(func=lambda e: e.is_private and e.media))
async def tint_it(event):

    async def progress(cur, tot):
        if time() >= last.get_current() + 2:
            last.set_current(time())
            await message.edit(f'✅ Done {last.action} {round(100 * cur / tot, 2)}% ')

    with tempfile.TemporaryDirectory() as temp_directory:

        async with client.conversation(event.chat_id, timeout=None, total_timeout=None) as conv:
            try:

                message = await conv.send_message("Downloading... ⏳")

                last = Timer(time())

                media = await client.download_media(event.media, progress_callback=progress, file=temp_directory)
                audio = AudioFileClip(media)
                await message.edit("Uploaded ✅ Converting to Mp3file 🎙")
                #ffmpeg -i video.mp4 -b:a 192K -vn music.mp3
                subprocess.run(f'ffmpeg -i {media} -b:a 192K -vn "{temp_directory}/file.mp3"', shell=True)
                #subprocess.run(f'ffmpeg -i {media} "{temp_directory}/file.mp3"', shell=True)
                await message.edit("Downloading... ⏳")
                last.set_action("Downloading... ⏳")
                await client.send_file(event.chat_id, f"{temp_directory}/file.mp3", supports_streaming=True,
                                       progress_callback=progress)
                await message.delete()
                await conv.send_message("Done ✅")
                audio.close()
            except:
                traceback.print_exc()
                await event.reply("🚫 Something went wrong please try again.")
                try:
                    audio.close()
                except:
                    pass


client.run_until_disconnected()
