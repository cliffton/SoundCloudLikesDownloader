from bs4 import BeautifulSoup
import requests
import os
import urllib
import requests
import json
base = 'http://streampocket.com/json2?stream='
fname = 'likelinks.txt'
chunk_size = 1024 * 1024
path = './likes/'

file_open = open('likes.html','r') 
# r = requests.get('http://localhost:8000/likes.html')
# html_doc = r.content
html_doc = file_open.read()
# import pdb; pdb.set_trace()
soup = BeautifulSoup(html_doc)

# for track in soup.find_all(itemprop='url'):
	# print (track.get('href'))
count = 0
to_download = []
for track in soup.find_all('li'):
	count += 1
	if count > 9:
		# import pdb; pdb.set_trace()
		for lis in track.find_all('a'):
			link = lis.get('href')
			if len(link.split('/')) > 4:
				# print link
				to_download.append(link)
count = 0
for song in to_download:
	try:
		open('./likes/'+song.split('/')[-1]+'.mp3','r')
		
		# os.renames('./likes/'+song.split('/')[-1],'./likes/'+song.split('/')[-1]+'.mp3')
	except Exception, e:
		try:
			open('./likes/'+song.split('/')[-1],'r')
		except Exception, e:
			print song
			count += 1
			try:
				# import pdb; pdb.set_trace()
				print "Track #%s"%(count)
				# song = song.split('\r\n')[0]
				sound = urllib.quote_plus(song)
				print "Making first request"
				r = requests.get(base+sound)
				if r.status_code == 200:
					resp = json.loads(r.content)
					cdn = resp['recorded']
					filename = song.split('/')[-1]
					print "Name of track = %s"%(filename)
					print "Making second request"
					file_path = path+filename+'.mp3'
					r = requests.get(cdn)
					if r.status_code == 200:
						with open(file_path, 'wb') as fd:
							for chunk in r.iter_content(chunk_size):
								fd.write(chunk)
					else:
						print "Error 2:- Track #%s Failed !"%(count)    
				else:
					print "Error 1:- Track #%s Failed !"%(count)
			except Exception, e:
				print "Error"
		pass

