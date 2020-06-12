import logging,os,tempfile,traceback,subprocess
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
    await event.reply("✋ Welcome I Can Convert 📽 Video To ⏯ Mp3 File :")
    
@client.on(events.NewMessage(func=lambda e: e.is_private and e.media))
async def tint_it(event):
    with tempfile.TemporaryDirectory() as temp_directory:
        async with client.conversation(event.chat_id, timeout=None, total_timeout=None) as conv:
            try:
                message = await conv.send_message("📥 Downloading ... ⏳")
                last = Timer(time())
                media = await client.download_media(event.media,file=temp_directory)
                audio = AudioFileClip(media)
                await message.edit("⏳ 🔄 Converting to Mp3file 🎙")
                subprocess.run(f'ffmpeg -i {media} -vn -acodec libmp3lame -ac 2 -ab 160k -ar 48000 "{temp_directory}/file.mp3"', shell=True)
                await message.edit("📤 Uploading ... ⏳")
                await client.send_file(event.chat_id, f"{temp_directory}/file.mp3", supports_streaming=True,
                                       reply_to=conv.message.reply_to_msg_id)
                await message.delete()
                audio.close()
            except:
                traceback.print_exc()
                await event.reply("🚫 Something went wrong please try again.")
                try:
                    audio.close()
                except:
                    pass

client.run_until_disconnected()
