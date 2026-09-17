import asyncio
import os
import random
import sys
import time
from datetime import datetime
from pyrogram import Client, filters, enums

api_id = 30326052
api_hash = "788a28136095136e4aeccc89db4a1510"

app = Client("my_account_1", api_id=api_id, api_hash=api_hash)

DOWNLOAD_DIR = "/storage/emulated/0/Download/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

START_TIME = time.time()
IS_AFK = False
AFK_REASON = ""
AFK_TIME = 0

# ==========================================
# 1. СИСТЕМА ВА ИТТИЛООТ (8 Фармон)
# ==========================================

@app.on_message(filters.me & filters.command("ping", prefixes="."))
async def ping(client, message):
    start = time.time()
    msg = await message.edit_text("🏓 Pinging...")
    delta = round((time.time() - start) * 1000, 2)
    await msg.edit_text(f"🚀 **Pong!**\n⚡ Latency: `{delta}ms`")

@app.on_message(filters.me & filters.command("alive", prefixes="."))
async def alive(client, message):
    sec = int(time.time() - START_TIME)
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    await message.edit_text(
        f"🟢 **Мега-Юзербот фаъол аст!**\n\n"
        f"⏱ **Аптайм:** `{h}ш {m}д {s}с`\n"
        f"⚡ **Библиотека:** Pyrogram\n"
        f"📱 **Платформа:** Android (Pydroid 3)"
    )

@app.on_message(filters.me & filters.command("info", prefixes="."))
async def info(client, message):
    reply = message.reply_to_message
    user = reply.from_user if reply and reply.from_user else message.from_user
    await message.edit_text(
        f"👤 **Инфои Корбар:**\n\n"
        f"🔹 **Ном:** {user.first_name}\n"
        f"🔹 **Юзернейм:** @{user.username if user.username else 'Надорад'}\n"
        f"🔹 **ID:** `{user.id}`\n"
        f"🔹 **Премиум:** {'Бале ⭐️' if user.is_premium else 'Не'}"
    )

@app.on_message(filters.me & filters.command("id", prefixes="."))
async def get_id(client, message):
    reply = message.reply_to_message
    if reply:
        await message.edit_text(f"👤 **User ID:** `{reply.from_user.id if reply.from_user else 'N/A'}`\n💬 **Chat ID:** `{message.chat.id}`\n📩 **Msg ID:** `{reply.id}`")
    else:
        await message.edit_text(f"💬 **Chat ID:** `{message.chat.id}`\n👤 **Шумо ID:** `{message.from_user.id}`")

@app.on_message(filters.me & filters.command("chatinfo", prefixes="."))
async def chat_info(client, message):
    chat = await client.get_chat(message.chat.id)
    members = chat.members_count if chat.members_count else "N/A"
    await message.edit_text(f"📊 **Маълумоти Чат:**\n\n🔹 **Ном:** {chat.title or chat.first_name}\n🔹 **ID:** `{chat.id}`\n🔹 **Навъ:** `{chat.type.value}`\n🔹 **Аъзоён:** `{members}`")

@app.on_message(filters.me & filters.command("stat", prefixes="."))
async def stats(client, message):
    await message.edit_text("📊 Ҳисобкунӣ...")
    p, g, c = 0, 0, 0
    async for d in client.get_dialogs():
        t = d.chat.type.value
        if t == "private": p += 1
        elif t in ["group", "supergroup"]: g += 1
        elif t == "channel": c += 1
    await message.edit_text(f"📊 **Статистика:**\n\n💬 ЛС: `{p}`\n👥 Гурӯҳҳо: `{g}`\n📢 Каналҳо: `{c}`")

@app.on_message(filters.me & filters.command("me", prefixes="."))
async def about_me(client, message):
    me = await client.get_me()
    await message.edit_text(f"👑 **Соҳиби Юзербот:**\n\n👤 Ном: {me.first_name}\n🆔 ID: `{me.id}`\n📞 Телефон: `+{me.phone_number}`")

