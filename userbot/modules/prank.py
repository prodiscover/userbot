from telethon import events
import asyncio
from datetime import datetime
from userbot import CMD_HELP, bot

from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from telethon.errors import RightForbiddenError, UserIdInvalidError, ChatAdminRequiredError


@bot.on(events.NewMessage(pattern=r"prank\.promote ?(.*)", outgoing=True))
async def _(e):
    if event.fwd_from:
        return
    start = datetime.now()
    to_promote_id = None
    rights = ChatAdminRights(
        post_messages=True
    )
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_promote_id = r_mesg.sender_id
    elif input_str:
        to_promote_id = input_str
        await event.edit("Successfully Promoted")
        await asyncio.sleep(5)
        await event.delete()