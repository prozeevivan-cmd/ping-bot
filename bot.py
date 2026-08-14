import os
import sqlite3
import random
import threading
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from flask import Flask

# ==========================================
# 1. НАСТРОЙКА ВЕБ-СЕРВЕРА ДЛЯ УПТИМЕ-РОБОТА
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Бот работает и готов к пингам UptimeRobot!"

def run_web_server():
    # Запуск веб-сервера на порту 8080
    app.run(host='0.0.0.0', port=8080)

# ==========================================
# 2. НАСТРОЙКА БОТА И БАЗЫ ДАННЫХ
# ==========================================
# Токен прописан прямо в коде
TOKEN = "8935315154:AAEtbDIDrCfStciV91IP7B8W8LutcYBtCiE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Подключаем базу данных SQLite
conn = sqlite3.connect("economy.db", check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу пользователей, если её нет
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    balance_coins INTEGER DEFAULT 100,
    balance_gems INTEGER DEFAULT 5,
    custom_tag TEXT DEFAULT 'Игрок',
    warns INTEGER DEFAULT 0
)
""")
conn.commit()

# Функция для быстрой проверки/добавления игрока в базу
def check_user(user_id, username):
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (user_id, username) VALUES (?, ?)", 
            (user_id, username or f"id{user_id}")
        )
        conn.commit()

# ==========================================
# 3. КОМАНДЫ БОТА
# ==========================================

# Команда /профиль или профиль
@dp.message(Command("профиль") | (F.text.lower() == "профиль"))
async def cmd_profile(message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    check_user(user_id, username)
    
    cursor.execute("SELECT balance_coins, balance_gems, custom_tag, warns FROM users WHERE user_id = ?", (user_id,))
    coins, gems, tag, warns = cursor.fetchone()
    
    text = (
        f"🌟 Профиль игрока {username}\n\n"
        f"🏷 Префикс: [{tag}]\n"
        f"🪙 Монеты: {coins}\n"
        f"💎 Гемы: {gems}\n"
        f"⚠️ Предупреждения (Варны): {warns}/3"
    )
    await message.reply(text, parse_mode="Markdown")

# Команда /баланс или баланс
@dp.message(Command("баланс") | (F.text.lower() == "баланс"))
async def cmd_balance(message: Message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    
    cursor.execute("SELECT balance_coins, balance_gems FROM users WHERE user_id = ?", (user_id,))
    coins, gems = cursor.fetchone()
    
    await message.reply(f"🪙 Ваши монеты: {coins}\n💎 Ваши гемы: {gems}", parse_mode="Markdown")

# Команда /магазин или магазин
@dp.message(Command("магазин") | (F.text.lower() == "магазин"))
async def cmd_shop(message: Message):
    text = (
        "🛒 Магазин товаров Starbally\n\n"
        "1️⃣ Снять варн — 20 гемов\n"
        "2️⃣ Личный тег (префикс) — 100 монет\n\n"
        " Чтобы купить, пишите: /купить [номер] [если надо, текст префикса]\n"
        "Пример: /купить 2 Топ Игрок"
    )
    await message.reply(text, parse_mode="Markdown")

# Команда /купить
@dp.message(Command("купить"))
async def cmd_buy(message: Message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        return await message.reply("❌ Укажите номер товара! Пример: /купить 1")
        
    item_id = args[1]
    
    cursor.execute("SELECT balance_coins, balance_gems, warns FROM users WHERE user_id = ?", (user_id,))
    coins, gems, warns = cursor.fetchone()
    
    if item_id == "1":
        if warns <= 0:
            return await message.reply("❌ У вас нет предупреждений!")
        if gems < 20:
            return await message.reply("❌ У вас недостаточно гемов! Нужно 💎 20.")
            
        cursor.execute("UPDATE users SET balance_gems = balance_gems - 20, warns = warns - 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        await message.reply("✅ Вы успешно сняли один варн за 20 гемов!")
        
    elif item_id == "2":
        if len(args) < 3:
            return await message.reply("❌ Укажите текст для префикса! Пример: /купить 2 Легенда")
        
        new_tag = args[2]
        if len(new_tag) > 15:
            return await message.reply("❌ Префикс слишком длинный! Максимум 15 символов.")
        if coins < 100:
            return await message.reply("❌ У вас недостаточно монет! Нужно 🪙 100.")
            
        cursor.execute("UPDATE users SET balance_coins = balance_coins - 100, custom_tag = ? WHERE user_id = ?", (new_tag, user_id))
        conn.commit()
        await message.reply(f"✅ Вы успешно сменили префикс на: [{new_tag}]")
    else:
        await message.reply("❌ Такого товара не существует в магазине.")

# ==========================================
# 4. ЗАПУСК БОТА И ВЕБ-СЕРВЕРА
# ==========================================
async def main():
    # Запускаем веб-сервер в фоновом режиме для UptimeRobot
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Бот и веб-сервер успешно запущены!")
    # Запуск бота (поллинг)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