@app.on_message(filters.me & filters.command("time", prefixes="."))
async def show_time(client, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.edit_text(f"🕒 **Вақти ҷорӣ:** `{now}`")

# ==========================================
# 2. ИДОРАКУНИИ АККАУНТ ВА ПРОФИЛ (4 Фармон)
# ==========================================

@app.on_message(filters.me & filters.command("setname", prefixes="."))
async def set_name(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        await client.update_profile(first_name=args[1])
        await message.edit_text(f"✅ Ном ба `{args[1]}` иваз шуд!")

@app.on_message(filters.me & filters.command("setbio", prefixes="."))
async def set_bio(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        await client.update_profile(bio=args[1])
        await message.edit_text(f"✅ Био ба `{args[1]}` иваз шуд!")

@app.on_message(filters.me & filters.command("setpfp", prefixes="."))
async def set_pfp(client, message):
    reply = message.reply_to_message
    if reply and reply.photo:
        file = await client.download_media(reply)
        await client.set_profile_photo(photo=file)
        await message.edit_text("✅ Расми профил нав карда шуд!")

@app.on_message(filters.me & filters.command("restart", prefixes="."))
async def restart_bot(client, message):
    await message.edit_text("🔄 **Бот аз нав оғоз шуда истодааст...**")
    os.execl(sys.executable, sys.executable, *sys.argv)

# ==========================================
# 3. МУДИРИЯТИ ГУРӮҲ (10 Фармон)
# ==========================================

@app.on_message(filters.me & filters.command("ban", prefixes="."))
async def ban_user(client, message):
    reply = message.reply_to_message
    if reply:
        try:
            await client.ban_chat_member(message.chat.id, reply.from_user.id)
            await message.edit_text("🚫 Корбар бан шуд!")
        except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("unban", prefixes="."))
async def unban_user(client, message):
    reply = message.reply_to_message
    if reply:
        try:
            await client.unban_chat_member(message.chat.id, reply.from_user.id)
            await message.edit_text("✅ Корбар аз бан баромад!")
        except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("mute", prefixes="."))
async def mute_user(client, message):
    reply = message.reply_to_message
    if reply:
        try:
            await client.restrict_chat_member(message.chat.id, reply.from_user.id, enums.ChatPermissions())
            await message.edit_text("🔇 Корбар Мут шуд!")
        except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("unmute", prefixes="."))
async def unmute_user(client, message):
    reply = message.reply_to_message
    if reply:
        try:
            await client.restrict_chat_member(message.chat.id, reply.from_user.id, enums.ChatPermissions(can_send_messages=True))
            await message.edit_text("🔊 Мут бекор шуд!")
        except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("kick", prefixes="."))
async def kick_user(client, message):
    reply = message.reply_to_message
    if reply:
        try:
            await client.ban_chat_member(message.chat.id, reply.from_user.id)
            await client.unban_chat_member(message.chat.id, reply.from_user.id)
            await message.edit_text("🦶 Корбар аз гурӯҳ пеш карда шуд!")
        except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("promote", prefixes="."))
async def promote_user(client, message):
    reply = message.reply_to_message
    if reply:
        try:
            await client.promote_chat_member(message.chat.id, reply.from_user.id, privileges=enums.ChatPrivileges(can_manage_chat=True, can_delete_messages=True))
            await message.edit_text("👑 Корбар Админ шуд!")
        except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("demote", prefixes="."))
async def demote_user(client, message):
    reply = message.reply_to_message
    if reply:
        try:
            await client.promote_chat_member(message.chat.id, reply.from_user.id, privileges=enums.ChatPrivileges())
            await message.edit_text("📉 Ҳуқуқи админӣ бекор шуд!")
        except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("tagall", prefixes="."))
async def tagall(client, message):
    args = message.text.split(maxsplit=1)
    txt = args[1] if len(args) > 1 else "Диққат!"
    await message.delete()
    m = ""
    async for member in client.get_chat_members(message.chat.id):
        if not member.user.is_bot:
            m += f"[{member.user.first_name}](tg://user?id={member.user.id}) "
            if len(m) > 800:
                await client.send_message(message.chat.id, f"📢 **{txt}**\n\n{m}")
                m = ""
                await asyncio.sleep(1)
    if m: await client.send_message(message.chat.id, f"📢 **{txt}**\n\n{m}")

