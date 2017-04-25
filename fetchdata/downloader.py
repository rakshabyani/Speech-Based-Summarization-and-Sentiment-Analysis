import os 

def download_subtitles(is_playlist, lang, url,path):
	query='youtube-dl '
	if is_playlist:
		query+='--yes-playlist '
	query+=	'--sub-lang '+str(lang)+' --write-sub --skip-download -o '+path+'/%\(title\)s.%\(ext\)s "' + url+'"'
	os.system(query)



def download_audio(is_playlist, url, path):	
	query='youtube-dl '
	if is_playlist:
		query+='--yes-playlist '
	query+=	'--extract-audio --audio-format mp3 -o '+path+'/%\(title\)s.%\(ext\)s "' + url+'"'
	os.system(query)

file = open('links.csv')
links= file.read().strip().split('\n')

if not os.path.exists('./outputs'):
		os.mkdir('./outputs')

for link in links:
	link=link.strip().split(' ')
	link=[x.strip() for x in link]
	dest_dir='./outputs/'+link[0]
	if not os.path.exists(dest_dir):
		os.mkdir(dest_dir)
	if "list" in link[1]:
		download_subtitles(True, 'de', link[1], dest_dir)
		download_audio(True, link[1],dest_dir)
	else:
		download_subtitles(False, 'de', link[1], dest_dir)
		download_audio(False, link[1],dest_dir)	



