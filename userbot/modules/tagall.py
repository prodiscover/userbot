from telethon import TelegramClient, events
import asyncio
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from userbot import bot


@bot.on(events.NewMessage(pattern=r"^.tagall$", outgoing=True))
@bot.on(events.MessageEdited(pattern=r"^.tagall$", outgoing=True))
async def tagging_powerful(e):
    mentions = "@tagall"
    chat = await e.get_input_chat()
    async for x in bot.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await e.edit(mentions)
