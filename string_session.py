# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from userbot import API_KEY, API_HASH

print("""Please go-to my.telegram.org
Login using your Telegram account
Click on API Development Tools
Create a new application, by entering the required details""")

with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
    print("Here is your userbot srting, copy it to a safe place !!")
    print("")
    print(client.session.save())
    print("")
    print("")
    print("Enjoy your userbot !!")
