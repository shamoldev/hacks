import telebot
from telebot.types import *
import sqlite3
import requests
import random
from datetime import *
import pytz
from flask import Flask, request, jsonify
username = "Akhatkulov"

app = Flask(__name__)

bot = telebot.TeleBot("6459864183:AAFG0dlG_wLuwgjtq6My6wj5ihwaqSrCxSg",parse_mode='html')

conn = sqlite3.connect('database.db',check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS database(id INTEGER PRIMARY KEY,chat_id INTIGER UNIQUE,tarif TEXT,balance INT,lmt INT)")
conn.commit()

key = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🚫 Bekor qilish"))
back = InlineKeyboardMarkup(row_width=1)
back.add(
    InlineKeyboardButton('⬅️ Orqaga', callback_data='back1'),

    )
def more_key():
  key = InlineKeyboardMarkup(row_width=1)
  key.add(
    InlineKeyboardButton('📸  Ai Photo',callback_data='photo'),
    InlineKeyboardButton('📝 Text to Audio',callback_data='tts_menu'),
    InlineKeyboardButton('⬅️ Orqaga',callback_data='back')
  )
  return key
def tts_menu():
  key = InlineKeyboardMarkup(row_width=2)
  key.add(
InlineKeyboardButton('AI - Rano',callback_data='tts_madina'),
InlineKeyboardButton('AI - Aziz',callback_data='tts_sardor'),
  ).add(InlineKeyboardButton('⬅️ Orqaga',callback_data='back'))
  return key
@app.route('/', methods=['POST', 'GET'])
def webhook():
  if request.method == 'POST':
    data = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(data)])
    return "OK"
  else:
    return "Hello, this is your Telegram bot's webhook!"

API_URL="https://haji-api.ir/Free-GPT3/?key=hajiapi&text="
ADMIN_ID = 789945598

tz = pytz.timezone('Asia/Tashkent')

panel = InlineKeyboardMarkup(row_width=2)
panel.add(
InlineKeyboardButton('📥 Xabar yuborish', callback_data='reklama'),
    InlineKeyboardButton('📝 Forward Xabar', callback_data='forward')

    ).add(
    InlineKeyboardButton('📊 Statistika', callback_data='stat')
   ).add(
    InlineKeyboardButton('✅ Premium', callback_data='set'),
    InlineKeyboardButton('❌ Premium', callback_data='del')
   ).add(InlineKeyboardButton('🏡 Bosh sahifa', callback_data='register'))
START_TEXT = """<b>
👋 Assalomu alaykum %name% 

Bot sizga savollaringizga javob topishda yordam beradi. Foydalanish uchun shunchaki savolingizni botga yozish kifoya.

Bot nimalar qiloladi?
1. Savolga javob berish;
2. Kod yozish va uni tahrirlash;
3. Har xil turdagi matnlar yozish va ularni tahrirlash;
4. Matnni barcha tillarda tarjima qilish;
5. Insho, she’r yozish va hokazolar.

Buyruqlar:
/start - Botni qayta ishga tushirish
/help - Foydalanish qo’llanmasi

Bot savollarga qancha tez javob beradi?
Bir necha soniyadan bir necha daqiqagacha.</b>
"""

CARD_TEXT =f"""<b>
💳 To'lov turlari
</b>
<b>Click:</b> <code>9860 1301 4550 4358</code>
<b>QIWI:</b> <code><a href="https://qiwi.com/n/METAFRA">LINK</a>
<b>
💸 Suma: 10.000 uzs

🟢Ps:To'lov qilib bo'lgach,  to'laganlik xaqidagi (скриншот, scrinshot)rasmga olib Telegram: @{username} ga rasm shaklida tashlash kerak!

〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️
Texnik qo'llab-quvvatlash.
Telegram: @{username}</b>"""
HELP_TEXT = """<b>
Bot OpenAI kompaniyasining ChatGPT sun’iy intellektiga ulangan. Foydalanish uchun shunchaki savolingizni botga yozish kifoya.

Buyruqlar:
/start - Botni qayta ishga tushirish
/help - Foydalanish qo’llanmasi

Foydalanish qo’llanmasi:
Bot bilan haqiqiy suhbatdoshdek, har xil tillarda so’zlashishingiz mumkin. E’tibor bering, ba’zida bot savolga xato javob berishi mumkin, bot faqat 2021 yilgacha ma’lumotlarga ega. Maksimal to’g’ri javob olish uchun savolingizni iloji boricha batafsilroq yozing.

Botga qo’shiladigan yangi funksiyalarni birinchilardan sinash uchun bot rasmiy kanaliga obuna bo’ling: @Akhatkulov_blog

Taklif va murojaatlar uchun: @Akhatkulov</b>
"""
BACK  =InlineKeyboardMarkup().add(InlineKeyboardButton('🔙 Back', callback_data='back'))
del_key  =InlineKeyboardMarkup().add(InlineKeyboardButton('❌', callback_data='delall'),InlineKeyboardButton('✅', callback_data='true'))
#
def ai_photo(msg):
  try:
    txt = msg.text
    a=requests.get("https://bekkoder.pythonanywhere.com/?text="+txt).json()["images"]
    h=[]
    for i in range(0,3):
      try:
        h.append(InputMediaPhoto(
           media = requests.get(a[i]).content,
           caption = "<b>Rano-AI.uz - @RanoAI_bot</b>",
          parse_mode="html"

          #reply_markup=more_key()
        ))
      except:
        pass
    #rand = random.randint(0,len(a)//2)
    
    b = bot.send_media_group(chat_id=msg.chat.id,media=h)[0].message_id
    bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption="<b>Rano-AI.uz - @RanoAI_bot</b>",reply_to_message_id=b,reply_markup=more_key())
  except Exception as e:
    print(e)
  
