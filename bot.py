import os
import telebot
import requests

# Botingiz maxfiy tokeni
API_TOKEN = '8830595692:AAEGH8ixVd9vWLljlNxkC56eho86-X72iv8'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Oqqush** botiga xush kelibsiz!\n\n"
        "🎬 Menga **Instagram Reels** yoki **TikTok** video havolasini (linkini) yuboring, yuklab beraman.\n"
        "🎵 Yoki shunchaki qo'shiq nomini yozing, musiqalarni topib beraman!"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    
    # Instagram yoki TikTok havolasi bo'lsa
    if "instagram.com" in text or "tiktok.com" in text:
        status_msg = bot.reply_to(message, "⏳ Havola tekshirilmoqda va yuklanmoqda, iltimos kuting...")
        
        try:
            # Render uchun maxsus, eng tezkor bepul yuklovchi API
            api_url = f"https://workers.dev{text}"
            response = requests.get(api_url, timeout=20).json()
            
            if response.get("url"):
                video_url = response["url"]
                bot.send_video(message.chat.id, video_url, caption="✨ Video muvaffaqiyatli yuklab olindi! \n@Oqqush_bot")
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ Videoni yuklab bo'lmadi. Havola xato yoki profil yopiq bo'lishi mumkin.", message.chat.id, status_msg.message_id)
        except Exception as e:
            bot.edit_message_text("❌ Tizimda yuklanish. Birozdan so'ng qayta urinib ko'ring.", message.chat.id, status_msg.message_id)

    # Musiqa qidirish qismi
    else:
        status_msg = bot.reply_to(message, f"🎵 '{text}' bo'yicha musiqalar qidirilmoqda...")
        try:
            # Renderda 100% cheklovsiz ishlaydigan katta musiqa bazasi API'si
            music_api = f"https://apple.com{text}&media=music&limit=3"
            res = requests.get(music_api, timeout=15).json()
            
            if res.get("resultCount", 0) > 0:
                bot.delete_message(message.chat.id, status_msg.message_id)
                for track in res["results"]:
                    title = track["trackName"]
                    artist = track["artistName"]
                    audio_url = track["previewUrl"]
                    bot.send_audio(message.chat.id, audio_url, caption=f"🎧 {artist} - {title}")
            else:
                bot.edit_message_text("🔍 Afsuski, bunday nomdagi musiqa topilmadi.", message.chat.id, status_msg.message_id)
        except Exception as e:
            bot.edit_message_text("❌ Musiqa qidirish xizmatida vaqtinchalik uzilish yuz berdi.", message.chat.id, status_msg.message_id)

if __name__ == '__main__':
    bot.infinity_polling()
  
