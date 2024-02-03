from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""MERHABA {msg.from_user.mention},

Benim adım {me2},
string generator bot.
Tamamen güvenlidir.
Hata yok.

BOT SAHİBİ  : [@benkadir](tg://user?id={OWNER_ID}) !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="SESSİON OLUŞTUR", callback_data="session")
                ],
                [
                    InlineKeyboardButton("KANALIMIZ", url="https://t.me/dilemin"),
                    InlineKeyboardButton("DESTEK", url="https://t.me/benkadir")
                ]
            ]
        ),
        disable_web_page_preview=True,
)
