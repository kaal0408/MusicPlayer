import os
import sys
from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR, SUDO_USERS

# System Uptime
START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("Minggu", 60 * 60 * 24 * 7),
    ("Hari", 60 * 60 * 24),
    ("Jam", 60 * 60),
    ("Menit", 60),
    ("Detik", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(filters.command(["ping"], prefixes=f"{HNDLR}"))
async def ping(client, m: Message):
    await m.delete()
    start = time()
    current_time = datetime.utcnow()
    m_reply = await m.reply_text("⚡")
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m_reply.edit(
        f"<b>😕😕 PONG</b> `{delta_ping * 1000:.3f} ms` \n<b>⏳ AKTIF</b> - `{uptime}`"
    )


@Client.on_message(
    filters.user(SUDO_USERS) & filters.command(["restart"], prefixes=f"{HNDLR}")
)
async def restart(client, m: Message):
    await m.delete()
    loli = await m.reply("1")
    await loli.edit("2")
    await loli.edit("3")
    await loli.edit("4")
    await loli.edit("5")
    await loli.edit("6")
    await loli.edit("7")
    await loli.edit("8")
    await loli.edit("9")
    await loli.edit("**✅ Userbot is restart💞**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@Client.on_message(filters.command(["mhelp"], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
    await m.delete()
    HELP = f"""
<b>👋 Hallo {m.from_user.mention}!

🛠 HELP MENU

⚡ COMMANDS FOR EVERYONE
• {HNDLR}mplay [song title | link youtube | balas file audio] - to play a song
• {HNDLR}vplay [video title | link youtube | balas file video] - to play a video
• {HNDLR}playlist to view playlist
• {HNDLR}ping - to check status....
• {HNDLR}mhelp - to see a list of commands
• {HNDLR}song - to download any song....
• {HNDLR}q/quote - to make a quote
• {HNDLR}tts  - To change text into voice 
• {HNDLR}id  - to get a user id
• {HNDLR}git  - to get a github account link
• {HNDLR}github  - to get a github account link
• {HNDLR}truth  - For truth dare game
• {HNDLR}dare  - For truth dare game

⚡ COMMANDS FOR ADMINS
• {HNDLR}resume - to continue playing a song or video
• {HNDLR}pause - to to pause the playback of a song or video
• {HNDLR}skip - to skip songs or videos
• {HNDLR}end - to end playback</b>
• {HNDLR}volume - volume  to increase decrease volume in voice chat

⚡ COMMANDS FOR SUDO
• {HNDLR}restart  - to restart the music and video bot
• {HNDLR}leavevc - to leave bot from voice chat

⚡ DEV - Loverboyxd, Manjeet SINGH
⚡ Powered by - @Murat_30_God
"""
    await m.reply(HELP)


