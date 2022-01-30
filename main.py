import asyncio

from pytgcalls import idle

from config import call_py
from MusicAndVideo.quote import arq
import os
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from pytgcalls import idle as pyidle
from config import bot

bot.start()
print("UserBot Started")
call_py.start()
print("Vc Client Started")
pyidle()
idle()
