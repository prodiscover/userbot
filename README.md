# Telegram-UserBot, RE1GNZ Version

### If the CI builds pass, but you still get syntax errors when running locally it's most probably not a problem with the source but with your version of python


[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Ruslan16022/AyeBot/tree/dev/reignz)


```
#include <std/disclaimer.h>
/**
    Your Telegram account may get banned.
    I am not responsible for any improper use of this bot
    This bot is intended for the purpose of having fun with memes,
    as well as efficiently managing groups.
    You ended up spamming groups, getting reported left and right,
    and you ended up in a Finale Battle with Telegram and at the end
    Telegram Team deleted your account?
    And after that, then you pointed your fingers at us
    for getting your acoount deleted?
    I will rolling on the floor laughing at you.
/**
```

A modular telegram Python UserBot running on python3 with a mongoDB coupled with Redis backend.

Started up as a simple bot, which helps with deleting messages and other stuffs when I didn't possess a smartphone(selecting each message indeed difficult) with a ton of meme features kanged from [SkittBot](https://github.com/skittles9823/SkittBot), it has evolved, becoming extremely modular and simple to use.

For configuring this userbot, you can checkout the [Wiki](https://wiki.raphielgang.org)

If you just want to stay in the loop about new features or
announcements you can join the [news channel](https://t.me/maestro_userbot_channel).

If you find any bugs or have any suggestions then don't hesitate to contact me in [my support group](https://t.me/userbot_support).

Please head to the wiki on instructions to setting it up!


### Contributing to the source:

We love to see you contributing and helping us improve on our way to a perfect userbot.

If you need help writing a new module, you can checkout the [Wiki](https://wiki.raphielgang.org).

Please target your PRs to the staging branch and not master. Commits on `master` wont be done by a user.


### If You Are Deploying Manually In Heroku Then Dont Forget To Add This In Setting Of Your App
-> heroku stack:set container -a APPNAME (Do this in heroku cli oterwise mongo db will show failed)

-> heroku/python

-> heroku-community/apt


### Instruction For Gdrive Module
Usage:
.mirror [in reply to TG file] or .mirror <link> | <filename>

Note: User needs to do the following:

Set up OAuth
- Visit the Google Cloud Console
- Go to the OAuth Consent tab, fill it, and save.
- Go to the Credentials tab and click Create Credentials -> OAuth Client ID
- Choose Other and Create.
- Use the download button to download your credentials.
- Move that file to the root of pydrive-client, and rename it to client_secrets.json

Enable the Drive API
- Visit the Google API Library page.
- Search for Drive.
- Make sure that it's enabled. Enable it if not.

Authenticating
- Run generate_drive_session.py to be prompted to follow an OAuth URL that will take you to the Google Drive login page, and then give you a code to paste on the terminal. Once that's done, these credentials will be cached and you will not be prompted again.

Updating config
- Once, you finished everything as above, open your config.env and add the following line:
- GDRIVE_FOLDER=""
- Where value is an ID of a folder on your Drive like "1n4XS6IZCPY6urGKu6JM4K9VS1fo21s_l"


### Credits:

I would like to thank people who assisted me throughout this project:

* [@uzbekcoder](https://github.com/uzbekcoder)
* [@YouTwitFace](https://github.com/YouTwitFace)
* [@TheDevXen](https://github.com/TheDevXen)
* [@Skittles9823](https://github.com/Skittles9823)
* [@deletescape](https://github.com/deletescape)
* [@songotenks69](https://github.com/songotenks69)
* [@Ovenoboyo](https://github.com/Ovenoboyo)
* [SphericalKat](https://github.com/ATechnoHazard)
* [@rupansh](https://github.com/rupansh)
* [@zakaryan2004](https://github.com/zakaryan2004)
* [@kandnub](https://github.com/kandnub)
* [@pqhaz](https://github.com/pqhaz)
* [@yshalsager](https://github.com/yshalsager)

and many more people who aren't mentioned here.

Found Bugs? Create an issue on the issue tracker, or post it in the [support group](https://t.me/userbot_support).
