import asyncio
import time
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Токен вашего бота
TOKEN = "8975709751:AAGQrX27XnEM7TDCH_ENUOqWuuFSZQk2W0k"

# Параметры из вашего конфига
TARGET_URL = "https://wl.wlrus.lol/media/live/"
HEADERS = {
    "Accept": "*/*",
    "Cookie": "session_id=c82ad25936fa2f3776a6d0a1767d4799",
    "Origin": "https://wl.wlrus.lol/",
    "Referer": "https://wl.wlrus.lol/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) Gecko/20100101 Firefox/151.0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("ping"))
async def cmd_ping(message: types.Message):
    msg = await message.answer("🏓 Пингуем сервер Норвегия (xhttp)...")
    
    start_time = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=10.0, http2=True) as client:
            response = await client.get(TARGET_URL, headers=HEADERS)
            
        end_time = time.perf_counter()
        ping_ms = round((end_time - start_time) * 1000)
        
        await msg.edit_text(
            f"✅ **Сервер доступен!**\n"
            f"🇳🇴 **Норвегия - БС**\n"
            f"⏱ Пинг (HTTP GET): `{ping_ms} ms`\n"
            f"🌐 Статус ответа: `{response.status_code}`",
            parse_mode="Markdown"
        )
    except httpx.RequestError as e:
        await msg.edit_text(
            f"❌ **Ошибка соединения с сервером!**\n"
            f"🛠 Детали: `{str(e)}`",
            parse_mode="Markdown"
        )

# Заглушка веб-сервера для Render, чтобы он видел открытый порт
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    # Render передает порт через переменную окружения PORT
    port = 8080 
    import os
    if "PORT" in os.environ:
        port = int(os.environ["PORT"])
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    # Запускаем веб-сервер и бота одновременно
    await start_web_server()
    print("Бот и веб-сервер запущены...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
