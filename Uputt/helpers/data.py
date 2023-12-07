from pyrogram.types import InlineKeyboardButton
from Uputt import CMD_HELP
class Data:

    text_help_menu = (
        "**Menu Inline Pyro-Cleo**\n**Prefixes:** ., ?, !, *"
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )
    reopen = [[InlineKeyboardButton("TEKEN AJA", callback_data="reopen")]]
