"""
\\================================================================ Tugas Besar Kelompok 13 ======================================================================//
\\======================================================================== K-19 =================================================================================//
"""

"""
Anggota Kelompok    :
1. Dimas Anggiat/16523052
2. Julian Benedict/16523178
3. Nayaka Ghana Subrata/19623031
4. Karol Yangqian Poetracahya/19623206
"""

# Program pemutar musik online
# Program akan menerima input dari user dan juga mengolah sesuai dengan perintah yang ada di interface


#KAMUS :


#ALGORITMA
#Import library
import os
import re 
import vlc
import pafy
import time
import threading
from youtubesearchpython import VideosSearch

# Set-up the import
os.environ["VLC_VERBOSE"] = str("-1")
Instance = vlc.Instance('--no-xlib -q > /dev/null 2>&1')
Instance.log_unset()
player = Instance.media_player_new()
clear = "\n" * 100

# Membuat sistem array untuk membuat Library dan PlayList
Playlistfile = "musicLibrary.txt"
library = []
PlayList_kini = []
Musik_kini = False
Now_playing = ""


# Proses
# Membuat class untuk Lagu
class Lagu():
    def __init__(self, lNama, lGrup, lTahun, lGenre, lPlayList, lLink):
        self.NamaLagu = lNama
        self.GrupLagu = lGrup
        self.TahunLagu = lTahun
        self.GenreLagu = lGenre
        self.PlayListLagu = lPlayList
        self.LinkLagu = lLink

    def printSelf(self):
        print(f"{self.NamaLagu} - {self.GrupLagu} - {str(self.TahunLagu)}")


# Membuat fungsi dalam pemutaran musik
def playSong(url):
    global Musik_kini
    Musik_kini = True
    url = url
    video = pafy.new(url)
    best = video.getbestaudio()
    playurl = best.url

    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()


# Membuat fungsi dalam mencari musik
def cariMusik(query):
    results = VideosSearch(query, limit = 1)
    return results.result()['result'][0]


# Membuat fungsi pemutaran musik yang dipilih
def putarMusikPilihan(LaguList):
    global Now_playing
    while True:
        pilih = input("Apakah Anda ingin memutar musik? (Y/N) ")
        if pilih.upper() == "Y":
            index = int(input("Masukkan indeks musik --> "))
            Now_playing = LaguList[index - 1].NamaLagu
            playSong(LaguList[index - 1].LinkLagu)
            break
        elif pilih.upper() == "N":
            break


def searchOutput():
    searchString = input("Masukkan musik yang ingin Anda cari --> ")
    res = searchLibrary(searchString)
    c = 1
    for t in res:
        print(c, end=" ")
        print(t.NamaLagu + " " + t.GrupLagu + " " + t.GenreLagu)
        c += 1
    return res


def validasiInput(pilih, min, max):
    return min <= pilih <= max


def validasiInputString(pilih):
    return bool(re.match(r"[\s\w]+$", pilih))


def tambahkeFile(data):
    library.append(data)


def searchLibrary(searchString):
    found = []
    for i in library:
        if searchString in i.NamaLagu or searchString in i.GenreLagu:
            found.append(i)
    return found


def gelPlayLists():
    playL = []
    for g in library:
        if not g.PlayListLagu in playL:
            playL.append(g.PlayListLagu)
    return playL

def tambahKePlaylist():
    global library, PlayList_kini

    print("Pilih lagu yang ingin ditambahkan ke dalam playlist:")
    res = searchOutput()

    index = int(input("Masukkan indeks lagu yang ingin ditambahkan ke playlist --> "))
    while not validasiInput(index, 1, len(res)):
        index = int(input("Masukkan indeks lagu yang ingin ditambahkan ke playlist --> "))

    lagu = res[index - 1]
    playlist_name = input("Masukkan nama playlist --> ")
    lagu_baru = Lagu(lagu.NamaLagu, lagu.GrupLagu, lagu.TahunLagu, lagu.GenreLagu, playlist_name, lagu.LinkLagu)

    tambahkeFile(lagu_baru)
    
    print(f"Lagu {lagu.NamaLagu} ditambahkan ke dalam playlist {playlist_name}")
    PlayList_kini.append(playlist_name)


def putarPlayList(playlislNama):
    play = []
    for g in library:
        if playlislNama.upper() == g.PlayListLagu.upper():
            play.append(g)

    for link in play:
        playSong(link.LinkLagu)
        print("Now Playing ... " + link.NamaLagu + " " + link.GrupLagu + " " + link.PlayListLagu)
        print(r"""
       _________
     _|_________|_               
    /             \             
   | ###       ### |            
   | ###       ### |
    \_____________/  
        """)
        time.sleep(1.5)
        durasi = player.get_length() / 1000
        time.sleep(durasi)
        while True:
            if "State.Ended" in str(player.get_state()):
                print("Next Track")
                break
            continue