@app.on_message(filters.me & filters.command("admins", prefixes="."))
async def admins_list(client, message):
    res = "👑 **Админҳо:**\n\n"
    async for m in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        res += f"• [{m.user.first_name}](tg://user?id={m.user.id})\n"
    await message.edit_text(res)

@app.on_message(filters.me & filters.command("leave", prefixes="."))
async def leave_group(client, message):
    await message.edit_text("👋 Баромад аз чат...")
    await client.leave_chat(message.chat.id)

# ==========================================
# 4. ИДОРАКУНИИ ПАЁМҲО (8 Фармон)
# ==========================================

@app.on_message(filters.me & filters.command("del", prefixes="."))
async def del_msg(client, message):
    if message.reply_to_message:
        await message.reply_to_message.delete()
        await message.delete()

@app.on_message(filters.me & filters.command("purgeme", prefixes="."))
async def purge_me(client, message):
    args = message.text.split()
    count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 5
    await message.delete()
    deleted = 0
    async for msg in client.get_chat_history(message.chat.id, limit=count + 15):
        if deleted >= count: break
        if msg.from_user and msg.from_user.is_self:
            await msg.delete()
            deleted += 1

@app.on_message(filters.me & filters.command("pin", prefixes="."))
async def pin_msg(client, message):
    if message.reply_to_message:
        try:
            await message.reply_to_message.pin()
            await message.edit_text("📌 Паём заккреп шуд!")
        except Exception: await message.edit_text("❌ Ҳуқуқи админ надоред!")

@app.on_message(filters.me & filters.command("unpin", prefixes="."))
async def unpin_msg(client, message):
    if message.reply_to_message:
        try:
            await message.reply_to_message.unpin()
            await message.edit_text("📌 Откреп шуд!")
        except Exception: await message.edit_text("❌ Ҳуқуқи админ надоред!")

@app.on_message(filters.me & filters.command("read", prefixes="."))
async def read_chat(client, message):
    await client.read_chat_history(message.chat.id)
    await message.edit_text("✅ Чат хондашуда нишон дода шуд!")

@app.on_message(filters.me & filters.command("block", prefixes="."))
async def block_usr(client, message):
    reply = message.reply_to_message
    target = reply.from_user.id if reply and reply.from_user else message.chat.id
    if target == message.from_user.id:
        await message.edit_text("❌ Худатонро блок карда наметавонед!")
        return
    try:
        await client.block_user(target)
        await message.edit_text("🔒 Блок карда шуд!")
    except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("unblock", prefixes="."))
async def unblock_usr(client, message):
    reply = message.reply_to_message
    target = reply.from_user.id if reply and reply.from_user else message.chat.id
    try:
        await client.unblock_user(target)
        await message.edit_text("🔓 Аз блок бароварда шуд!")
    except Exception as e: await message.edit_text(f"❌ Хатогӣ: {e}")

@app.on_message(filters.me & filters.command("firstmsg", prefixes="."))
async def first_msg(client, message):
    async for msg in client.get_chat_history(message.chat.id, limit=1, reverse=True):
        await message.edit_text(f"🔗 **Аввалин паёми чат:**\n{msg.link}")

# ==========================================
# 5. ҲОЛАТИ AFK (2 Фармон)
# ==========================================

@app.on_message(filters.me & filters.command("afk", prefixes="."))
async def set_afk(client, message):
    global IS_AFK, AFK_REASON, AFK_TIME
    args = message.text.split(maxsplit=1)
    AFK_REASON = args[1] if len(args) > 1 else "Занятам"
    IS_AFK, AFK_TIME = True, time.time()
    await message.edit_text(f"💤 **Ҳолати AFK фаъол шуд!**\n📝 Сабаб: {AFK_REASON}")

@app.on_message(filters.me & filters.command("unafk", prefixes="."))
async def unset_afk(client, message):
    global IS_AFK
    if IS_AFK:
        IS_AFK = False
        await message.edit_text("☀️ **AFK бекор шуд! Ман баргаштам.**")

