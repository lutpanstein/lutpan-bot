#Credit Bye Geez|Ram
#Thanks To All Dev
#pii

import time
import traceback
from sys import version as pyver
from datetime import datetime
import os
import shlex
import textwrap
import asyncio

from pyrogram import Client
from pyrogram import __version__ as pyrover
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from Uputt.helpers.data import Data
from Uputt.helpers.inline import inline_wrapper, paginate_help
from config import BOT_VER, BRANCH as branch
from Uputt import CMD_HELP, StartTime, app

modules = CMD_HELP

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


async def alive_function(message: Message, answers):
    uptime = await get_readable_time((time.time() - StartTime))
    msg = f"""
<b> — **NYALA YA AJG**.</b>

<b> ☘ **USER** ❥ </b> {message.from_user.mention}
<b> ☘ **PYROGRAM VERSI** ❥ </b> <code>{pyrover}</code>
<b> ☘ **UPTIME** ❥ </b> <code>{uptime}</code>
"""
    answers.append(
        InlineQueryResultArticle(
            title="alip",
            description="Check Bot's Stats",
            thumb_url="https://telegra.ph/file/97b753a248f764d72d47c.jpg",
            input_message_content=InputTextMessageContent(
                msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("──「 ʜᴇʟᴘ 」──", callback_data="helper")]]
            ),
        )
    )
    return answers


async def pingme(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await message.reply_text(
              f" ⚝ 𝙻𝚄𝚃𝙿𝙰𝙽 𝚄𝙱𝙾𝚃  ⚝\n"
      f" 𝗣𝗜𝗡𝗚𝗡𝗬𝗔 𝗦𝗘𝗚𝗜𝗡𝗜 𝗔𝗝𝗚\n"
      f" 🏓 `%sms`\n"
      f" ⚘ 𝙽𝚈𝙰𝙻𝙰 ❥ `{uptime}`\n"
      f" ⚘ 𝙾𝚆𝙽𝙴𝚁 ❥ `{client.me.mention}`\n"
      f" ⚘ 𝚅𝙴𝚁𝚂𝙸 ❥ `{BOT_VER}`" % (duration)
)
async def peler_function(message: Message, answers):
    msg = (
        fb    "⚝ 𝙻𝚄𝚃𝙿𝙰𝙽 𝚄𝙱𝙾𝚃 ⚝\n"
        "ㅤ    ㅤ**NYALA** \n"
        f" ⚘ㅤㅤㅤ 𝙿𝙻𝚄𝙶𝙸𝙽 ❥ </b> <code>{len(modules)} Modules</code> \n"
        f" ⚘ㅤㅤ𝚟𝚎𝚛𝚜𝚒 ❥ {BOT_VER} \n"
        f" ⚘ㅤㅤ`BRANCH`: {branch} \n\n"
    )
    answers.append(
        InlineQueryResultArticle(
            title="alive",
            description="Check Bot's Stats",
            thumb_url="https://telegra.ph//file/ad02750e78083a8c57e90.jpg",
            input_message_content=InputTextMessageContent(
                msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url="t.me/heiscancer"), InlineKeyboardButton(text="ᴏᴡɴᴇʀ", url="t.me/uneedsaha")], [InlineKeyboardButton(text="ᴍᴇɴᴜ", callback_data="reopen")]]
            ),
        )
    )
    return answers


async def help_function(answers):
    bttn = paginate_help(0, CMD_HELP, "helpme")
    answers.append(
        InlineQueryResultArticle(
            title="Help Article!",
            description="Check Command List & Help",
            thumb_url="https://telegra.ph//file/ad02750e78083a8c57e90.jpg",
            input_message_content=InputTextMessageContent(
                Data.text_help_menu.format(len(CMD_HELP))
            ),
            reply_markup=InlineKeyboardMarkup(bttn),
        )
    )
    return answers


@app.on_inline_query()
@inline_wrapper
async def inline_query_handler(client: Client, query):
    try:
        text = query.query.strip().lower()
        string_given = query.query.lower()
        answers = []
        if text.strip() == "":
            return
        elif text.split()[0] == "alip":
            answerss = await alive_function(query, answers)
            await client.answer_inline_query(query.id, results=answerss, cache_time=10)
        elif string_given.startswith("helper"):
            answers = await help_function(answers)
            await client.answer_inline_query(query.id, results=answers, cache_time=0)
        elif string_given.startswith("alive"):
            answers = await peler_function(query, answers)
            await client.answer_inline_query(query.id, results=answers, cache_time=5)
    except Exception as e:
        e = traceback.format_exc()
        print(e, "InLine")
