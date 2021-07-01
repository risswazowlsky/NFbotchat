import amanobot
import amanobot.namedtuple
from amanobot.namedtuple import File, InlineKeyboardMarkup, InlineKeyboardButton
from amanobot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply
import random
import requests
from bs4 import BeautifulSoup
import time
import os
import json
from glob import glob
import pytz
from datetime import datetime
from config import TOKEN, ADMIN, OWNER, INSTAGRAM, CHANNEL, GROUP, PROJECT_NAME

token = TOKEN
bot = amanobot.Bot(token)

queue = {
	"free":[],
	"occupied":{}
}
users = []
user3 = []

def saveConfig(data):
	return open('app.json', 'w').write(json.dumps(data))

if __name__ == '__main__':
	s = time.time()
	print(f'[#] Buatan oleh\n[i] Created by {OWNER}\n')
	print('[#] mengecek config...')
	if not os.path.isfile('app.json'):
		print('[#] memebuat config file...')
		open('app.json', 'w').write('{}')
		print('[#] Done')
	else:
		print('[#] Config found!')
	print('[i] Bot online ' + str(time.time() - s) + 's')
def exList(list, par):
	a = list
	a.remove(par)
	return a

def handle(update):
		
	global queue
	try:
		config = json.loads(open('app.json', 'r').read())
		if 'text' in update:
			text = update["text"]
		else:
			text = ""
		uid = update["chat"]["id"]
		
		if uid not in user3:
			users.append(uid)
		
		if not uid in config and text != "/nopics":
			config[str(uid)] = {"pics":True}
			saveConfig(config)

		if uid in queue["occupied"]:
			if 'text' in update:
				if text != "/exit" and text != "❌ Exit" and text != "Next ▶️" and text != "/next":
					bot.sendMessage(queue["occupied"][uid], "" + text)
			
			if 'photo' in update:
				photo = update['photo'][0]['file_id']
				bot.sendPhoto(queue["occupied"][uid], photo, caption=captionphoto)

			if 'video' in update:
				video = update['video']['file_id']
				bot.sendVideo(queue["occupied"][uid], video, caption=captionvideo)
				
			if 'document' in update:
				document = update['document']['file_id']
				bot.sendDocument(queue["occupied"][uid], document, caption=captionducument)
				
			if 'audio' in update:
				audio = update['audio']['file_id']
				bot.sendAudio(queue["occupied"][uid], audio, caption=captionaudio)
				
			if 'video_note' in update:
				video_note = update['video_note']['file_id']
				bot.sendVideoNote(queue["occupied"][uid], video_note)
			
			if 'voice' in update:
				voice = update['voice']['file_id']
				bot.sendVoice(queue["occupied"][uid], voice, caption=captionvoice)

			if 'sticker' in update:
				sticker = update['sticker']['file_id']
				bot.sendSticker(queue["occupied"][uid], sticker)

			if 'contact' in update:
				nama = update["contact"]["first_name"]
				contact = update['contact']['phone_number']
				bot.sendContact(queue["occupied"][uid], contact, first_name=nama, last_name=None)
		

		if text == "/start" or text == "/refresh":
			if not uid in queue["occupied"]:
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="👑 Owner", url=f"https://t.me/pachemild"),InlineKeyboardButton(text="📮 Instagram", url=f"https://instagram.com/nishfu_im"),InlineKeyboardButton(text="💬 Grup Chat", url=f"https://t.me/HappyZgameBot")]])
				bot.sendMessage(uid, f"{PROJECT_NAME} is a bot for meetings.\n\n_🇮🇩 You can find Partner and start Chatting.\n⏺️ I hope you share this bot.\n\n💬 /Search to find a your Partner.", parse_mode='MarkDown', disable_web_page_preview=True , reply_markup=keyboard)
		if 'message_id' in update:
			if not uid in queue["occupied"]:
				if text != "/start" and text != "Pengguna 👤" and text !="Next ▶️" and text != "/refresh" and text != "/help" and text != "/search" and text != "Search Partner 🔍" and text != "🛠 Menu Bot" and text != "🔙 Main Menu" and text != "Info Profile 📌" and text != "📝 Info Covid-19"  and text != "/user":
					news = ReplyKeyboardRemove()
					bot.sendMessage(uid, "_[❗️] You don't have partner\nTo find your partner /search_", parse_mode="MarkDown",reply_markup=news, reply_to_message_id=update['message_id'])
		

		if text == "/test":
			if not uid in queue["occupied"]:
				lolt = ReplyKeyboardMarkup(keyboard=[
                    ['Plain text', KeyboardButton(text='Text only')],
					[dict(text='phone', request_contact=True), KeyboardButton(text='Location', request_location=True)]], resize_keyboard=True)
				bot.sendMessage(uid, "contoh", reply_markup=lolt)

		elif text == "Pengguna 👤":
			file = json.loads(open("app.json", "r").read())
			text = "Pengguna Online Saat Ini : " + str(len(file)) + " Online👤"
			bot.sendMessage(uid, text)

		elif text == "/user":
			if str(uid) in ADMIN :
				file = open("is.txt", "r")
				text = "Pengguna : " + str(len(file.readlines())) + " Online👤"
				bot.sendMessage(uid, text)
			else:
				bot.sendMessage(uid, "👮 Perintah ini hanya untuk admin")
		elif text == 'Info Profile 📌':
			if str(uid) in ADMIN :
				name = update["from"]["first_name"]
				_id = update["from"]["id"]
				username = update["from"]["username"]
				tipe = update["chat"]["type"]
				date1 = datetime.fromtimestamp(update["date"], tz=pytz.timezone("asia/jakarta")).strftime("%d/%m/%Y %H:%M:%S").split()
				text = "*Nama : " + str(name)+"*" +"\n"
				text += "*ID Kamu :* " +"`"+ str(_id) +"`"+"\n"
				text += f"*Username :* @{username}"+ "\n"
				text += "*Tipe Chat* : " +"_"+ str(tipe)+"_" +"\n"
				text += "*Tanggal :* " + str(date1[0]) +"\n"
				text += "*Waktu :* " + str(date1[1]) + " WIB" "\n"
				bot.sendMessage(uid, text, parse_mode='MarkDown', reply_to_message_id=update['message_id'])
			else:
				bahasa = update["from"]["language_code"]
				name = update["from"]["first_name"]
				_id = update["from"]["id"]
				bot.sendMessage(uid, f"Info Profile 📌\n\nNama = {name}\nID = `{_id}`\nBahasa = {bahasa}", parse_mode="MarkDown")

		elif text == 'Search 🔍' or text == "/search":
			if not uid in queue["occupied"]:
				keyboard = ReplyKeyboardRemove()
				bot.sendMessage(uid, '🔍  Waiting find your Partner, please don't go_',parse_mode='MarkDown', reply_markup=keyboard)
				print("[SB] " + str(uid) + " Bergabung ke obrolan")
				queue["free"].append(uid)

		elif text == '❌ Exit' or text == '/exit' and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan jodohnya ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍'],['Pengguna 👤','🛠 Menu Bot']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "❌ Meetings has done, find a new Partners /Search", parse_mode='MarkDown', reply_markup=keyboard)
			bot.sendMessage(queue["occupied"][uid], "😣 _Pasangan lu gasuka sama lu haha_", parse_mode='MarkDown', reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid]

		elif text == '🛠 Menu Bot':
			keyboard = ReplyKeyboardMarkup(keyboard=[
				['Info Profile 📌','📝 Info Covid-19'],['🔙 Main Menu']
			], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, f"👋🏻 Selamat datang lagi kamu\nYuk Join di Grup @{GROUP} dan Channel @{CHANNEL} Agar Mimin Bisa Update Bot Lebih Mantep Lagi 🥳", reply_markup=keyboard)

		elif text == '📝 Info Covid-19':
			web = requests.get('https://www.worldometers.info/coronavirus/country/indonesia/')
			tampilan = BeautifulSoup(web.content, 'html.parser')
			dataweb = tampilan.find_all("div", {"class": "maincounter-number"})
			ouy = "*KASUS VIRUS COVID-19 DI INDONESIA 🇮🇩*\n\n😷 Terpapar Virus : {} jiwa\n😵 Orang Meninggal : {} jiwa\n😇 Orang Sembuh : {} jiwa".format(dataweb[0].span.text,dataweb[1].span.text,dataweb[2].span.text)
			bot.sendMessage(uid, ouy, parse_mode='MarkDown')
			
		elif text == '🔙 Main Menu':
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍'],['Pengguna 👤','🛠 Menu Bot']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "_🔄 Kembali_", parse_mode='MarkDown', disable_web_page_preview=True, reply_markup=keyboard)
		elif text == "Next ▶️" or text == "/next" and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan obrolan dengan ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍', '🔙 Main Menu']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "_🛑 Your Partner has stoped, /search to find_",parse_mode="MarkDown")
			bot.sendMessage(queue["occupied"][uid], "_🛑 Your Partner has stoped, /search to find a new._",parse_mode="MarkDown", reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid] 
			if not uid in queue["occupied"]:
				key = ReplyKeyboardRemove()
				bot.sendMessage(uid, '🔍 Waiting for you partner, please don't go_',parse_mode="MarkDown" ,reply_markup=key)
				print("[SB] " + str(uid) + " Join ke obrolan") 
				queue["free"].append(uid)
		
		if text == "/nopics":
			config[str(uid)]["pics"] = not config[str(uid)]["pics"] 
			if config[str(uid)]["pics"]:
				bot.sendMessage(uid, "Pasangan Mengirim Foto")
			else:
				bot.sendMessage(uid, "Pasangan Tidak Bisa Mengirim Fhoto")
			saveConfig(config)

		if len(queue["free"]) > 1 and not uid in queue["occupied"]:
			partner = random.choice(exList(queue["free"], uid))
			if partner != uid:
				keyboard = ReplyKeyboardMarkup(keyboard=[
					['Next ▶️', '❌ Exit'],[dict(text='Send my phone', request_contact=True)]
				],resize_keyboard=True, one_time_keyboard=True)
				print('[SB] ' + str(uid) + ' Berjodoh dengan ' + str(partner))
				queue["free"].remove(partner)
				queue["occupied"][uid] = partner
				queue["occupied"][partner] = uid
				bot.sendMessage(uid, f'🎉 _Selamat Pasangan kamu telah ditemukan, jangan insecure ya..._\n\n⚠️ *PERINGATAN UNTUK ANDA* ⚠️\n_Jangan Chat Yang Membahas Tentang Porn, psikopat, LGBT, melecehkan, dan penghinaan agama, jika ada yang seperti itu , silahkan lapor mimin aja ya @{OWNER}_',parse_mode='MarkDown', reply_markup=keyboard)
				bot.sendMessage(partner, f'🎉 _Selamat Pasangan kamu telah ditemukann, jangan insecure ya..._\n\n⚠️ *PERINGATAN UNTUK ANDA* ⚠️\n_Jangan Chat Yang Membahas Tentang Porn, psikopat, LGBT, melecehkan, dan penghinaan agama, jika ada yang seperti itu , silahkan lapor mimin aja ya @{OWNER}_',parse_mode='MarkDown', reply_markup=keyboard)
	except 	Exception as e:
		print('[!] Error: ' + str(e))

if __name__ == '__main__':
	bot.message_loop(handle)

	while 1:
		time.sleep(3)