@app.on_message((filters.private | filters.mentioned) & ~filters.me)
async def afk_handler(client, message):
    if IS_AFK:
        dur = int(time.time() - AFK_TIME)
        m, s = divmod(dur, 60)
        await message.reply_text(f"🤖 **Соҳиби аккаунт онлайн нест!**\n📝 Сабаб: {AFK_REASON}\n⏱ Муддат: {m}д {s}с")

# ==========================================
# 6. МЕДИА ВА ФАЙЛҲО (6 Фармон)
# ==========================================

@app.on_message(filters.me & filters.command("download", prefixes="."))
async def dl_file(client, message):
    reply = message.reply_to_message
    if reply:
        await message.edit_text("📥 Сабт шуда истодааст...")
        p = await client.download_media(reply, file_name=DOWNLOAD_DIR)
        await message.edit_text(f"✅ Сабт шуд: `{os.path.basename(p)}`")

@app.on_message(filters.me & filters.command("save", prefixes="."))
async def save_msg(client, message):
    reply = message.reply_to_message
    if reply:
        await reply.copy("me")
        await message.edit_text("📥 Ба Saved Messages фиристода шуд!")

@app.on_message(filters.me & filters.command("tovoice", prefixes="."))
async def to_voice(client, message):
    reply = message.reply_to_message
    if reply and (reply.audio or reply.video):
        await message.edit_text("🔄 Ба Voice табдил ёфта истодааст...")
        file = await client.download_media(reply)
        await client.send_voice(message.chat.id, voice=file)
        os.remove(file)
        await message.delete()

@app.on_message(filters.me & filters.command("tosticker", prefixes="."))
async def to_sticker(client, message):
    reply = message.reply_to_message
    if reply and reply.photo:
        file = await client.download_media(reply)
        await client.send_sticker(message.chat.id, sticker=file)
        os.remove(file)
        await message.delete()

@app.on_message(filters.me & filters.command("tophoto", prefixes="."))
async def to_photo(client, message):
    reply = message.reply_to_message
    if reply and reply.sticker:
        file = await client.download_media(reply)
        await client.send_photo(message.chat.id, photo=file)
        os.remove(file)
        await message.delete()

@app.on_message(filters.me & filters.command("circle", prefixes="."))
async def to_circle(client, message):
    reply = message.reply_to_message
    if reply and reply.video:
        file = await client.download_media(reply)
        await client.send_video_note(message.chat.id, video_note=file)
        os.remove(file)
        await message.delete()

# ==========================================
# 7. ФОРМАТКУНИИ МАТН (10 Фармон)
# ==========================================

