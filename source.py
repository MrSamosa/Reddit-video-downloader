import random
from requests import get
import json
import time
import subprocess

UserAgents = """
Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.669.0 Safari/534.20
Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.19 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.19
Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.18 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.18
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0
Mozilla/5.0 (Macintosh; AMD Mac OS X 10_8_2) AppleWebKit/535.22 (KHTML, like Gecko) Chrome/18.6.872
Mozilla/5.0 (X11; CrOS i686 1660.57.0) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.46 Safari/535.19
Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19
"""

def user_agent():
	return random.choice(UserAgents.split('\n'))


url="https://www.reddit.com/r/Unexpected/comments/m0dmg9/huh/"
obj = get(url + '.json',headers = {'User-agent': user_agent()})
data = json.loads(obj.text)[0]['data']['children'][0]['data']
video_url = data['secure_media']['reddit_video']['fallback_url']

v = get(video_url).content
with open('video.mkv', 'wb') as file2:
    file2.write(v)
file2.close()

for c in reversed(video_url):
	if(c!='_'):
		video_url = video_url[:-1]
	else:
		break

audio_url = video_url + 'audio.mp4'
a = get(audio_url).content
with open('audio.wav', 'wb') as file1:
    file1.write(a)
file1.close()

cmd = 'ffmpeg -y -i audio.wav  -r 30 -i video.mkv  -filter:a aresample=async=1 -c:a flac -c:v copy final_video.mkv'
subprocess.call(cmd, shell=True)
print('Muxing Done')