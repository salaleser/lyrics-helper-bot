import telebot
import lyricsgenius

cfg_file = open('config', 'r')
telegram_token, genius_token = cfg_file.readlines()
cfg_file.close()

genius = lyricsgenius.Genius(genius_token)
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(content_types=['text'])
def start(message):
	if message.text == '/start':
		bot.send_message(message.from_user.id, 'Введите название трека')
	else:
		get_lyrics(message)

def get_lyrics(message):
	args = message.text
	arg1, arg2 = args.split('-')

	# artist = genius.search_artist(arg1, max_songs=1, sort="title")
	song = genius.search_song(arg2, arg1)
	bot.send_message(message.from_user.id, 'Текст песни "'+song.artist+' — '+song.title+'":\n'+song.lyrics)

bot.polling(none_stop=True, interval=0)
