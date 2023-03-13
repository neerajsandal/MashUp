from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import os
import sys


def download_files(x, n):
    html = urllib.request.urlopen(
        'https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    for i in range(n):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i])
        print("Downloading Songs "+str(i+1)+" .......")
        mp4files = yt.streams.filter(only_audio=True).first().download(
            filename='Music-'+str(i)+'.mp3')

    print("All Songs Are downloaded")
    print("Creating MashUp.....")


def merging(n, y):
    if os.path.isfile("Music-0.mp3"):
        try:
            fin_sound = AudioSegment.from_file("Music-0.mp3")[0:y*1000]
        except:
            fin_sound = AudioSegment.from_file(
                "Music-0.mp3", format="mp4")[0:y*1000]
    for i in range(1, n):
        aud_file = str(os.getcwd()) + "/Music-"+str(i)+".mp3"
        try:
            f = AudioSegment.from_file(aud_file)
            fin_sound = fin_sound.append(f[0:y*1000], crossfade=1000)
        except:
            f = AudioSegment.from_file(aud_file, format="mp4")
            fin_sound = fin_sound.append(f[0:y*1000], crossfade=1000)

    return fin_sound


def main():
    if len(sys.argv) == 5:
        x = sys.argv[1]
        x = x.replace(' ', '') + "Music"
        try:
            n = int(sys.argv[2])
            y = int(sys.argv[3])
        except:
            sys.exit("Parameters are Not Correct")
        output_name = sys.argv[4]
    else:
        sys.exit(
            'Arguments must be 4 (Singer_Name, No._Songs, Audio_Filename, Mashup.mp3 )')

    download_files(x, n)
    fin_sound = merging(n, y)
    fin_sound.export(output_name, format="mp3")
    print("MashUp Created, Let's play it")


if __name__ == '__main__':
    main()
