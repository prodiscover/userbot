# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to android"""

import re
from requests import get
from bs4 import BeautifulSoup

from userbot import CMD_HELP
from userbot.events import register


EVOX_DEVICES = 'https://raw.githubusercontent.com/Evolution-X-Devices/' \
               'official_devices/master/devices.json'

@register(outgoing=True, pattern=r"^.evo(?: |$)(\S*)")
async def device_info(request):
    if not request.text[0].isalpha()\
            and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        device = request.pattern_match.group(1)
        if device:
            pass
        elif textx:
            device = textx.text
        else:
            await request.edit("`Usage: .evo <codename>`")
            return
    found = [
        i for i in get(EVOX_DEVICES).json()
        if i["codename"] == device
    ]
    if found:
        reply = ''
        for item in found:
            name = item['name']
            brand = item['brand']
            codename = item['codename']
            maintainer = item['supported_versions'][0]['maintainer_name']
            xda = item['supported_versions'][0]['xda_thread']
            mainurl = item['supported_versions'][0]['maintainer_url'] 
            version = item['supported_versions'][0]['version_code']
            reply += f'**📲 Evolution X for {brand} {name} ({codename})**\n' \
                f'👤 by: {maintainer}\n' \
                f'ℹ️ Version: {version}\n' \
                f'[⬇ Download Now](https://sourceforge.net/projects/evolution-x/files/{codename}) \n' \
                f'[📱 XDA Thread]({xda})'
    else:
        reply = f"`Device not found!!!.`\n"
    await request.edit(reply)


CMD_HELP.update({
    ".evo <devices>": "For example .evo beryllium"
})
