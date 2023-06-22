from __future__ import unicode_literals
import yt_dlp as youtube_dl
import os
import random

# Creating all necessary Folders
dlDir = os.path.join(os.getcwd(), 'Downloads')
if not os.path.isdir(dlDir):
    os.makedirs(dlDir)
wrkDir = os.path.join(os.getcwd(), 'Working')
if not os.path.isdir(wrkDir):
    os.makedirs(wrkDir)
ulDir = os.path.join(os.getcwd(), 'Uploads')
if not os.path.isdir(ulDir):
    os.makedirs(ulDir)
imgDir = os.path.join(os.getcwd(), 'Images')
if not os.path.isdir(imgDir):
    os.makedirs(imgDir)

removeStr = ['[Official Music Video]', '(Official Music Video)', '[Official Video]', '(Official Video)',
             '[official music video]', '(official music video)', '[official video]', '(official video)',
             '(Lyrics)', '[Lyrics]', '[official lyric video]', '(official lyric video)', '(lyrics)', '[lyrics]',
             '[Official Lyric Video]', '(Official Lyric Video)', '(Lyrics Video)', '[Lyrics Video]', '(lyrics video)',
             '[lyrics video]']

run_qc = False
video = 'https://www.youtube.com/watch?v=8v_4O44sfjM'
type = "grl"


def yorn(prompt):
    x = input(prompt + ' (y/n) : ')
    if x == 'y' or x == 'Y':
        return True
    elif x == 'n' or x == 'N':
        return False
    else:
        yorn()


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'outtmpl': '/Downloads/%(title)s.%(ext)s',
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

# Downloading playlist
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    print("downloading: " + video)
    ydl.download([video])


# Song selection
if run_qc:
    print('presorting songs')
    songs = os.listdir(dlDir)
    for i in songs:
        title = "./Uploads/" + i.replace(".wav", "[Nightcore]")

        os.system('ffmpeg.exe -i "' + os.path.join('./Downloads/', i) + '" -filter:a '
            '"rubberband=pitch=1.15463094352953, rubberband=tempo=1.15" -crf 0 "' + os.path.join('./Working/', i) + '"')

        os.system('ffplay.exe "' + os.path.join('./Working', i) + '"')

        test = yorn('Does the song sound good? ')
        if test:
            print('yes')
            os.remove(os.path.join(wrkDir, i))
            os.rename(os.path.join(dlDir, i), os.path.join(wrkDir, i))
        elif not test:
            print('no')
            #os.remove(os.path.join(dlDir, i))
            os.remove(os.path.join(wrkDir, i))


# editing song 1
print('editing song 1')
if run_qc: songs = os.listdir(wrkDir)
else: songs = os.listdir(dlDir)
for i in songs:
    if run_qc:
        title = os.path.join(wrkDir, i)
    else:
        title = os.path.join(dlDir, i)
    newTitle = title
    for j in removeStr:
        newTitle = title.replace(j, '')

    if run_qc:
        print('ffmpeg.exe -i "' + title + '" -filter:a atempo=1.15, asetrate=44100*1.15, aresample=44100 "' + newTitle.replace('.wav', '[Nightcore].wav') + '"')
    else:
        os.system('ffmpeg.exe -i "' + title + '" -filter:a atempo=1.15,aresample=44100,asetrate=44100*1.15,aresample=44100 "' + newTitle.replace('.wav', '[Nightcore].wav') + '"')
        os.remove(os.path.join(dlDir, i))


# Video creation
while False:
    # Selecting Image
    igmTypeDir = os.path.join(imgDir, type)
    imgs = os.listdir(igmTypeDir)
    img = imgs[random.randint(0, len(imgs) - 1)]
    imgPth = os.path.join('./Images/', type, img)
    print("Using: " + imgPth)

    # Adding Background
    print("Adding background image to " + i)
    os.system('ffmpeg -loop 1 -i "' + imgPth + '" -i "' + title + '.wav" -shortest "' + newTitle + '.mp4"')

    print("removing original file")
    os.remove(title.replace('Uploads', 'Downloads').replace('[Nightcore]', '.wav'))

    # Removing Image from pool
    os.path.join(igmTypeDir, img)
    try:
        os.rename(imgPth, imgPth.replace('grl', 'u-grl'))
    except:
        try:
            os.rename(imgPth, imgPth.replace('boy', 'u-boy'))
        except:
            os.rename(imgPth, imgPth.replace('duo', 'u-duo'))


print("Finished!")
