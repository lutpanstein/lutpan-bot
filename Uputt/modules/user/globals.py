# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message

from config import CMD_HANDLER as cmd
from Uputt import *
from Uputt.helpers.adminHelpers import DEVS, WHITELIST
from Uputt.helpers.basic import edit_or_reply
from Uputt.helpers.PyroHelpers import get_ub_chats
from Uputt.utils import extract_user, extract_user_and_reason

from .help import add_command_help


def globals_init():
    try:
        global sql, sql2
        from importlib import import_module

        sql = import_module("Uputt.helpers.SQL.gban_sql")
        sql2 = import_module("Uputt.helpers.SQL.gmute_sql")
    except Exception as e:
        sql = None
        sql2 = None
        LOGS.warn("Unable to run GBan and GMute command, no SQL connection found")
        raise e


globals_init()


@Client.on_message(
    filters.command("cgban", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("gban", cmd) & filters.me)
async def gban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        Uputt = await message.reply("`MAINNYA GBAN ANJIRRR`")
    else:
        Uputt = await message.edit("`Lagi gban bang`")
    if not user_id:
        return await Uputt.edit("Ganti username dia bang takut digban.")
    if user_id == client.me.id:
        return await Uputt.edit("**Ngapain NgeGban Diri Sendiri Pepek**")
    if user_id in DEVS:
        return await Uputt.edit("**NI DEVELOPER Uputt TERHORMAT GABISA LU BAN PEPEKK**")
    if user_id in WHITELIST:
        return await Uputt.edit(
            "**Kau Gak Bisa Kontol Gban Dia Karena Dia Adalah admin @Karc0de 😡**"
        )
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await Uputt.edit("`Harap tentukan pengguna yang valid!`")

    if sql.is_gbanned(user.id):
        return await Uputt.edit(
            f"[Jamet](tg://user?id={user.id}) **ini sudah ada di daftar gbanned**"
        )
    f_chats = await get_ub_chats(client)
    if not f_chats:
        return await Uputt.edit("**Anda tidak mempunyai GC yang anda admin 🥺**")
    er = 0
    done = 0
    for gokid in f_chats:
        try:
            await client.ban_chat_member(chat_id=gokid, user_id=int(user.id))
            done += 1
        except BaseException:
            er += 1
    sql.gban(user.id)
    msg = (
        r"**\\#GBanned_User//**"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    msg += f"\n**Affected To:** `{done}` **Chats**"
    await Uputt.edit(msg)


@Client.on_message(
    filters.command("cungban", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("ungban", cmd) & filters.me)
async def ungban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        Uputt = await message.reply("`UnGbanning...`")
    else:
        Uputt = await message.edit("`UnGbanning....`")
    if not user_id:
        return await Uputt.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await Uputt.edit("`Harap tentukan pengguna yang valid!`")

    try:
        if not sql.is_gbanned(user.id):
            return await Uputt.edit("`Udah ga digban tititttt`")
        ung_chats = await get_ub_chats(client)
        if not ung_chats:
            return await Uputt.edit("**Anda tidak mempunyai GC yang anda admin 🥺**")
        er = 0
        done = 0
        for good_boi in ung_chats:
            try:
                await client.unban_chat_member(chat_id=good_boi, user_id=user.id)
                done += 1
            except BaseException:
                er += 1
        sql.ungban(user.id)
        msg = (
            r"**MAKHLUK YG DIBUKAIN GBAN**"
            f"\n\n**NAMA MAKHLUK** [{user.first_name}](tg://user?id={user.id})"
            f"\n**TOGEL** `{user.id}`"
        )
        if reason:
            msg += f"\n**Reason:** `{reason}`"
        msg += f"\n**Affected To:** `{done}` **Chats**"
        await Uputt.edit(msg)
    except Exception as e:
        await Uputt.edit(f"**ERROR:** `{e}`")
        return


@Client.on_message(filters.command("listgban", cmd) & filters.me)
async def gbanlist(client: Client, message: Message):
    users = sql.gbanned_users()
    Uputt = await edit_or_reply(message, "`Processing...`")
    if not users:
        return await Uputt.edit("Belum Ada Jamet yang Di-Gban")
    gban_list = "**GBanned Users:**\n"
    count = 0
    for i in users:
        count += 1
        gban_list += f"**{count} -** `{i.sender}`\n"
    return await Uputt.edit(gban_list)


@Client.on_message(filters.command("gmute", cmd) & filters.me)
async def gmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    Uputt = await edit_or_reply(message, "`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await Uputt.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await Uputt.edit(f"`Please specify a valid user!`")
        return
    if user.id == client.me.id:
        return await Uputt.edit("**Ngapain NgeGmute Diri Sendiri Pepek**")
    if user.id in DEVS:
        return await Uputt.edit("**Gak Bisa Di Gmute Kontol karena dia Yang Buat Aku 🗿**")
    if user.id in WHITELIST:
        return await Uputt.edit(
            "**Kau Gak Bisa Kontol Gmute Dia Karena Dia Adalah admin @Karc0de 😡**"
        )
    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await Uputt.edit("`Calm down anybob, you can't gmute yourself.`")
    except BaseException:
        pass

    try:
        if sql2.is_gmuted(user.id):
            return await Uputt.edit("`User already gmuted`")
        sql2.gmute(user.id)
        await Uputt.edit(f"[{user.first_name}](tg://user?id={user.id}) globally gmuted!")
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.restrict_member(user.id, ChatPermissions())
        except BaseException:
            pass
    except Exception as e:
        await Uputt.edit(f"**ERROR:** `{e}`")
        return


@Client.on_message(filters.command("ungmute", cmd) & filters.me)
async def ungmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    Uputt = await edit_or_reply(message, "`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await Uputt.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await Uputt.edit(f"`Please specify a valid user!`")
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await Uputt.edit("`Calm down anybob, you can't ungmute yourself.`")
    except BaseException:
        pass

    try:
        if not sql2.is_gmuted(user.id):
            return await Uputt.edit("`Udah diemut masal`")
        sql2.ungmute(user.id)
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.unban_member(user.id)
        except BaseException:
            pass
        await Uputt.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **DI EMUT MASALL**"
        )
    except Exception as e:
        await Uputt.edit(f"**ERROR:** `{e}`")
        return


@Client.on_message(filters.command("listgmute", cmd) & filters.me)
async def gmutelist(client: Client, message: Message):
    users = sql2.gmuted_users()
    Uputt = await edit_or_reply(message, "`Processing...`")
    if not users:
        return await Uputt.edit("Belum Ada Jamet yang Di-Gmute")
    gmute_list = "**MAKHLUK YG DI GLOBAL EMUT :**\n"
    count = 0
    for i in users:
        count += 1
        gmute_list += f"**{count} -** `{i.sender}`\n"
    return await Uputt.edit(gmute_list)


@Client.on_message(filters.incoming & filters.group)
async def globals_check(client: Client, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not user_id:
        return
    if sql.is_gbanned(user_id):
        try:
            await client.ban_chat_member(chat_id, user_id)
        except BaseException:
            pass

    if sql2.is_gmuted(user_id):
        try:
            await message.delete()
        except errors.RPCError:
            pass
        try:
            await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()


add_command_help(
    "globals",
    [
        [
            "gban <reply/username/userid>",
            "Melakukan Global Banned Ke Semua Grup Dimana anda Sebagai Admin.",
        ],
        ["ungban <reply/username/userid>", "Membatalkan Global Banned."],
        ["listgban", "Menampilkan List Global Banned."],
    ],
)
