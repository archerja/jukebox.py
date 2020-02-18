#!/usr/bin/python

# Copyright (c) 2018, Joseph Archer

# Import the os module, for the os.walk function
import os
import sys
from mutagen.mp3 import MP3

USE_EXT = ('mp3')
style = ''
path = ''
numcols = 4
cover_file = 'folder.jpg'

jclassic = os.path.join(os.getcwd(),'Jukebox_classic.html')
jmodern = os.path.join(os.getcwd(),'Jukebox_modern.html')
jvarious = os.path.join(os.getcwd(),'Jukebox_various.html')

version = '0.0.4'

class ID3:
    def __init__(self,path):
        self._load(path)

    def _load(self, filename):
        tags = MP3(filename)
        comments = []
        for key in tags:
            if key[0:4] == 'COMM':
                if(tags[key].desc == ''):
                    comments.append(tags[key].text[0])
        comments.append('')
        self.album = tags.get('TALB', [''])[0]
        self.artist = tags.get('TPE1', [''])[0]
        self.duration = "%u:%.2d" % (tags.info.length / 60, tags.info.length % 60)
        self.length = tags.info.length
        self.bitrate = tags.info.bitrate / 1000
        self.year = str(tags.get('TDRC', [''])[0])
        self.title = tags.get('TIT2', [''])[0]
        self.comment = comments[0]
        self.genre = tags.get('TCON', [''])[0]
        self.track = tags.get('TRCK', [''])[0]

def build(path):
        titleslist = []
        errors = []
        for root, dir, files in os.walk(path):
            for name in files:
                if name[-4:].lower() == '.mp3':
                    path = os.path.join(root,name)
                    location = path.split(path)[1]
                    print(".")
                    try:
                        id3 = ID3(path)
                    except:
                        errors.append(path)
                        id3 = None
                    if id3 != None:
                        if style == 'classic':
                            titleslist.append((id3.artist,id3.title,id3.track,id3.album,id3.genre,id3.bitrate,id3.year,id3.comment,id3.duration,root,path,location))
                        elif style == 'modern':
                            titleslist.append((id3.artist,id3.year,id3.album,id3.comment,id3.track,id3.title,id3.genre,id3.bitrate,id3.duration,root,path,location))
                        # various
                        else:
                            titleslist.append((id3.album,id3.comment,id3.track,id3.artist,id3.title,id3.genre,id3.bitrate,id3.duration,root,path,location))
        print("")
        if len(errors) > 0:
            print("")
            print("---- Errors ----")
            print("")
            for error in errors:
                print(error)
        titleslist.sort()
#	print titleslist
        return titleslist


def makeVarious(path):
    pagedata = ''
    thelist = build(path)
    pagedata = '<table border=1 >\n'
    i = thelist
    prev = 0
    now = 0
    for n in range(0,len(i)):
      if n == now:
        next = n
        pagedata = pagedata + '<tr>\n'
        col = 0
        for r in range(1,numcols):
          if next == len(i):
            pagedata = pagedata + '</td>\n'
            break
          while i[prev][2] == i[next][2]:			# while albums match
            if col == numcols:
              break
            col = col + 1
            pagedata = pagedata + '<td valign="top" width="300">\n'
            pagedata = pagedata + '<b>' + i[prev][0] + '</b>\n'
            pagedata = pagedata + '<hr>\n'
            pagedata = pagedata + i[prev][1] + '\n'
            pagedata = pagedata + '<hr>\n'
            img = i[prev][8] + '/' + cover_file
            pagedata = pagedata + '<img src="' + img + '" width = "300"></br>\n'
            while i[prev][1] == i[next][1]:			# while albums match
              pagedata = pagedata + '(' + i[now][2] + ') ' + i[now][3] + ' - ' + '</br><a href="' + i[now][9] + '" target="_blank">'  + i[now][4] + '</a></br>\n'
              now = now + 1
              next = next + 1
              if next == len(i):
                break
            if next == len(i):
              break
            prev = next
            pagedata = pagedata + '</td>\n'
        pagedata = pagedata + '</tr>\n'
    pagedata = pagedata + '</table>\n'
    return pagedata


