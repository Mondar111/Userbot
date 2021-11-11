# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for System Stats commands """

import asyncio
import platform
import sys
import time
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from datetime import datetime
from platform import python_version
from shutil import which

import psutil
from pytgcalls import __version__ as pytgcalls
from telethon import __version__, version

from userbot import ALIVE_LOGO, BOT_VER, CHANNEL
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, GROUP, StartTime, bot
from userbot.events import man_cmd
from userbot.modules.sql_helper.globals import gvarstatus

from .ping import get_readable_time

modules = CMD_HELP
emoji = gvarstatus("ALIVE_EMOJI") or "⚡️"
alive_text = gvarstatus("ALIVE_TEKS_CUSTOM") or "Hey, I am alive."


@bot.on(man_cmd(outgoing=True, pattern=r"spc"))
async def psu(event):
    uname = platform.uname()
    softw = "**Informasi Sistem**\n"
    softw += f"`Sistem   : {uname.system}`\n"
    softw += f"`Rilis    : {uname.release}`\n"
    softw += f"`Versi    : {uname.version}`\n"
    softw += f"`Mesin    : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Waktu Hidup: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**Informasi CPU**\n"
    cpuu += "`Physical cores   : " + str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "**Total CPU Usage**\n"
    cpuu += f"`Semua Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**Memori Digunakan**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**Bandwith Digunakan**\n"
    bw += f"`Unggah  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{softw}\n"
    help_string += f"{cpuu}\n"
    help_string += f"{memm}\n"
    help_string += f"{bw}\n"
    help_string += "**Informasi Mesin**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@bot.on(man_cmd(outgoing=True, pattern=r"sysd$"))
async def sysdetails(sysd):
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("**Install neofetch Terlebih dahulu!!**")


@bot.on(man_cmd(outgoing=True, pattern=r"botver$"))
async def bot_ver(event):
    if event.text[0].isalpha() or event.text[0] in ("/", "#", "@", "!"):
        return
    if which("git") is not None:
        ver = await asyncrunapp(
            "git",
            "describe",
            "--all",
            "--long",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        rev = await asyncrunapp(
            "git",
            "rev-list",
            "--all",
            "--count",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await event.edit(
            "✥ **Userbot Versi :** " f"`{verout}`" "\n✥ **Revisi :** " f"`{revout}`"
        )
    else:
        await event.edit("anda tidak memiliki git, Anda Menjalankan Bot - 'v1.beta.4'!")


@bot.on(man_cmd(outgoing=True, pattern=r"(?:alive|on)\s?(.)?"))
async def amireallyalive(alive):
    user = await bot.get_me()
    uptime = await get_readable_time((time.time() - StartTime))
    output = (
        f"**[Man-Userbot](https://github.com/mrismanaziz/Man-Userbot) is Up and Running.**\n\n"
        f"**{alive_text}**\n\n"
        f"{emoji} **Master :** [{user.first_name}](tg://user?id={user.id}) \n"
        f"{emoji} **Modules :** `{len(modules)} Modules` \n"
        f"{emoji} **Bot Version :** `{BOT_VER}` \n"
        f"{emoji} **Python Version :** `{python_version()}` \n"
        f"{emoji} **Pytgcalls Version :** `{pytgcalls.__version__}` \n"
        f"{emoji} **Telethon Version :** `{version.__version__}` \n"
        f"{emoji} **Bot Uptime :** `{uptime}` \n\n"
        f"    **[𝗦𝘂𝗽𝗽𝗼𝗿𝘁](https://t.me/{GROUP})** | **[𝗖𝗵𝗮𝗻𝗻𝗲𝗹](https://t.me/{CHANNEL})** | **[𝗢𝘄𝗻𝗲𝗿](tg://user?id={user.id})**"
    )
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await alive.delete()
            msg = await bot.send_file(alive.chat_id, logo, caption=output)
            await asyncio.sleep(800)
            await msg.delete()
        except BaseException:
            await alive.edit(
                output + "\n\n ***Logo yang diberikan tidak valid."
                "\nPastikan link diarahkan ke gambar logo**"
            )
            await asyncio.sleep(100)
            await alive.delete()
    else:
        await alive.edit(output)
        await asyncio.sleep(100)
        await alive.delete()


CMD_HELP.update(
    {
        "system": f"**Plugin : **`system`.\
        \n\n  •  **Syntax :** `{cmd}sysd`\
        \n  •  **Function : **Menampilkan informasi sistem menggunakan neofetch\
        \n\n\n  •  **Syntax :** `{cmd}botver`\
        \n  •  **Function : **Menampilkan versi userbot\
        \n\n  •  **Syntax :** `{cmd}spc`\
        \n  •  **Function : **Show system specification\
    "
    }
)


CMD_HELP.update(
    {
        "alive": f"**Plugin : **`alive`\
        \n\n  •  **Syntax :** `{cmd}alive` atau `{cmd}on`\
        \n  •  **Function : **Untuk melihat apakah bot Anda berfungsi atau tidak.\
    "
    }
)
