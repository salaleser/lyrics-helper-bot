import telebot
import lyricsgenius
from musixmatch import Musixmatch

cfg_file = open('config', 'r', newline='\n')
telegram_token, genius_token, musixmatch_token = cfg_file.readlines()
cfg_file.close()

bot = telebot.TeleBot(telegram_token.split('\n')[0])
genius = lyricsgenius.Genius(genius_token.split('\n')[0])
musixmatch = Musixmatch(musixmatch_token.split('\n')[0])

@bot.message_handler(content_types=['text'])
def start(message):
	if message.text == '/start':
		bot.send_message(message.from_user.id,
		'Введите имя исполнителя и наименование песни в формате {artist_name}-{song_title}')
	else:
		get_lyrics_from_genius(message)
		# get_lyrics_from_musixmatch(message)

def get_lyrics_from_musixmatch(message):
	try:
		args = message.text
		arg1, arg2 = args.split('-')

		song_json = musixmatch.matcher_lyrics_get(arg2, arg1)

		# status_code = song_json['message']['header']['status_code']
		# if (status_code != 200):
		# 	bot.send_message(message.from_user.id, 'Не найдено в Musixmatch!\nПытаюсь найти в Genius...')
		# 	get_lyrics_from_genius(message)
		# 	return
		
		lyrics = song_json['message']['body']['lyrics']['lyrics_body']
		bot.send_message(message.from_user.id, 'Текст песни "'+arg1+' — '+arg2+'":\n'+lyrics)
	except BaseException as e:
		bot.send_message(message.from_user.id, 'Error!\n'+repr(e))

def get_lyrics_from_genius(message):
	try:
		args = message.text
		arg1, arg2 = args.split('-')

		# artist = genius.search_artist(arg1, max_songs=1, sort="title")
		song = genius.search_song(arg2, arg1)
		bot.send_message(message.from_user.id, 'Текст песни "'+song.artist+' — '+song.title+'":\n'+song.lyrics)
	except BaseException as e:
		bot.send_message(message.from_user.id, 'Error!\n'+repr(e))

bot.polling(none_stop=True, interval=0)