def ads_send(message):
    try:
        text = message.text
        if text=="🚫 Bekor qilish":
            bot.send_photo(message.chat.id,photo="https://t.me/the_solodest/178",caption="🚫 Xabar yuborish bekor qilindi !",reply_markup=back)
        else:
            cursor.execute("SELECT chat_id FROM database")
            rows = cursor.fetchall()
            for i in rows:
                chat_id = i[0]
                print(chat_id)
                bot.send_message(chat_id,message.text)
            bot.send_photo(ADMIN_ID,photo="https://t.me/the_solodest/178",caption="<b>✅ Xabar hamma foydalanuvchiga yuborildi!</b>",reply_markup=back)
    except:
        pass
def for_send(message):
    text = message.text
    if text == "🚫 Bekor qilish":
        bot.send_photo(message.chat.id,photo="https://t.me/the_solodest/178",caption="🚫 Xabar yuborish bekor qilindi!", reply_markup=back)
    else:
        cursor.execute("SELECT chat_id FROM database")
        rows = cursor.fetchall()
        for row in rows:
            try:
                chat_id = row[0]
                print(chat_id)
                bot.forward_message(chat_id, ADMIN_ID, message.message_id)
            except Exception as e:
                print(e)
        bot.send_message(ADMIN_ID, "✅ Xabar hamma foydalanuvchiga yuborildi!", reply_markup=back)

def menu():
    key = InlineKeyboardMarkup()
    key.add(
        InlineKeyboardButton('ℹ️ Qollanma', callback_data='docs'),
        InlineKeyboardButton('📱 Kabinet', callback_data='profile')
        
    ).add(
      InlineKeyboardButton('🌅 More',callback_data='more'),
      InlineKeyboardButton('💸 To\'lash', callback_data='pay')
      
    )
    return key
def _madina_tts(msg):
  if msg.text=="🚫 Bekor qilish":
    bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption="<b>❌ Bekor qilindi !</b>",reply_markup=menu())
  else:
    json_data = {
      "userId": "public-access",
      "platform": "landing_demo",
      "ssml": f"<speak><p>{msg.text}</p></speak>",
      "voice": "uz-UZ-MadinaNeural",
      "narrationStyle": "regular"
    }
    bot.send_chat_action(msg.chat.id, 'upload_audio')
    requests.post("https://play.ht/api/transcribe", json=json_data)
    response = requests.post("https://play.ht/api/transcribe", json=json_data).json()['file']
    with open(f"{msg.chat.id}.ogg",'wb')  as f:
      f.write(requests.get(response).content)
    with open(f"{msg.chat.id}.ogg",'rb')  as f:
      bot.send_voice(msg.chat.id,voice=f,caption="<b>@Akhatkulov</b>",reply_markup=tts_menu())
    os.remove(f"./{msg.chat.id}.ogg")

    
def _sardor_tts(msg):
  if msg.text=="🚫 Bekor qilish":
    bot.send_photo(msg.chat.id,photo="http://telegra.ph//file/ee1281dbb6d16ef432055.jpg",caption="<b>❌ Bekor qilindi !</b>",reply_markup=menu())
  else:
    json_data = {"userId":"public-access","platform":"landing_demo","ssml":f"<speak><p>{msg.text}</p></speak>","voice":"uz-UZ-SardorNeural","narrationStyle":"regular"}
    bot.send_chat_action(msg.chat.id, 'upload_audio')
    mrequests.post("https://play.ht/api/transcribe", json=json_data)
    response = requests.post("https://play.ht/api/transcribe", json=json_data).json()['file']
    with open(f"{msg.chat.id}.ogg",'wb')  as f:
      f.write(requests.get(response).content)
    with open(f"{msg.chat.id}.ogg",'rb')  as f:
      bot.send_voice(msg.chat.id,voice=f,caption="<b>Rano-AI.uz - @RanoAI_bot</b>",reply_markup=tts_menu())
    os.remove(f"./{msg.chat.id}.ogg")

