# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for mentioning users. """

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K && @INF1N17Y

from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
import os
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from userbot import CMD_HELP, bot

@bot.on(events.NewMessage(pattern="^.mention ?(.*)", outgoing=True))
@bot.on(events.MessageEdited(pattern="^.mention ?(.*)", outgoing=True))
async def mention(event):
    """ For .mention, generates a permalink to a user's profile with custom caption. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if event.fwd_from:
            return
        input_str = event.pattern_match.group(1)
        target, mention_text = input_str.split(' ', 1)
        replied_user = await get_user(event, target)
        user_id = replied_user.user.id
        caption = """<a href='tg://user?id={}'>{}</a>""".format(
            user_id, str(mention_text))
        await event.edit(caption, parse_mode="HTML")


async def get_user(event, target):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = target

        if user.isnumeric():
            user = int(user)

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


CMD_HELP.update({
    "mention <username> <text>": "Generates the user's permanent link with custom text."
})
