## SCRIPT INI HASIL EDIT DARI PYRO-MAN USERBOT
## Ā© @mrismanaziz

import time
from datetime import datetime

import speedtest
from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from config import BOT_VER, BRANCH as brch
from Uputt import CMD_HELP, StartTime
from Uputt.helpers.basic import edit_or_reply
from Uputt.helpers.constants import WWW
from Uputt.helpers.PyroHelpers import SpeedConvert
from Uputt.utils.tools import get_readable_time
from Uputt.helpers.adminHelpers import DEVS

from .help import add_command_help

modules = CMD_HELP


@Client.on_message(filters.command(["speed", "speedtest"], cmd) & filters.me)
async def speed_test(client: Client, message: Message):
    new_msg = await edit_or_reply(message, "`Running speed test . . .`")
    spd = speedtest.Speedtest()

    new_msg = await message.edit(
        f"`{new_msg.text}`\n" "`Getting best server based on ping . . .`"
    )
    spd.get_best_server()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing download speed . . .`")
    spd.download()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing upload speed . . .`")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`Getting results and preparing formatting . . .`"
    )
    results = spd.results.dict()

    await message.edit(
        WWW.SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )

@Client.on_message(filters.command(["speed", "speedtest"], cmd) & filters.me)
async def speed_test(client: Client, message: Message):
    new_msg = await edit_or_reply(message, "`Running speed test . . .`")
    spd = speedtest.Speedtest()

    new_msg = await message.edit(
        f"`{new_msg.text}`\n" "`Getting best server based on ping . . .`"
    )
    spd.get_best_server()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing download speed . . .`")
    spd.download()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing upload speed . . .`")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`Getting results and preparing formatting . . .`"
    )
    results = spd.results.dict()

    await message.edit(
        WWW.SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )

@Client.on_message(filters.command("ping", cmd) & filters.me)
async def pingme(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()

    xx = await edit_or_reply(message, "**NI LIAT YA AJG PINGYA**")
    await xx.edit("**BENTAR YA CUKI**")
    await xx.edit("**LAGI NGETEST PING LU KONTOL**")
    await xx.edit("**NGETEST PING BUAT GIKES YA**")
    await xx.edit("**KEK DERESS AJA GIKESANLU**")
    await xx.edit("**NI {client.me.mention}LIAT YA AJG PINGNYA**")
    await message.reply_text(
        f" ā¯ š¯™»š¯„š¯š¯™æš¯™°š¯™½ š¯„š¯™±š¯™¾š¯  ā¯\n"
        f" š¯—£š¯—š¯—�š¯—š¯—�š¯—¬š¯—” š¯—¦š¯—š¯—š¯—š¯—�š¯— š¯—”š¯—¯š¯—\n"
        f" š¸“ `%sms`\n"
        f" ā š¯™½š¯š¯™°š¯™»š¯™° ā¯� `{uptime}`\n"
        f" ā š¯™¾š¯†š¯™½š¯™´š¯ ā¯� `{client.me.mention}`\n"
        f" ā š¯…š¯™´š¯š¯‚š¯™ø ā¯� `{BOT_VER}`" % (duration)
)

@Client.on_message(
    filters.command("ceping", ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command("kping", cmd) & filters.me)
async def kping(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    xx = await edit_or_reply(message, "**NI LIAT YA AJG PINGNYA**") 
    await xx.edit("**BENTAR YA CUKI**")
    await xx.edit("**LAGI NGETEST PING LU KONTOL**")
    await xx.edit("**NGETEST PING BUAT GIKES YA**")
    await xx.edit("**KEK DERES AJA GIKESANLU**")
    await xx.edit("**NI LIAT YA AJG PINGNYA**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await xx.edit(
        f" ā¯ š¯™»š¯„š¯š¯™æš¯™°š¯™½ š¯„š¯™±š¯™¾š¯  ā¯\n"
      f" š¯—£š¯—š¯—�š¯—š¯—�š¯—¬š¯—” š¯—¦š¯—š¯—š¯—š¯—�š¯— š¯—”š¯—¯š¯—\n"
      f" š¸“ `%sms`\n"
      f" ā š¯™½š¯š¯™°š¯™»š¯™° ā¯� `{uptime}`\n"
      f" ā š¯™¾š¯†š¯™½š¯™´š¯ ā¯� `{client.me.mention}`\n"
      f" ā š¯…š¯™´š¯š¯‚š¯™ø ā¯� `{BOT_VER}`" % (duration)
)

     
      