@app.on_message(filters.me & filters.command("type", prefixes="."))
async def type_anim(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return
    t = ""
    for c in args[1]:
        t += c
        await message.edit_text(t + "▒")
        await asyncio.sleep(0.08)
    await message.edit_text(t)

@app.on_message(filters.me & filters.command("shout", prefixes="."))
async def shout(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        await message.edit_text(f"📣 **{' '.join(list(args[1].upper()))}**")

@app.on_message(filters.me & filters.command("mock", prefixes="."))
async def mock(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        res = "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(args[1]))
        await message.edit_text(res)

@app.on_message(filters.me & filters.command("reverse", prefixes="."))
async def rev_text(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1: await message.edit_text(args[1][::-1])

@app.on_message(filters.me & filters.command("vapor", prefixes="."))
async def vapor_text(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1: await message.edit_text("  ".join(list(args[1])))

@app.on_message(filters.me & filters.command("upper", prefixes="."))
async def upper_text(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1: await message.edit_text(args[1].upper())

@app.on_message(filters.me & filters.command("lower", prefixes="."))
async def lower_text(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1: await message.edit_text(args[1].lower())

@app.on_message(filters.me & filters.command("bold", prefixes="."))
async def bold_text(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1: await message.edit_text(f"**{args[1]}**")

@app.on_message(filters.me & filters.command("italic", prefixes="."))
async def italic_text(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1: await message.edit_text(f"__{args[1]}__")

@app.on_message(filters.me & filters.command("spoiler", prefixes="."))
async def spoiler_text(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1: await message.edit_text(f"||{args[1]}||")

# ==========================================
# 8. АНИМАТСИЯҲО ВА БОЗИҲО (10 Фармон)
# ==========================================

@app.on_message(filters.me & filters.command("hearts", prefixes="."))
async def hearts(client, message):
    for h in ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍"]:
        await message.edit_text(f"{h} **Love Userbot** {h}")
        await asyncio.sleep(0.3)

@app.on_message(filters.me & filters.command("clock", prefixes="."))
async def clock_anim(client, message):
    for c in ["🕐", "🕒", "🕕", "🕘", "🕛"]:
        await message.edit_text(f"⏳ **Тик-так:** {c}")
        await asyncio.sleep(0.3)

@app.on_message(filters.me & filters.command("loading", prefixes="."))
async def loading(client, message):
    for i in range(0, 101, 20):
        await message.edit_text(f"🔄 **Loading:** `{i}%`\n[{'█' * (i // 10)}{'░' * (10 - i // 10)}]")
        await asyncio.sleep(0.2)
    await message.edit_text("✅ **Загрузка пурра шуд!**")

@app.on_message(filters.me & filters.command("bomb", prefixes="."))
async def bomb_anim(client, message):
    for i in range(3, 0, -1):
        await message.edit_text(f"💣 **Таркиш пас аз:** `{i}`")
        await asyncio.sleep(0.8)
    await message.edit_text("💥 **BOOM!** 💥")

@app.on_message(filters.me & filters.command("dice", prefixes="."))
async def send_dice(client, message):
    await message.delete()
    await client.send_dice(message.chat.id, "🎲")

@app.on_message(filters.me & filters.command("dart", prefixes="."))
async def send_dart(client, message):
    await message.delete()
    await client.send_dice(message.chat.id, "🎯")

@app.on_message(filters.me & filters.command("basket", prefixes="."))
async def send_basket(client, message):
    await message.delete()
    await client.send_dice(message.chat.id, "🏀")

@app.on_message(filters.me & filters.command("slot", prefixes="."))
async def send_slot(client, message):
    await message.delete()
    await client.send_dice(message.chat.id, "🎰")

@app.on_message(filters.me & filters.command("coin", prefixes="."))
async def flip_coin(client, message):
    res = random.choice(["🪙 **Орёл!**", "🪙 **Решка!**"])
    await message.edit_text(res)

@app.on_message(filters.me & filters.command("roll", prefixes="."))
async def roll_num(client, message):
    await message.edit_text(f"🎲 **Рақами омад:** `{random.randint(1, 100)}`")


# ==========================================
# 📜 РӮЙХАТИ ШАРҲДОДАШУДАИ 58 ФАРМОН (.help)
# ==========================================

@app.on_message(filters.me & filters.command("help", prefixes="."))
async def help_menu(client, message):
    help_text = (
        "📜 **РӮЙХАТИ ҲАМАИ 58 ФАРМОНИ ЮЗЕРБОТ:**\n\n"
        
        "🟢 **1. Инфо ва Система:**\n"
        "• `.ping` - Санҷиши суръат ва пинги бот\n"
        "• `.alive` - Ҳолат ва вақти кории бот (Uptime)\n"
        "• `.info` - Маълумот дар бораи корбар (бо reply)\n"
        "• `.id` - Гирифтани ID-и чат ва корбар\n"
        "• `.chatinfo` - Маълумоти пурра дар бораи чат\n"
        "• `.stat` - Статистикаи чатҳо ва каналҳо\n"
        "• `.me` - Маълумот дар бораи аккаунти худ\n"
        "• `.time` - Нишон додани вақт ва таьрихи ҷорӣ\n\n"

        "⚙️ **2. Идоракунии Аккаунт:**\n"
        "• `.setname [ном]` - Тағйир додани номи профил\n"
        "• `.setbio [матн]` - Тағйир додани Био-и профил\n"
        "• `.setpfp` - Мондани расми нав (бо reply)\n"
        "• `.restart` - Аз нав оғоз кардани бот\n\n"

        "🛡 **3. Мудирияти Гурӯҳ:**\n"
        "• `.ban` - Бан кардани корбар (бо reply)\n"
        "• `.unban` - Аз бан баровардани корбар\n"
        "• `.mute` - Хомӯш кардани чати корбар\n"
        "• `.unmute` - Баргардонидани ҳуқуқи навиштан\n"
        "• `.kick` - Пеш кардани корбар аз гурӯҳ\n"
        "• `.promote` - Админ кардани корбар\n"
        "• `.demote` - Гирифтани ҳуқуқи админӣ\n"
        "• `.tagall [матн]` - Тег кардани ҳамаи аъзоён\n"
        "• `.admins` - Рӯйхати ҳамаи админҳои чат\n"
        "• `.leave` - Баромадан аз гурӯҳ ё канал\n\n"

        "💬 **4. Идоракунии Паёмҳо:**\n"
        "• `.del` - Пок кардани паём (бо reply)\n"
        "• `.purgeme [шумора]` - Пок кардани паёмҳои худ\n"
        "• `.pin` - Заккреп кардани паём (бо reply)\n"
        "• `.unpin` - Откреп кардани паём (бо reply)\n"
        "• `.read` - Хондашуда кардани чат\n"
        "• `.block` - Блок кардани корбар\n"
        "• `.unblock` - Аз блок баровардани корбар\n"
        "• `.firstmsg` - Истинод ба аввалин паёми чат\n\n"

        "💤 **5. Ҳолати AFK:**\n"
        "• `.afk [сабаб]` - Фаъол кардани ҳолати Занятам\n"
        "• `.unafk` - Бекор кардани ҳолати AFK\n\n"

        "📥 **6. Воситаҳои Медиа:**\n"
        "• `.download` - Сабт кардани файл ба телефон\n"
        "• `.save` - Гузаронидан ба Saved Messages\n"
        "• `.tovoice` - Табдил ба Голосовой\n"
        "• `.tosticker` - Табдил додани акс ба Стикер\n"
        "• `.tophoto` - Табдил додани стикер ба Акс\n"
        "• `.circle` - Табдил ба Видеосообщение (Кругляк)\n\n"

        "✨ **7. Форматкунӣ ва Матн:**\n"
        "• `.type [матн]` - Эффекти навиштани пеши чашм\n"
        "• `.shout [матн]` - Матни ҳарфҳои калони фосиладор\n"
        "• `.mock [матн]` - Матни ҳарфҳои омехта (мАтН)\n"
        "• `.reverse [матн]` - Чаппа кардани матн\n"
        "• `.vapor [матн]` - Матни паҳншуда (в а п о р)\n"
        "• `.upper [матн]` - Ҳама ҳарфҳо КАЛОН\n"
        "• `.lower [матн]` - Ҳама ҳарфҳо хурд\n"
        "• `.bold [матн]` - Матни **ғафс**\n"
        "• `.italic [матн]` - Матни __қия__\n"
        "• `.spoiler [матн]` - Матни пӯшида (Спойлер)\n\n"

        "🎮 **8. Аниматсия ва Бозиҳо:**\n"
        "• `.hearts` - Аниматсияи дилҳои рангоранг\n"
        "• `.clock` - Аниматсияи соати тик-так\n"
        "• `.loading` - Аниматсияи сабти фоизҳо\n"
        "• `.bomb` - Аниматсияи ҳисоби ақиб ва таркиш\n"
        "• `.dice` - Партофтани зари бозӣ (🎲)\n"
        "• `.dart` - Партофтани тири Дартс (🎯)\n"
        "• `.basket` - Партофтани бӯб ба сабад (🏀)\n"
        "• `.slot` - Бозии Игровой автомат (🎰)\n"
        "• `.coin` - Партофтани танга (Орел/Решка)\n"
        "• `.roll` - Интихоби рақами тасодуфӣ (1-100)"
    )
    await message.edit_text(help_text)

print("🚀 Мега-Юзербот бо 58 фармони шарҳдор ба кор даромад!")
app.run()
