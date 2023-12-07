import importlib
from pyrogram import idle
from uvloop import install


from Uputt.modules import ALL_MODULES
from Uputt import BOTLOG_CHATID, LOGGER, LOOP, aiosession, app, bots, ids
from Uputt.modules.basic import join
from Uputt.helpers.misc import heroku, create_botlog

BOT_VER = "9.9.9"
CMD_HANDLER = ["." "," "?" "!"]
MSG_ON = """
💢 **LUTPANSTEIN MASSAGE** 💢
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
❍▹ 𝙻𝚄𝚃𝙿𝙰𝙽 𝚄𝙱𝙾𝚃 𝚟𝚎𝚛𝚜𝚒  `{}`
❍▹ **Kᴇᴛɪᴋ** `{}alive` **Uɴᴛᴜᴋ Mᴇɴɢᴇᴄᴇᴋ Bᴏᴛ**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""


async def main():
    await app.start()
    print("LOG: Founded Bot token Booting..")
    for all_module in ALL_MODULES:
        importlib.import_module("Lutpan.modules" + all_module)
        print(f"Successfully Imported {all_module} ")
    for bot in bots:
        try:
            await bot.start()
            ex = await bot.get_me()
            await join(bot)
            try:
                await bot.send_message(BOTLOG_CHATID, MSG_ON.format(BOT_VER, CMD_HANDLER))
            except BaseException:
                pass
            print(f"Started as {ex.first_name} | {ex.id} ")
            ids.append(ex.id)
        except Exception as e:
            print(f"{e}")
    if bot and not str(BOTLOG_CHATID).startswith("-100"):
        await create_botlog(bot)
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("Lutpan").info("LUTPAN UBOT Telah Aktif")
    heroku()
    install()
    LOOP.run_until_complete(main())
