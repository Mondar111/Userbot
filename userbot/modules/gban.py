# by:koala @mixiologist
# Lord Userbot

from telethon import events

from userbot import ALIVE_NAME, DEVS, bot
from userbot.events import man_cmd, register
from userbot.modules.sql_helper.gmute_sql import is_gmuted

from .admin import get_user_from_event

# Ported For Lord-Userbot by liualvinas/Alvin


@bot.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        if is_gmuted(user.id) and chat.admin_rights:
            try:
                await event.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                await event.reply(
                    f"**#GBanned_User** Joined.\n\n** • First Name:** [{user.first_name}](tg://user?id={user.id})\n • **Action:** `Banned`"
                )
            except BaseException:
                pass


@bot.on(man_cmd(outgoing=True, pattern=r"gband(?: |$)(.*)"))
@register(incoming=True, from_users=DEVS, pattern=r"^\.cgband(?: |$)(.*)")
async def gben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if sender.id != me.id:
        dark = await dc.reply("`Gbanning...`")
    else:
        dark = await dc.edit("`Memproses Global Banned Jamet..`")
    me = await userbot.client.get_me()
    await dark.edit("`Global Banned Akan Segera Aktif..`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    try:
        user, reason = await get_user_from_event(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await dark.edit("**Gagal Global Banned :(**")
    if user:
        if user.id in DEVS:
            return await dark.edit("**Gagal Global Banned, Dia Adalah Pembuat Saya 🤪**")
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, view_messages=False)
                a += 1
                await dark.edit(
                    r"\\**#GBanned_User**//"
                    f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
                    f"**User ID:** `{user.id}`\n"
                    f"**Action:** `Global Banned`"
                )
            except BaseException:
                b += 1
    else:
        await dark.edit("**Balas Ke Pesan Penggunanya Goblok**")
    try:
        if gmute(user.id) is False:
            return await dark.edit(
                "**#Already_GBanned**\n\nUser Already Exists in My Gban List.**"
            )

    except BaseException:
        pass
    return await dark.edit(
        r"\\**#GBanned_User**//"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
        f"**User ID:** `{user.id}`\n"
        f"**Action:** `Global Banned by {ALIVE_NAME}`"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"ungband(?: |$)(.*)"))
@register(incoming=True, from_users=DEVS, pattern=r"^\.cungband(?: |$)(.*)")
async def gunben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if sender.id != me.id:
        dark = await dc.reply("`Ungbanning...`")
    else:
        dark = await dc.edit("`Ungbanning....`")
    me = await userbot.client.get_me()
    await dark.edit("`Membatalkan Perintah Global Banned`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    try:
        user, reason = await get_user_from_event(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await dark.edit("**Gagal Ungbanned :(**")
    if user:
        if user.id in DEVS:
            return await dark.edit(
                "**Man Tidak Bisa Terkena Perintah Ini, Karna Dia Pembuat saya**"
            )
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await dark.edit("`Membatalkan Global Banned...`")
            except BaseException:
                b += 1
    else:
        await dark.edit("`Balas Ke Pesan Penggunanya Goblok`")
    try:
        if ungmute(user.id) is False:
            return await dark.edit("**Error! Pengguna Sedang Tidak Di Global Banned.**")
    except BaseException:
        pass
    return await dark.edit(
        r"\\**#UnGbanned_User**//"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})\n"
        f"**User ID:** `{user.id}`\n"
        f"**Action:** `UnGBanned by {ALIVE_NAME}`"
    )


@bot.on(man_cmd(outgoing=True, pattern=r"listgmute$"))
async def gablist(event):
    gmuted_users = is_gmuted()
    GMUTE_LIST = "**List Global Banned Saat Ini**\n"
    if len(gmuted_users) > 0:
        for a_user in gmuted_users:
            if a_user.reason:
                GMUTE_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) **Reason** `{a_user.reason}`\n"
            else:
                GMUTE_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) `No Reason`\n"
                )
    else:
        GMUTE_LIST = "Belum ada Pengguna yang Di-Gmute"
    await event.edit(GMUTE_LIST)