def premium_set(msg):
  if msg.text=="🚫 Bekor qilish":
    bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption="<b>❌ Bekor qilindi !</b>",reply_markup=panel)
  else:
    try:
      cursor.execute(f"SELECT * FROM database WHERE chat_id={msg.text}")
      rows = cursor.fetchone()
  
      print(rows)
      if(rows):
        cursor.execute(f"UPDATE database SET tarif='Premium' WHERE chat_id={msg.text}")
        conn.commit()
        bot.send_photo(msg.text,photo="https://t.me/the_solodest/178",caption="<b>✅ Sizning tarifingiz Premium ga o'tkazildi!</b>",reply_markup=manu())
        
        bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption=f"<b>✅ <a href='tg://user?id={msg.text}'>{bot.get_chat(msg.text).first_name}</a>  Premium ga o'tkazildi!</b>",reply_markup=panel)
      else:
        bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption="<b>❌ Foydalanuvchi topilmadi !</b>",reply_markup=panel)
    except:
      pass
def premium_del(msg):
  if msg.text=="🚫 Bekor qilish":
    bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption="<b>❌ Bekor qilindi !</b>",reply_markup=panel)
  else:
    try:
      cursor.execute(f"SELECT * FROM database WHERE chat_id={msg.text}")
      rows = cursor.fetchone()
  
      print(rows)
      if(rows):
        cursor.execute(f"UPDATE database SET tarif='Oddiy' WHERE chat_id={msg.text}")
        conn.commit()
        bot.send_photo(msg.text,photo="https://t.me/the_solodest/178",caption="<b>✅ Sizning tarifingiz Oddiy ga o'tkazildi!</b>",reply_markup=menu())
        bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption=f"<b>✅ <a href='tg://user?id={msg.text}'>{bot.get_chat(msg.text).first_name}</a>  Oddiy ga o'tkazildi!</b>",reply_markup=panel)
      else:
        bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption="<b>❌ Foydalanuvchi topilmadi !</b>",reply_markup=panel)
    except:
      pass
@bot.message_handler(commands=['start'])
def _welcome(msg):
    try:
        cursor.execute("INSERT INTO database(chat_id,tarif,balance,lmt) VALUES (?,?,?,?)", (msg.chat.id,'Oddiy',0,100))
        conn.commit()
        bot.send_message(ADMIN_ID,f"<b>👤 Yangi <a href='tg://user?id={msg.chat.id}'>{msg.from_user.first_name}</a> qo'shildi!</b>",parse_mode='html')
    except sqlite3.IntegrityError:
        pass
    bot.send_photo(msg.chat.id,"https://t.me/the_solodest/178",caption=START_TEXT.replace("%name%",msg.from_user.first_name),reply_markup=menu())
    
