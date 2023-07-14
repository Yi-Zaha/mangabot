import io
import sys
import traceback
import importlib
import logging

from pathlib import Path 
from pyrogram.enums import ParseMode
from bot import bot, DB, filters, file_options, mangas, Subscription, LastChapter

MAX_MESSAGE_LENGTH = 4096

ALLOWED_USERS = 5591954930
def load_plugin(plugin_path: Path):
    plugin_name = plugin_path.stem
    if not plugin_name.startswith("__"):
        name = f"{plugin_path.parent.stem}.{plugin_name}" if plugin_path.parent.stem else plugin_name
        spec = importlib.util.spec_from_file_location(name, plugin_path)
        load = importlib.util.module_from_spec(spec)
        load.logger = logging.getLogger(plugin_name)
        spec.loader.exec_module(load)
        sys.modules[name] = load
    
@bot.on_message(filters=filters.command("eval") & filters.user(ALLOWED_USERS), group=1)
async def _(client, message):
    status_message = await message.reply_text("Processing ...")
    try:
        cmd = message.text.markdown.split(" ", maxsplit=1)[1]
    except:
        return await status_message.edit_text("Give code to evaluate...")

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**EVAL**: "
    final_output += f"`{cmd}`\n\n"
    final_output += "**OUTPUT**:\n"
    final_output += f"`{evaluation.strip()}`\n"

    if len(final_output) > MAX_MESSAGE_LENGTH:
        with io.BytesIO(str.encode(evaluation)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file,
                caption=f"`{cmd[: MAX_MESSAGE_LENGTH // 4 - 1]}`",
                disable_notification=True,
                parse_mode=ParseMode.MARKDOWN,
                quote=True,
            )
    else:
        await reply_to_.reply_text(final_output, parse_mode=ParseMode.MARKDOWN, quote=True)
    await status_message.delete()

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "\n m = message"
        + "\n chat = m.chat.id"
        + "\n reply = m.reply_to_message"
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)
