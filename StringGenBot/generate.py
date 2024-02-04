from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "» Lütfen bir oturum dizesi seçiniz :"
buttons_ques = [
    [
        InlineKeyboardButton("PYROGRAM", callback_data="pyrogram1"),
        InlineKeyboardButton("PYROGRAM V2", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton("TELETHON", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("PYROGRAM BOT", callback_data="pyrogram_bot"),
        InlineKeyboardButton("TELETHON BOT", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text=" OTURUM OLUŞTUR ", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "TELETHON"
    else:
        ty = "PYROGRAM"
        if not old_pyro:
            ty += " V2"
    if is_bot:
        ty += " BOT"
    await msg.reply(f"» DİZE OLUŞTURULUYOR {ty} SESSİON GENERATOR")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "Lütfen API_ID numaranızı giriniz.\n\nYada /iptal yazınız.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("API_ID numaranız yanlış, Lütfen tekrar başlatınız.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "» Lütfen API_HASH numaranızı giriniz ve devam ediniz.", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "» Lütfen telefon numaranızı ülke kodu ile giriniz. \nÖRNEK : `+910000000000`'"
    else:
        t = "Lütfen ʙᴏᴛ_ᴛᴏᴋᴇɴ numaranızı giriniz ve devam ediniz.\nÖRNEK : `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("» kod göndermeye çalışıyorum...")
    else:
        await msg.reply("» Bot token ile giriş yapmaya çalışıyorum...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("» ᴀᴩɪ_ɪᴅ ve ᴀᴩɪ_ʜᴀsʜ numaranız telegram sistemi ile eşleşmiyor. \n\nLütfen tekrar deneyiniz..", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except ("Yanlış telefon numarası girdiniz, Telefon numaranız geçersiz, telefon numaranız hatalı."):
        await msg.reply("» girdiğiniz ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ herhangi bir telegram hesabına ait değil.\n\nLütfen tekrar deneyiniz.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "» Lütfen kodunuzu giriniz.\n kodunuz `12345`, Lütfen aralarında boşluk bırakarak giriniz `1 2 3 4 5`.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("» 10 dakikalık süre aşıldı.\n\nLütfen tekrar deneyiniz.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply("» Yanlış kod girdiniz\n\nLütfen tekrar deneyiniz.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply("» Yanlış kod girdiniz\n\nLütfen tekrar deneyiniz.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            try:
                two_step_msg = await bot.ask(user_id, "» Lütfen iki adımlı doğrulama şifrenizi giriniz.", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("» 5 dakikalık süre aşıldı.\n\nLütfen tekrar deneyiniz.", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await two_step_msg.reply("» Yanlış şifre girdiniz.\n\nLütfen tekrar deneyiniz.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"Session dizeniz {ty} burada \n\n`{string_session}` \n\n Oluşturan : @Sessionkeyfibot\n not: Kimse ile paylaşmayınız @benkadir"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "» session dizeniz {} kayıtlı mesajlanıza eklendi.\n\nlütfen kayıtlı mesajlarınızı kontrol ediniz ! \n\n Oluşturan @Sessionkeyfibot".format("ᴛᴇʟᴇᴛʜᴏɴ" if telethon else "ᴩʏʀᴏɢʀᴀᴍ"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("» işlem iptal edildi!", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("» BOT YENİDEN BAŞLATILDI. !", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("» Devam eden dize oluşturma işlemi iptal edildi !", quote=True)
        return True
    else:
        return False
