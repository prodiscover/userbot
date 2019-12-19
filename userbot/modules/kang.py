# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for kanging stickers or making new ones. """

import io
import math
import urllib.request
from os import remove as DelFile

from PIL import Image
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto

from userbot import CMD_HELP, bot
from userbot.events import register
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
from telethon.tl.types import DocumentAttributeSticker

PACK_FULL = "Whoa! That's probably enough stickers for one pack, give it a break. \
A pack can't have more than 120 stickers at the moment."

CREATE_RESP = "  A <strong>Telegram</strong> user has created the \
<strong>Sticker&nbsp;Set</strong>."

@register(outgoing=True, pattern="^.kang")
async def kang(args):
    """ For .kang command, kangs stickers or creates new ones. """
    user = await bot.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = ""
    await args.edit("`Kanging...`")
    if message and message.media:
        # For kanging regular images
        if isinstance(message.media, MessageMediaPhoto):
            photo = io.BytesIO()
            photo = await bot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split('/'):
            photo = io.BytesIO()
            await bot.download_file(message.media.document, photo)
            # For kanging other sticker
            if (DocumentAttributeFilename(file_name='sticker.webp') in
                    message.media.document.attributes):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        # For kanging Animated Stickers
        elif (DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in
              message.media.document.attributes):
            await bot.download_file(message.media.document, 'AnimatedSticker.tgs')
            #
            # !!! HACK HACK HACK HACK !!!
            # We have to check both as Telegram constantly moving
            # the attributes between 0 and 1
            #
            try:
                emoji = message.media.document.attributes[0].alt
            except AttributeError:
                emoji = message.media.document.attributes[1].alt
            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await args.edit("`Unsupported File!`")
            return
    else:
        await args.edit("`Reply to photo to kang it bruh`")
        return

    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "🤔"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]  # User sent both
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                # User wants to push into different pack, but is okay with
                # thonk as emote.
                pack = int(splat[1])
            else:
                # User sent just custom emote, wants to push to default
                # pack
                emoji = splat[1]

        packname = f"a{user.id}_by_{user.username}_{pack}"
        packnick = f"@{user.username}'s userbot pack {pack}"
        cmd = '/newpack'
        file = io.BytesIO()

        if not is_anim:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            packname += "_anim"
            packnick += " animated"
            cmd = '/newanimated'

        response = urllib.request.urlopen(
            urllib.request.Request(f'http://t.me/addstickers/{packname}'))
        htmlstr = response.read().decode("utf8").split('\n')

        if CREATE_RESP not in htmlstr:
            async with bot.conversation('Stickers') as conv:
                await conv.send_message('/addsticker')
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                resp = await conv.get_response()
                while resp.text == PACK_FULL:
                    pack += 1
                    packname = f"a{user.id}_by_{user.username}_{pack}"
                    packnick = f"@{user.username}'s userbot pack {pack}"
                    await args.edit("`Switching to Pack " + str(pack) +
                                    " due to insufficient space`")
                    await conv.send_message(packname)
                    resp = await conv.get_response()
                    if resp.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file('AnimatedSticker.tgs', force_document=True)
                            DelFile('AnimatedSticker.tgs')
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await args.edit(
                            f"Sticker added in a Different Pack! This Pack is Newly created! \
                            Your pack can be found [here](t.me/addstickers/{packname})",
                            parse_mode='md')
                        return
                if is_anim:
                    await conv.send_file('AnimatedSticker.tgs', force_document=True)
                    DelFile('AnimatedSticker.tgs')
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                await conv.get_response()
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message('/done')
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await args.edit("Userbot sticker pack \
doesn't exist! Making a new one!")
            async with bot.conversation('Stickers') as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file('AnimatedSticker.tgs', force_document=True)
                    DelFile('AnimatedSticker.tgs')
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                await conv.get_response()
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)

        await args.edit(
            f"Sticker added! Your pack can be found [here](t.me/addstickers/{packname})",
            parse_mode='md')


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


@register(outgoing=True, pattern="^.stkrinfo$")
async def get_pack_info(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if not event.is_reply:
            await bot.update_message(event, PACKINFO_HELP)
            return
        rep_msg = await event.get_reply_message()
        if not rep_msg.document:
            await event.edit("`Reply to a sticker to get the pack details`")
            return
        stickerset_attr = rep_msg.document.attributes[1]
        if not isinstance(stickerset_attr, DocumentAttributeSticker):
            await event.edit("`This is not a sticker. Reply to a sticker.`")
            return
        get_stickerset = await bot(GetStickerSetRequest(InputStickerSetID(id=stickerset_attr.stickerset.id, access_hash=stickerset_attr.stickerset.access_hash)))
        pack_emojis = []
        for document_sticker in get_stickerset.packs:
            if document_sticker.emoticon not in pack_emojis:
                pack_emojis.append(document_sticker.emoticon)
        OUTPUT = f"**Sticker Title:** `{get_stickerset.set.title}\n`" \
                f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n" \
                f"**Official:** `{get_stickerset.set.official}`\n" \
                f"**Archived:** `{get_stickerset.set.archived}`\n" \
                f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n" \
                f"**Emojis In Pack:** {' '.join(pack_emojis)}"
        await event.edit(OUTPUT)


CMD_HELP.update({
    "kang":
    ".kang\n"
    "Usage: Reply .kang to a sticker or an image to kang it to your userbot pack."
})

CMD_HELP.update({
    "kang":
    ".kang [emoji('s)]\n"
    "Usage: Works just like .kang but uses the emoji('s) you picked."
})

CMD_HELP.update({
    "kang":
    ".kang [number]\n"
    "Usage: Kang's the sticker/image to the specified pack but uses 🤔 as emoji."
})

CMD_HELP.update({
    "stkrinfo":
    ".stkrinfo \n"
    "Usage: Gets info about the sticker pack."
})
