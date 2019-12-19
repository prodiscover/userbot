# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

from telethon import events
import asyncio
from userbot.events import register
from userbot import bot


@register(outgoing=True, pattern="^.ttf (.*)")
async def get(event):
    name = event.text[5:]
    m = await event.get_reply_message()
    with open(name, "w") as f:
        f.write(m.message)
    await event.delete()
    await bot.send_file(event.chat_id,name,force_document=True)
