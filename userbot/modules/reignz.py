# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing various modules. """

import asyncio
from asyncio import wait

from userbot import bot

import os, shutil, bs4, re
from time import sleep
from html import unescape
from re import findall
from datetime import datetime
from urllib.parse import quote_plus
from urllib import parse
from shutil import rmtree
from collections import deque
from telethon import events, functions, types

from gtts import gTTS
from requests import get

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, CURRENCY_API,
                     YOUTUBE_API_KEY, bot)
from userbot.events import register

#kanged from Blank-x ;---;
@register(outgoing=True, pattern="^.imdb (.*)")
async def imdb(e):
 try:
    movie_name = e.pattern_match.group(1)
    remove_space = movie_name.split(' ')
    final_name = '+'.join(remove_space)
    page = get("https://www.imdb.com/find?ref_=nv_sr_fn&q="+final_name+"&s=all")
    lnk = str(page.status_code)
    soup = bs4.BeautifulSoup(page.content,'lxml')
    odds = soup.findAll("tr","odd")
    mov_title = odds[0].findNext('td').findNext('td').text
    mov_link = "http://www.imdb.com/"+odds[0].findNext('td').findNext('td').a['href']
    page1 = get(mov_link)
    soup = bs4.BeautifulSoup(page1.content,'lxml')
    if soup.find('div','poster'):
    	poster = soup.find('div','poster').img['src']
    else:
    	poster = ''
    if soup.find('div','title_wrapper'):
    	pg = soup.find('div','title_wrapper').findNext('div').text
    	mov_details = re.sub(r'\s+',' ',pg)
    else:
    	mov_details = ''
    credits = soup.findAll('div', 'credit_summary_item')
    if len(credits)==1:
    	director = credits[0].a.text
    	writer = 'Not available'
    	stars = 'Not available'
    elif len(credits)>2:
    	director = credits[0].a.text
    	writer = credits[1].a.text
    	actors = []
    	for x in credits[2].findAll('a'):
    		actors.append(x.text)
    	actors.pop()
    	stars = actors[0]+','+actors[1]+','+actors[2]
    else:
    	director = credits[0].a.text
    	writer = 'Not available'
    	actors = []
    	for x in credits[1].findAll('a'):
    		actors.append(x.text)
    	actors.pop()
    	stars = actors[0]+','+actors[1]+','+actors[2]
    if soup.find('div', "inline canwrap"):
    	story_line = soup.find('div', "inline canwrap").findAll('p')[0].text
    else:
    	story_line = 'Not available'
    info = soup.findAll('div', "txt-block")
    if info:
    	mov_country = []
    	mov_language = []
    	for node in info:
    		a = node.findAll('a')
    		for i in a:
    			if "country_of_origin" in i['href']:
    				mov_country.append(i.text)
    			elif "primary_language" in i['href']:
    				mov_language.append(i.text)
    if soup.findAll('div',"ratingValue"):
    	for r in soup.findAll('div',"ratingValue"):
    		mov_rating = r.strong['title']
    else:
    	mov_rating = 'Not available'
    await e.edit('<a href='+poster+'>&#8203;</a>'
    			'<b>Title : </b><code>'+mov_title+
    			'</code>\n<code>'+mov_details+
    			'</code>\n<b>Rating : </b><code>'+mov_rating+
    			'</code>\n<b>Country : </b><code>'+mov_country[0]+
    			'</code>\n<b>Language : </b><code>'+mov_language[0]+
    			'</code>\n<b>Director : </b><code>'+director+
    			'</code>\n<b>Writer : </b><code>'+writer+
    			'</code>\n<b>Stars : </b><code>'+stars+
    			'</code>\n<b>IMDB Url : </b>'+mov_link+
    			'\n<b>Story Line : </b>'+story_line,
    			link_preview = True , parse_mode = 'HTML'
    			)
 except IndexError:
     await e.edit("Plox enter **Valid movie name** kthx")


@register(outgoing=True, pattern="^.f ")
async def payf(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        paytext = e.text[3:]
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*6, paytext,paytext, paytext*5, paytext, paytext, paytext)
        await e.edit(pay)