# Membuat animasi loading
def loadanimasi():
    animasi = [
        "[        ]",
        "[=       ]",
        "[==      ]",
        "[===     ]",
        "[====    ]",
        "[=====   ]",
        "[======  ]",
        "[======= ]",
        "[========]",
        "[ =======]",
        "[  ======]",
        "[   =====]",
        "[    ====]",
        "[     ===]",
        "[      ==]",
        "[       =]",
        "[        ]",
        "[        ]"
    ]

    Tidak_selesai = True
    i = 0

    while Tidak_selesai:
        print(animasi[i % len(animasi)], end='\r')
        time.sleep(.1)
        i += 1
        if i > 17:
            Tidak_selesai = False





# Membuat interface utama
def menu():
    global Musik_kini, Now_playing
    print(r"""                                                                                        
                        
 __    __     __  __     ______     __     ______   __  __    
/\ "-./  \   /\ \/\ \   /\  ___\   /\ \   /\  == \ /\ \_\ \   
\ \ \-./\ \  \ \ \_\ \  \ \___  \  \ \ \  \ \  _-/ \ \____ \  
 \ \_\ \ \_\  \ \_____\  \/\_____\  \ \_\  \ \_\    \/\_____\ 
  \/_/  \/_/   \/_____/   \/_____/   \/_/   \/_/     \/_____/ 

                                        
    versi 0.0.1 - Kelompok 13
    """)

    print("""
     1) Tambahkan ke library
     2) Tunjukkan library
     3) Cari lagu
     4) Cari berdasarkan genre
     5) Hapus lagu
     6) Tambah ke playlist
     7) Mainkan PlayList
     8) Mainkan sebuah lagu
     9)
    10) Keluar

    """)

    if Musik_kini:
        print("Now playing....  " + Now_playing)
        print(r"""
       _________
     _|_________|_              11 -pause
    /             \             12 -stop
   | |||       ||| |            22 -play
   | ---       --- |
    \_____________/  
        """)

    opsi = int(input(" -->"))
    while not validasiInput(opsi, 1, 23):
        opsi = int(input(" -->"))


# Membuat algoritma utama dari music player

# Sistem opsi 1
    if opsi == 1:
        title = input("Masukkan title lagu ")
        while not validasiInputString(title):
            title = input("Masukkan title lagu ")
        kreator = input("Masukkan nama kreator ")
        while not validasiInputString(kreator):
            kreator = input("Masukkan nama kreator ")
        genre = input("Masukkan genre lagu ")
        while not validasiInputString(genre):
            genre = input("Masukkan genre lagu ")
        tahun = int(input("Masukkan tahun terbit lagu "))
        while not validasiInput(tahun, 1500, 3000):
            tahun = int(input("Masukkan tahun terbit lagu "))
        PlayList = input("Masukkan nama PlayList ")
        while not validasiInputString(PlayList):
            PlayList = input("Masukkan nama PlayList ")

        Musik = Lagu(cariMusik(title)["title"], kreator, tahun, genre, PlayList, cariMusik(title)["link"])
        Musik.printSelf()
        tambahkeFile(Musik)

# Sistem opsi 2
    elif opsi == 2:
        print("Ini adalah library Anda")
        print("------------------------------------------------------------------")
        print()
        c = 1
        for i in library:
            print(c, end=" ")
            i.printSelf()
            c += 1
        print()
        print()
        print("------------------------------------------------------------------")

        putarMusikPilihan(library)

# Sistem opsi 3
    elif opsi == 3:
        res = searchOutput()
        putarMusikPilihan(res)

    elif opsi == 4:
        print()
    elif opsi == 5:
        res = searchOutput()
        index = int(input("Masukkan indeks lagu yang ingin dihapus --> "))
        while not validasiInput(index, 0, len(res) + 1):
            index = int(input("Masukkan indeks lagu yang ingin dihapus --> "))
            if index == 0:
                break
        fullLib = library
        print(fullLib.pop(index - 1))
        print()
        print(fullLib)

        print("Menghapus...")
    elif opsi == 6:
         tambahKePlaylist()
    elif opsi == 7:
        pl = gelPlayLists()
        print()
        c = 1
        for p in pl:
            print(str(c) + ") ", end=" ")
            print(p)
            c += 1

        while True:
            pilih = input("Apakah Anda ingin memutar PlayList? (Y/N) ")
            if pilih.upper() == "Y":
                index = int(input("Pilih PlayList --> "))
                print(pl[index - 1])
                putarPlayList(pl[index - 1])
                break
            elif pilih.upper() == "N":
                break
    elif opsi == 8:
        query = input("Masukkan lagu yang ingin diputar ==>")
        Now_playing = cariMusik(query)['title']
        player.stop()
        playSong(cariMusik(query)['link'])
    elif opsi == 9:
        print(player.get_state())
        print(type(player.get_state()))
        print(str(player.get_state()))

    elif opsi == 11:
        player.pause()
    elif opsi == 22:
        player.play()
    elif opsi == 12:
        player.stop()
        Musik_kini = False
    elif opsi == 10:
        exit()


def main():
    while True:
        print(clear)
        menu()
        Tr = threading.Thread(target=loadanimasi())
        Tr.start()

if __name__ == "__main__":
    main()