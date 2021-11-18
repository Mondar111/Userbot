import os

import heroku3
from telethon.tl.functions.users import GetFullUserRequest

from userbot import CMD_HANDLER as cmd
from userbot import (
    CMD_HELP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    SUDO_HANDLER,
    SUDO_USERS,
    bot,
)
from userbot.events import man_cmd
from userbot.utils import edit_delete, edit_or_reply, get_user_from_event

Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
sudousers = os.environ.get("SUDO_USERS") or ""


@bot.on(man_cmd(outgoing=True, pattern=r"sudo$"))
async def sudo(event):
    sudo = "True" if SUDO_USERS else "False"
    users = sudousers
    if sudo == "True":
        await edit_or_reply(
            event,
            f"🔮 **Sudo:** `Enabled`\n\n📚 ** List Sudo Users:**\n» `{users}`\n\n**SUDO_HANDLER:** `{SUDO_HANDLER}`",
        )
    else:
        await edit_delete(event, "🔮 **Sudo:** `Disabled`")


@bot.on(man_cmd(outgoing=True, pattern=r"addsudo(?:\s|$)([\s\S]*)"))
async def add(event):
    suu = event.text[9:]
    reply = await event.get_reply_message()
    user, reason = await get_user_from_event(event)
    if not user and not reply:
        return
    if user.id == (await event.client.get_me()).id:
        return await edit_or_reply(
            event, "**Ngapain ngesudo diri sendiri Goblok Kan lu yang punya bot 🐽**"
        )
    if user.id in SUDO_USERS:
        return await edit_delete(event, "dia sudah ada di daftar sudo anda")
    xxnx = await edit_or_reply(event, "`Processing...`")
    bot = "SUDO_USERS"
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await edit_delete(
            xxnx,
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menambahkan pengguna sudo**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    if suu:
        target = suu
    elif reply:
        target = await get_user(event)
    suudo = f"{sudousers} {target}"
    newsudo = suudo.replace("{", "")
    newsudo = newsudo.replace("}", "")
    await xxnx.edit(
        f"**Berhasil Menambahkan** `{target}` **ke Pengguna Sudo.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
    )
    heroku_Config[bot] = newsudo


@bot.on(man_cmd(outgoing=True, pattern="delsudo(?:\s|$)([\s\S]*)"))
async def _(event):
    suu = event.text[8:]
    reply = await event.get_reply_message()
    user, reason = await get_user_from_event(event)
    if not user and not reply:
        return
    if user.id == (await event.client.get_me()).id:
        return await edit_or_reply(event, "**Heuuu stess 🐽**")
    xxx = await edit_or_reply(event, "`Processing...`")
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await edit_delete(
            xxx,
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menghapus pengguna sudo**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    if suu != "" and suu.isnumeric():
        target = suu
    elif reply:
        target = await get_user(event)
    gett = str(target)
    if gett in sudousers:
        newsudo = sudousers.replace(gett, "")
        await xxx.edit(
            f"**Berhasil Menghapus** `{target}` **dari Pengguna Sudo.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
        )
        bot = "SUDO_USERS"
        heroku_Config[bot] = newsudo
    else:
        await edit_delete(
            xxx, "**Pengguna ini tidak ada dalam Daftar Pengguna Sudo anda.**", 45
        )


async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.forward.sender_id)
            )
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
    return replied_user.user.id


CMD_HELP.update(
    {
        "sudo": f"**Plugin : **`sudo`\
        \n\n  •  **Syntax :** `{cmd}sudo`\
        \n  •  **Function : **Untuk Mengecek informasi Sudo.\
        \n\n  •  **Syntax :** `{cmd}addsudo` <reply/user id>\
        \n  •  **Function : **Untuk Menambahkan User ke Pengguna Sudo.\
        \n\n  •  **Syntax :** `{cmd}delsudo` <reply/user id>\
        \n  •  **Function : **Untuk Menghapus User dari Pengguna Sudo.\
        \n\n  •  **NOTE: Berikan Hak Sudo anda Kepada orang yang anda percayai**\
    "
    }
)
