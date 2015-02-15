import urllib
import requests
import json
base = 'http://streampocket.com/json2?stream='
fname = 'likelinks.txt'
chunk_size = 1024 * 1024
path = './likes/'

with open(fname) as f:
    content = f.readlines()

count = 0
for track in content:
    count += 1
    try:
        print "Track #%s"%(count)
        track = track.split('\r\n')[0]
        sound = urllib.quote_plus(track)
        print "Making first request"
        r = requests.get(base+sound)
        if r.status_code == 200:
            resp = json.loads(r.content)
            cdn = resp['recorded']
            filename = track.split('/')[-1]
            print "Name of track = %s"%(filename)
            print "Making second request"
            file_path = path+filename
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