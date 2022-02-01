
from __future__ import unicode_literals

import asyncio
import functools
import os
import subprocess
import traceback
from sys import version as pyver

# Initialize db
import db
db.init()

from pyrogram import filters, idle
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.raw.types import InputPeerChannel
from pyrogram.types import Message
from pytgcalls import GroupCall

from db import db

@app.on_message(filters.command("splay") & ~filters.private)
async def queuer(_, message):
    global running
    try:
        usage = "**Usage:**\n__**/splay Song_Name**__"
        if len(message.command) < 3:
            return await message.reply_text(usage, quote=False)
        text = message.text.split(None, 2)[1:]
        service = text[0].lower()
        song_name = text[1]
        requested_by = message.from_user.first_name
        services = ["saavn"]
        if service not in services:
            return await message.reply_text(usage, quote=False)
        await message.delete()
        chat_id = message.chat.id
        if chat_id not in db:
            db[chat_id] = {}

        if "queue" not in db[chat_id]:
            db[chat_id]["queue"] = asyncio.Queue()
        if not db[chat_id]["queue"].empty():
            await message.reply_text("__**Added To Queue.__**", quote=False)
        await db[chat_id]["queue"].put(
            {
                "service": savan
                "requested_by": requested_by,
                "query": song_name,
                "message": message,
            }
        )
        if "running" not in db[chat_id]:
            db[chat_id]["running"] = False
        if not db[chat_id]["running"]:
            db[chat_id]["running"] = True
            await start_queue(chat_id)
    except Exception as e:
        await message.reply_text(str(e), quote=False)
        e = traceback.format_exc()
        print(e)


@app.on_message(filters.command("dplay") & ~filters.private)
async def queuer(_, message):
    global running
    try:
        usage = "**Usage:**\n__**/dplay  Song_Name**__"
        if len(message.command) < 3:
            return await message.reply_text(usage, quote=False)
        text = message.text.split(None, 2)[1:]
        service = text[0].lower()
        song_name = text[1]
        requested_by = message.from_user.first_name
        services = ["saavn"]
        if service not in services:
            return await message.reply_text(usage, quote=False)
        await message.delete()
        chat_id = message.chat.id
        if chat_id not in db:
            db[chat_id] = {}

        if "queue" not in db[chat_id]:
            db[chat_id]["queue"] = asyncio.Queue()
        if not db[chat_id]["queue"].empty():
            await message.reply_text("__**Added To Queue.__**", quote=False)
        await db[chat_id]["queue"].put(
            {
                "service": deezer
                "requested_by": requested_by,
                "query": song_name,
                "message": message,
            }
        )
        if "running" not in db[chat_id]:
            db[chat_id]["running"] = False
        if not db[chat_id]["running"]:
            db[chat_id]["running"] = True
            await start_queue(chat_id)
    except Exception as e:
        await message.reply_text(str(e), quote=False)
        e = traceback.format_exc()
        print(e)



# Deezer


async def deezer(requested_by, query, message: Message):
    m = await message.reply_text(
        f"__**Searching for {query} on Deezer.**__", quote=False
    )
    songs = await arq.deezer(query, 1)
    if not songs.ok:
        return await m.edit(songs.result)
    songs = songs.result
    title = songs[0].title
    duration = convert_seconds(int(songs[0].duration))
    thumbnail = songs[0].thumbnail
    artist = songs[0].artist
    url = songs[0].url
    await m.edit("__**Downloading And Transcoding.**__")
    cover, _ = await asyncio.gather(
        generate_cover(
            requested_by, title, artist, duration, thumbnail, message.chat.id
        ),
        download_and_transcode_song(url, message.chat.id),
    )
    await m.delete()
    caption = (
        f"🏷 **Name:** [{title[:45]}]({url})\n⏳ **Duration:** {duration}\n"
        + f"🎧 **Requested By:** {message.from_user.mention}\n📡 **Platform:** Deezer"
    )
    m = await message.reply_photo(
        photo=cover,
        caption=caption,
    )
    os.remove(cover)
    duration = int(songs[0]["duration"])
    await pause_skip_watcher(m, duration, message.chat.id)
    await m.delete()


# saavn


async def saavn(requested_by, query, message):
    m = await message.reply_text(
        f"__**Searching for {query} on JioSaavn.**__", quote=False
    )
    songs = await arq.saavn(query)
    if not songs.ok:
        return await m.edit(songs.result)
    songs = songs.result
    sname = songs[0].song
    slink = songs[0].media_url
    ssingers = songs[0].singers
    sthumb = songs[0].image
    sduration = songs[0].duration
    sduration_converted = convert_seconds(int(sduration))
    await m.edit("__**Downloading And Transcoding.**__")
    cover, _ = await asyncio.gather(
        generate_cover(
            requested_by,
            sname,
            ssingers,
            sduration_converted,
            sthumb,
            message.chat.id,
        ),
        download_and_transcode_song(slink, message.chat.id),
    )
    await m.delete()
    caption = (
        f"🏷 **Name:** {sname[:45]}\n⏳ **Duration:** {sduration_converted}\n"
        + f"🎧 **Requested By:** {message.from_user.mention}\n📡 **Platform:** JioSaavn"
    )
    m = await message.reply_photo(
        photo=cover,
        caption=caption,
    )
    os.remove(cover)
    duration = int(sduration)
    await pause_skip_watcher(m, duration, message.chat.id)
    await m.delete()


@app.on_message(filters.command("joinvc") & ~filters.private)
async def joinvc(_, message):
    chat_id = message.chat.id
    if chat_id not in db:
        db[chat_id] = {}

    if "call" in db[chat_id]:
        return await message.reply_text(
            "__**Bot Is Already In The VC**__", quote=False
        )

@app.on_message(filters.command("leavevc") & ~filters.private)
async def leavevc(_, message):
    chat_id = message.chat.id
    if chat_id in db:
        if "call" in db[chat_id]:
            vc = db[chat_id]["call"]
            del db[chat_id]["call"]
            await vc.leave_current_group_call()
            await vc.stop()
    await message.reply_text("__**Left The Voice Chat**__", quote=False)


@app.on_message(filters.command("volume") & ~filters.private)
async def volume_bot(_, message):
    usage = "**Usage:**\n/volume [1-200]"
    chat_id = message.chat.id
    if chat_id not in db:
        return await message.reply_text("VC isn't started")
    if "call" not in db[chat_id]:
        return await message.reply_text("VC isn't started")
    vc = db[chat_id]["call"]
    if len(message.command) != 2:
        return await message.reply_text(usage, quote=False)
    volume = int(message.text.split(None, 1)[1])
    if (volume < 1) or (volume > 200):
        return await message.reply_text(usage, quote=False)
    try:
        await vc.set_my_volume(volume=volume)
    except ValueError:
        return await message.reply_text(usage, quote=False)
    await message.reply_text(f"**Volume Set To {volume}**", quote=False)
