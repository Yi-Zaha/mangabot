import asyncio as aio
import os
import uvloop

uvloop.install()

from pathlib import Path
from bot import bot, manga_updater
from models.db import DB 
from models.db1 import DBX
from extras import load_plugin

load_plugin(Path("extras.py"))

async def async_main():
    db = DB()
    dbx = DBX()
    await db.connect()
    await dbx.connect()
    
if __name__ == '__main__':
    loop = aio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(async_main())
    loop.create_task(manga_updater())
    bot.run()