def makeModern(path):
    pagedata = ''
    thelist = build(path)
    pagedata = '<table border=1 >\n'
    i = thelist
    prev = 0
    now = 0
    for n in range(0,len(i)):
      if n == now:
        next = n
        pagedata = pagedata + '<tr>\n'
        col = 0
        for r in range(1,numcols):
          if next == len(i):
            pagedata = pagedata + '</td>\n'
            break
          while i[prev][2] == i[next][2]:			# while albums match
            if col == numcols:
              break
            col = col + 1
            pagedata = pagedata + '<td valign="top" width="300">\n'
            pagedata = pagedata + '<b>' + i[prev][0] + '</b>\n'
            pagedata = pagedata + '<hr>\n'
            pagedata = pagedata + i[prev][2] + ' (' + i[prev][1] + ')\n'
            pagedata = pagedata + '<hr>\n'
            img = i[prev][9] + '/' + cover_file
            pagedata = pagedata + '<img src="' + img + '" width = "300"></br>\n'
            if i[prev][3] == i[next][3]:
              pagedata = pagedata + i[now][3] + '</br>\n'
              curcom = i[now][3]
            while i[prev][2] == i[next][2]:			# while albums match
              if curcom != i[next][3]:
                pagedata = pagedata + i[now][3] + '</br>\n'
                curcom = i[next][3]
              pagedata = pagedata + '<a href="' + i[now][10] + '" target="_blank">' + i[now][4] + ' - ' + i[now][5] + '</a></br>\n'
              now = now + 1
              next = next + 1
              if next == len(i):
                break
            if next == len(i):
              break
            prev = next
            pagedata = pagedata + '</td>\n'
        pagedata = pagedata + '</tr>\n'
    pagedata = pagedata + '</table>\n'
    return pagedata


def makeClassic(path):
    pagedata = ''
    thelist = build(path)
    n = 0
    i = thelist
    pagedata = '<table border=1 >\n'
    for n in range(0,len(i),numcols * 2) :
      pagedata = pagedata + '<tr>\n'
      for r in range(0,numcols * 2, 2):
        toptitle = n + r
        topartist = toptitle
        bottitle = n + r + 1
        if toptitle == (len(i)):
          break
        pagedata = pagedata + '<td align=center width="300" height="110" background="redlabel.jpg">\n'
        pagedata = pagedata + '<a href="' + i[toptitle][10] + '" target="_blank">' + i[toptitle][1] + '</a>\n'
        botartist = bottitle
        if botartist == (len(i)):
          pagedata = pagedata + '</br></br>' + i[toptitle][0] + '</br></br> \n'
          pagedata = pagedata + '</br></td>\n'
          break
        if i[topartist][0] == i[botartist][0]:
          pagedata = pagedata + '</br></br>' + i[toptitle][0] + '</br></br> \n'
        else:
          pagedata = pagedata + '</br></br>' + i[toptitle][0] + '/' + i[botartist][0] + '</br></br> \n'
        if bottitle == (len(i)):
          pagedata = pagedata + '</br></td>\n'
          break
        pagedata = pagedata + '<a href="' + i[bottitle][10] + '" target="_blank">' + i[bottitle][1] + '</a>\n'
        pagedata = pagedata + '</td>\n'
      pagedata = pagedata + '</tr>\n'
    pagedata = pagedata + '</table>\n'
    return pagedata


def makepage(path,style):
    if style == 'classic':
      fileName = jclassic
      pagetable = makeClassic(path)
    elif style == 'modern':
      fileName = jmodern
      pagetable = makeModern(path)
    else:
      fileName = jvarious
      pagetable = makeVarious(path)
    print("")
    print("Creating web page '%s'" % fileName)
    f = open(fileName, "w")
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<title>Jukebox</title>\n')
    f.write('</head>\n')
    f.write('<body background="background.jpg">\n')
    f.write('<h1>Jukebox</h1>\n')
#    print pagetable
    f.write(pagetable)
    f.write('<font size="-1">version ' + version +' &copy; 2018. <A HREF="https://github.com/archerja/jukebox.py" target="_blank">Jukebox on github</A></font>\n')
    f.write('</body>\n')
    f.write('</html>\n')
    f.close()

def help():
    print('')
    print(sys.argv[0], ', version ', version)
    print('')
    print('Usage: ', sys.argv[0], ' [PATH] [TYPE] [OPTION]')
    print('')
    print('                    PATH     [path to your mp3 folder]')
    print('')
    print('                    TYPE     [classic|modern|various]')
    print('                                (choose 1 of 3 styles)')
    print('                                classic = original jukebox, good for multiple artists')
    print('                                modern  = CD jukebox, good for single artist')
    print('                                various = CD jukebox, good for multiple artists')
    print('')
    print('                    OPTION   [number of columns]')
    print('                                (optional: defaults to 4)')
    print('')
    exit

if __name__ == '__main__':

    if len(sys.argv) < 2:
       print('Usage: jukebox.py [PATH] [TYPE] [OPTION]')
       print("Try 'jukebox.py --help' for more information.")
    else:
       if sys.argv[1:]:
          path = sys.argv[1]
       if sys.argv[2:]:
          style = sys.argv[2]
       if sys.argv[3:]:
          numcols = int(sys.argv[3])
       if path == '--help':
          help()
       else:	  	  
          print("directory to scan is: ", path)
          makepage(path,style)