@register(outgoing=True, pattern="^.cry$")
async def cry(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("(;´༎ຶД༎ຶ)")


@register(outgoing=True, pattern="^.fp$")
async def facepalm(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("🤦‍♂")


@register(outgoing=True, pattern="^.myusernames$")
async def _(event):
    if event.fwd_from:
        return
    result = await bot(functions.channels.GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"- {channel_obj.title} @{channel_obj.username} \n"
    await event.edit(output_str)


@register(outgoing=True, pattern="^.channel$")
async def channel(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("[Join This Channel](t.me/)")


@register(outgoing=True, pattern="^.clock$")
async def _(event):
 if event.fwd_from:
  return
 deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
 for _ in range(48):
  await asyncio.sleep(0.1)
  await event.edit("".join(deq))
  deq.rotate(1)

@register(outgoing=True, pattern="^.json$")
async def json(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if event.fwd_from:
            return
        the_real_message = None
        reply_to_id = None
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            the_real_message = previous_message.stringify()
            reply_to_id = event.reply_to_msg_id
        else:
            the_real_message = event.stringify()
            reply_to_id = event.message.id
        if len(the_real_message) > 4096:
            with io.BytesIO(str.encode(the_real_message)) as out_file:
                out_file.name = "message.json"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    reply_to=reply_to_id
                )
                await event.delete()
        else:
            await event.edit(f"`{the_real_message}`")


@register(outgoing=True, pattern="^.moon$")
async def _(event):
 if event.fwd_from:
  return
 deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
 for _ in range(32):
  await asyncio.sleep(0.1)
  await event.edit("".join(deq))
  deq.rotate(1)


@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
async def scam(event):
    """ Just a small command to fake chat actions for fun !! """
    if not event.text[0].isalpha() and event.text[0] not in (
            "/", "#", "@", "!"):
        options = ['typing', 'contact', 'game', 'location', 'voice', 'round', 'video', 'photo', 'document', 'cancel']
        input_str = event.pattern_match.group(1)
        args = input_str.split()
        if len(args) is 0: # Let bot decide action and time
            scam_action = random.choice(options)
            scam_time = random.randint(30, 60)
        elif len(args) is 1: # User decides time/action
            try:
                scam_action = str(args[0]).lower()
                scam_time = random.randint(30, 60)
            except ValueError:
                scam_action = random.choice(options)
                scam_time = int(args[0])
        elif len(args) is 2: # User decides both action and time
            scam_action = str(args[0]).lower()
            scam_time = int(args[1])
        else:
            await event.edit("`Invalid Syntax !!`")
            return
        try:
            if (scam_time > 0):
                await event.delete()
                async with event.client.action(event.chat_id, scam_action):
                    await asyncio.sleep(scam_time)
        except BaseException:
            return


@register(outgoing=True, pattern="^.gangsta$")
async def whoizme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`EVERyBOdy iZ GangSTur UNtIL I ArRivE` 🔥")

@register(outgoing=True, pattern="^.noobda$")
async def whoizme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`EVERyOne iZ Noob UNtIL Ultra Noob ArRivE` 🔥")

@register(outgoing=True, pattern="^.hacker$")
async def whoizme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`Your account has been haXed.` 🔥") 

@register(outgoing=True, pattern="^.pruhack$")
async def whoizme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`Your account iz hacked now... Pay moni to remove get rid of it` 🔥")


@register(outgoing=True, pattern="^.pru$")
async def whoizme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`This gey is pro as phack` 🔥")


CMD_HELP.update({
    'imdb': ".imdb <movie-name>\
    \nUsage: Shows movie info and other stuffs."
})
CMD_HELP.update({
    'f': ".f <texts or emojis>\
    \nUsage: Pay Respect."
})
CMD_HELP.update({
    'cry': ".cry\
    \nUsage: Crying."
})
CMD_HELP.update({
    'fp': ".fp\
    \nUsage: facepalm."
})
CMD_HELP.update({
    'channel': ".channel\
    \nUsage: channel link."
})

CMD_HELP.update({
    'json': '.json\
\nUsage: Get detailed JSON formatted data about replied message.'
})

CMD_HELP.update({
    'moon': '.moon\
\nUsage: Pokuda zalupa reksa.'
})


CMD_HELP.update({
    'scam': '.scam <option>\
\nUsage: Scam troll.'
})

CMD_HELP.update({
    "gangsta": "Gangta Slag"
})
CMD_HELP.update({
    "noobda": "Just A Fucking Noob"
})
CMD_HELP.update({
    "hacker": "Account` Hacked And Deleted"
})
CMD_HELP.update({
    "pruhack": "Account`Hacked Need Money xD"
})

CMD_HELP.update({
    "pru": "Just A Fucking Pro"
})

CMD_HELP.update({
    "clock": "часики наверно которые крутяца"
})