@bot.message_handler(content_types=['text'])
def chat_gpt(msg):
   savol = msg.text
   if msg.text == '/panel' and msg.chat.id == ADMIN_ID:
      bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",
                     caption="<b>🧑‍💻 Admin panelga Xush-kelibsiz!</b>",
                     reply_markup=panel)
   else:
      try:
          bot.send_chat_action(msg.chat.id,action='typing')
          
          cursor.execute(f"SELECT * FROM database WHERE chat_id='{msg.chat.id}'")
          rows = cursor.fetchone()
          tarif = rows[2]
          if tarif=='Oddiy':
            limit = rows[4]
            if int(limit)>0:
              
              cursor.execute(f"UPDATE database SET lmt={limit-1} WHERE chat_id={msg.chat.id}")
              conn.commit()
              txt = requests.get(API_URL+savol).json()['result']['answer']
              bot.send_message(msg.chat.id,text=txt,parse_mode='markdown',reply_markup=del_key)
            else:
              bot.send_photo(msg.chat.id,photo="https://t.me/the_solodest/178",caption="<b>Sizning tarifingiz tugadi!</b>",reply_markup=menu())
              
            
          else:
            txt = requests.get(API_URL+savol).json()['result']['answer']
            bot.send_message(msg.chat.id,text=txt,parse_mode='markdown')
      except Exception as e:
          bot.send_message(msg.chat.id,f"<b>🛠 Kechirasiz texnik nosozlik! {e}</b>")
          bot.send_message(ADMIN_ID,f"{e+txt}")

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
   data = call.data
   user_id = call.message.chat.id
   if data=='profile':
    cursor.execute(f"SELECT * FROM database WHERE chat_id='{user_id}'")
    rows = cursor.fetchone()
    tarif = rows[2]
    balance = rows[3]
    limit = rows[4]
    if tarif=="Premium":
      limit = "♾"
    userid = rows[0]
    PROFILE = f"""<b>
🏠ID raqamingiz: {user_id}

💸 Balansingiz: {balance} so'm
Limit: {limit}

🔔Tarif: {tarif}
ℹ️ ID : {userid}
</b>
    """
    bot.edit_message_caption(PROFILE,chat_id=user_id,message_id=call.message.id,parse_mode='html',reply_markup=BACK)
   elif data=='back':
    a = (call.from_user.first_name)
    bot.edit_message_caption(START_TEXT.replace("%name%",a),chat_id=user_id,message_id=call.message.id,parse_mode='html',reply_markup=menu())
   elif data=="more":
     bot.edit_message_caption("<b>O'zingizga kerakli bo'limni tanlang 👇</b>",chat_id=user_id,message_id=call.message.id,parse_mode='html',reply_markup=more_key())
   elif data=='docs':
        bot.edit_message_caption(HELP_TEXT,chat_id=user_id,message_id=call.message.id,parse_mode='html',reply_markup=BACK) 
   elif data == 'pay':
    bot.edit_message_caption(CARD_TEXT,
                            chat_id=user_id,
                            message_id=call.message.id,
                            parse_mode='html',
                            reply_markup=BACK)
   if data == "register":
      a = (call.from_user.first_name)
      bot.edit_message_caption(chat_id=user_id,
                            caption=START_TEXT.replace("%name%",a),
                            message_id=call.message.id,
                            parse_mode='html',
                            reply_markup=menu())
   if data=="tts_menu":
     bot.edit_message_caption("<b>O'zingizga kerakli AI tanlang 👇</b>",chat_id=user_id,message_id=call.message.id,parse_mode='html',reply_markup=tts_menu())
   if data == "delall":
      bot.answer_callback_query(call.id, "🙏 Sorry",show_alert=True)
      bot.delete_message(user_id, call.message.id)
   if data=='true':
     bot.answer_callback_query(call.id, "🙏 Thank you",show_alert=True)
   try:
      callback_data = data
      if callback_data == 'stat' and user_id == ADMIN_ID:
        cursor.execute("SELECT COUNT(chat_id) FROM database")
        rows = cursor.fetchall()
        bot.edit_message_caption(f"<b>📊 Bot obunachilari soni: {rows[0][0]}</b>",
                              user_id,
                              call.message.id,
                              reply_markup=back)
      if callback_data == 'back1' and user_id == ADMIN_ID:
        bot.edit_message_caption(chat_id=user_id,caption=f"<b>🧑‍💻 Admin panelga Xush-kelibsiz!</b>",message_id=call.message.id,reply_markup=panel)
      if callback_data == 'reklama' and user_id == ADMIN_ID:
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>✍️ Xabar matnini kiritng !</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver, ads_send)
      if callback_data == 'tts_madina':
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>✍️ Xabar matnini kiritng !</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver,_madina_tts)
      if callback_data == 'tts_sardor':
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>✍️ Xabar matnini kiritng !</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver, _sardor_tts)
      if callback_data == 'forward' and user_id == ADMIN_ID:
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>✍️ Xabar matnini kiritng !</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver, for_send)
      if callback_data == 'set' and user_id == ADMIN_ID:
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>Enter chat_id..</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver, premium_set)
      if callback_data == 'del' and user_id == ADMIN_ID:
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>Enter chat_id..</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver, premium_del)
      if callback_data=="photo":
        bot.delete_message(user_id, call.message.id)
        adver = bot.send_message(user_id,
                                 "<b>Matn kiriting.</b>",
                                 reply_markup=key)
        bot.register_next_step_handler(adver,ai_photo)
        

   except Exception as e:
      bot.send_photo(ADMIN_ID,photo="https://t.me/the_solodest/178",caption=f"<b>Error {e}</b>", reply_markup=panel)
   except Exception as e:
    bot.send_photo(ADMIN_ID,photo="https://t.me/the_solodest/178",caption=f"<b>Error {e}</b>", reply_markup=panel)



print(bot.get_me())
bot.infinity_polling()
