import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import random
import threading
import asyncio
from flask import Flask

# ==========================================
# 1. НАСТРОЙКА ВЕБ-СЕРВЕРА ДЛЯ ПИНГОВ (ОТ СНА)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Бот активен и не спит!"

def run_web_server():
    # Render автоматически выделяет порт через переменную окружения PORT, 
    # либо используем 8080 по умолчанию
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# 2. НАСТРОЙКА БОТА И БАЗЫ ДАННЫХ
# ==========================================
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

@dp.message(Command("баланс") | (F.text.lower() == "баланс"))
async def cmd_balance(message: Message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    
    cursor.execute("SELECT balance_coins, balance_gems FROM users WHERE user_id = ?", (user_id,))
    coins, gems = cursor.fetchone()
    
    await message.reply(f"🪙 Ваши монеты: {coins}\n💎 Ваши гемы: {gems}", parse_mode="Markdown")

@dp.message(Command("магазин") | (F.text.lower() == "магазин"))
async def cmd_shop(message: Message):
    text = (
        "🛒 Магазин товаров Starbally\n\n"
        "1️⃣ Снять варн — 20 гемов\n"
        "2️⃣ Личный тег (префикс) — 100 монет\n\n"
        "💬 Чтобы купить, пишите: /купить [номер] [если надо, текст префикса]\n"
        "Пример: /купить 2 Топ Игрок"
    )
    await message.reply(text, parse_mode="Markdown")

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
        if gems < 20:
            return await message.reply("❌ У вас не хватает гемов! Нужно 20 💎")
        if warns == 0:
            return await message.reply("❌ У вас нет активных варнов.")
            
        cursor.execute("UPDATE users SET balance_gems = balance_gems - 20, warns = warns - 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        await message.reply("✅ Успешно! С вас списано 20 гемов, 1 варн снят.")
        
    elif item_id == "2":
        if len(args) < 3:
            return await message.reply("❌ Напишите текст вашего префикса после номера товара! Пример: /купить 2 Админ")
        if coins < 100:
            return await message.reply("❌ У вас не хватает монет! Нужно 100 🪙")
            
        new_tag = args[2][:15]
        cursor.execute("UPDATE users SET balance_coins = balance_coins - 100, custom_tag = ? WHERE user_id = ?", (new_tag, user_id))
        conn.commit()
        await message.reply(f"✅ Успешно! Установлен новый префикс: [{new_tag}]")
    else:
        await message.reply("❌ Такого товара не существует.")

@dp.message(Command("казино"))
async def cmd_casino(message: Message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    
    args = message.text.split()
    if len(args) < 2:
        return await message.reply("❌ Укажите ставку! Пример: /казино 50")
        
    try:
        bet = int(args[1])
    except ValueError:
        return await message.reply("❌ Ставка должна быть числом!")
        
    if bet <= 0:
        return await message.reply("❌ Ставка должна быть больше 0!")
        
    cursor.execute("SELECT balance_coins FROM users WHERE user_id = ?", (user_id,))
    coins = cursor.fetchone()[0]
    
    if coins < bet:
        return await message.reply("❌ У вас недостаточно монет для такой ставки!")
        
    if random.randint(1, 100) <= 45:
        cursor.execute("UPDATE users SET balance_coins = balance_coins + ? WHERE user_id = ?", (bet, user_id))
        conn.commit()
        await message.reply(f"🎰 Вы выиграли! Вы получили {bet} монет! 🎉", parse_mode="Markdown")
    else:
        cursor.execute("UPDATE users SET balance_coins = balance_coins - ? WHERE user_id = ?", (bet, user_id))
        conn.commit()
        await message.reply(f"🎰 Вы проиграли! Вы потеряли {bet} монет. 📉", parse_mode="Markdown")

# ==========================================
# 4. ЗАПУСК ВЕБ-СЕРВЕРА И БОТА
# ==========================================
async def main():
    # Запуск веб-сервера в фоновом потоке
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Бот и веб-сервер успешно запущены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
