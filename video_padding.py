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
    await event.reply("✋ مرحبا أرسل فيديو لا يزيد عن 2:20 دقيقة")
    
@client.on(events.NewMessage(func=lambda e: e.is_private and e.media))
async def tint_it(event):

    async def progress(cur, tot):
        if time() >= last.get_current() + 2:
            last.set_current(time())
            await message.edit(f'تم {last.action} {round(100 * cur / tot, 2)}% ')

    with tempfile.TemporaryDirectory() as temp_directory:

        async with client.conversation(event.chat_id, timeout=None, total_timeout=None) as conv:
            try:

                message = await conv.send_message("جار التحميل...")

                last = Timer(time())

                media = await client.download_media(event.media, progress_callback=progress, file=temp_directory)

                await message.edit("تم التحميل. جار إضافة الإطار إلى المقطع المرئي.")
                subprocess.run(f'ffmpeg -i {media} {temp_directory}/file.mp3', shell=True)

                await message.edit("جار التحميل.")
                last.set_action("التحميل")
                await client.send_file(event.chat_id, f"{temp_directory}/file.mp3", supports_streaming=True,
                                       progress_callback=progress)
                await conv.send_message("تم")
                video.close()
            except:
                traceback.print_exc()
                await event.reply("حدث خلل ما الرجاء التجربة مرة اخرى")
                try:
                    video.close()
                except:
                    pass


client.run_until_disconnected()
