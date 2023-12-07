from .adminHelpers import *
from .basic import *
from .constants import *
from .expand import *
#from .misc import *
from .interval import *
from .msg_types import *
from .parser import *
from .PyroHelpers import *
from .tools import *
from .utility import *


import os
import sys
from pyrogram import Client


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Uputt"])

async def join(client):
    try:
        await client.join_chat("amneseey0u")
        await client.join_chat("UputtSupport")
        await client.join_chat("berisikjelekk")
        await client.join_chat("meliodassupoort")
        await client.join_chat("carivirtualrandom")
        await client.join_chat("allaboutcleoo")
    except BaseException:
        pass
