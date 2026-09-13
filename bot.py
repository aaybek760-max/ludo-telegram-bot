import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN =8251349766:AAGPMazrz

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎲 LUDO BOT\n\n"
        "Ludo o‘ynash uchun /ludo buyrug‘ini bosing.\n"
        "👥 2–4 kishilik o‘yin."
    )


@dp.message(Command("ludo"))
async def ludo(message: types.Message):
    dice = random.randint(1, 6)
    await message.answer(
        f"🎲 Ludo o‘yini boshlandi!\n\n"
        f"👤 O‘yinchi: {message.from_user.first_name}\n"
        f"🎲 Kubik: {dice}\n\n"
        "Yana tashlash uchun /ludo ni bosing."
    )


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
