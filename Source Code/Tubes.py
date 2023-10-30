"""
\\===================================================== Tugas Besar Pengenalan Komputasi Kelompok 13 =====================================================================//
\\============================================================== Online Music Player "Musipy" ============================================================================//
\\======================================================================== K-19 ==========================================================================================//
"""

"""
Anggota Kelompok    :
1. Dimas Anggiat (16523052)
2. Julian Benedict (16523178)
3. Nayaka Ghana Subrata (19623031)
4. Karol Yangqian Poetracahya (19623206)
"""

# Program pemutar musik online (online music player)
# Program akan menerima input dari user dan juga mengolah sesuai dengan perintah yang ada di interface


# ------------------------------------------------------------------------- PENTING!!! ------------------------------------------------------------------------------------------------------------------------------------------

""" README sederhana (Hanya sebagian, jangan lupa untuk membaca 'README.txt') """
# INSTALL REQUIREMENTS  : (lakukan di terminal)
# pip3 install pafy
# pip3 install python-vlc
# pip3 install youtube-dl
# pip3 install youtube-search-python

""" Pastikan Anda terhubung dengan internet """


# -------------------------------------------------------------------------- KAMUS -------------------------------------------------------------------------------------------------------------------------------------

# library, PlayList_kini : list of string
# Musik_kini : boolean
# Now_playing : string

# Terlampir di setiap def (fungsi)


# ------------------------------------------------------------------------- ALGORITMA ---------------------------------------------------------------------------------------------------------------------------------

# Import libraries and modules
import os; import re ; import vlc
import json; import pafy; import time
import threading; from youtubesearchpython import VideosSearch


# Membuat sistem array untuk membuat Library dan PlayList
FILENAME = "musiclib.json"
library = []
PlayList_kini = []
Musik_kini = False
Now_playing = ""


# Set-up the vlc
os.environ["VLC_VERBOSE"] = str("-1")
Instance = vlc.Instance('--no-xlib -q > /dev/null 2>&1')
Instance.log_unset()
player = Instance.media_player_new()
clear = "\n" * 100


# Membuat class untuk Lagu (inisiasi awal dan fondasi dasar program)
class Lagu():
    # Deklarasi init
    def __init__(self, lNama, lGrup, lTahun, lGenre, lPlayList, lLink):
        # Fungsi membuat sebuah self dari library

        # KAMUS LOKAL
        # lNama, Lgrup, lGenre, lPlayList, lLink : string
        # NamaLagu, GrupLagu, GenreLagu, PlayListLagu, LinkLagu : string
        # lTahun, TahunLagu : integer

        # ALGORITMA
        self.NamaLagu = lNama
        self.GrupLagu = lGrup
        self.TahunLagu = lTahun
        self.GenreLagu = lGenre
        self.PlayListLagu = lPlayList
        self.LinkLagu = lLink


    # Deklarasi fungsi untuk print 'self'
    def printSelf(self):
        # Fungsi untuk print 'self'

        # KAMUS LOKAL
        # NamaLagu, GrupLagu, TahunLagu : string

        # ALGORITMA
        print(f"{self.NamaLagu} - {self.GrupLagu} - {str(self.TahunLagu)}")


    # Deklarasi fungsi untuk membuat format JSON
    def FormatJson(self):
        # Fungsi untuk mengubah input ke format JSON

        # KAMUS LOKAL
        # NamaLagu, GrupLagu, TahunLagu, GenreLagu, PlayListLagu, LinkLagu : string

        # ALGORITMA
        return{
            "NamaLagu": self.NamaLagu,
            "GrupLagu": self.GrupLagu,
            "TahunLagu": self.TahunLagu,
            "GenreLagu": self.GenreLagu,
            "PlayListLagu": self.PlayListLagu,
            "LinkLagu": self.LinkLagu
        }
    


# ----------------------------------------------------------------------- Function Declaration ----------------------------------------------------------------------------------------------------------------------------------


# Deklarasi fungsi dalam pemutaran musik
def playSong(url):
    # Fungsi akan berperan dalam memutar lagu

    # KAMUS LOKAL
    # Musik_kini : boolean

    # ALGORITMA
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


# Deklarasi fungsi dalam mencari musik
def cariMusik(query):
    # Fungsi akan mencari musik

    # KAMUS LOKAL
    # limit : integer

    # ALGORITMA
    results = VideosSearch(query, limit = 1)
    return results.result()['result'][0]


# Deklarasi fungsi dalam memutar musik yang dipilih
def putarMusikPilihan(ListLagu):
    # Fungsi akan memutar lagu yang dipilih

    # KAMUS LOKAL
    # pilih : char
    # Now_playing, NamaLagu, LinkLagu: string
    # index : integer
    # ListLagu : list

    # ALGORITMA
    global Now_playing
    while True:
        pilih = input("Apakah Anda ingin memutar musik? (Y/N) ")
        if pilih.upper() == "Y":
            index = int(input("Masukkan indeks musik --> "))
            Now_playing = ListLagu[index - 1].NamaLagu
            playSong(ListLagu[index - 1].LinkLagu)
            break
        elif pilih.upper() == "N":
            break


# Deklarasi fungsi dalam pencarian data
def searchOutput():
    # Fungsi akan mencari suatu data

    # KAMUS LOKAL
    # seacrhString, NamaLagu, GrupLagu, GenreLagu : string
    # c : integer

    # ALGORITMA
    searchString = input("Masukkan musik yang ingin Anda cari --> ").title()
    res = searchLibrary(searchString)
    if not res:
        print("Tidak ada lagu yang ditemukan.")
        return []
    
    c = 1
    for l in res:
        print(c, end=" ")
        print(l.NamaLagu + " " + l.GrupLagu + " " + l.GenreLagu)
        c += 1
    return res


# Deklarasi fungsi untuk mengecek validasi input
def validasiInput(pilih, min, max):
    # Fungsi mengecek apakah input valid

    # KAMUS LOKAL
    # pilih : integer

    # ALGORITMA
    if (pilih in range (min,max)):
        return True
    else:
        return False


# Deklarasi fungsi untuk mengecek validasi input dari suatu string
def validasiInputString(pilih):
    # Fungsi mengecek apakah Input suatu string valid
    
    # KAMUS LOKAL
    # pilih : string

    # ALGORITMA
    if (re.match(r"[\s\w]+$",pilih)):
        return True
    else:
        return False


# Deklarasi fungsi untuk menambah data ke format json
def tambahkeFile(data):
    # Fungsi menambah suatu input ke format JSON

    # KAMUS LOKAL
    # library : list
    # Lagu, NamaLagu, GrupLagu, TahunLagu, GenreLagu, PlayListLagu, LinkLagu, data : string
    # indent : integer

    # ALGORITMA
    with open('musiclib.json',"r") as openfile:
        json_obj= json.load(openfile)
        
    json_obj.append(data)
    with open("musiclib.json","w") as outfile:
       json.dump(json_obj,outfile,indent=4)
    
    library.append(Lagu(data["NamaLagu"], data["GrupLagu"], data["TahunLagu"], data["GenreLagu"], data["PlayListLagu"],
                        data["LinkLagu"]))


# Deklarasi fungsi untuk membaca file json
def bacaFile():
    # Fungsi membaca file berformat JSON
    # KAMUS LOKAL
    # l, Lagu, NamaLagu, GrupLagu, TahunLagu, GenreLagu, PlayListLagu, LinkLagu, data : string
    # library : list

    # ALGORITMA
    with open('musiclib.json', "r") as openfile:
        json_obj = json.load(openfile)
    
    for l in json_obj:
        library.append(Lagu(l["NamaLagu"],l["GrupLagu"],l["TahunLagu"],l["GenreLagu"],l["PlayListLagu"],l["LinkLagu"]))
    return json_obj


# Deklarasi fungsi untuk mencari lagu di library
def searchLibrary(searchString):
    # Fungsi mencari lagu yang ada di library

    # KAMUS LOKAL
    # library, found : list
    # i, searchString, NamaLagu, GenreLagu : string

    # ALGORITMA
    if len(library) <= 0:
        bacaFile()

    found = []
    for i in library:
        if searchString in i.NamaLagu or searchString in i.GenreLagu:
            found.append(i)
    return found


# Deklarasi fungsi untuk mencari lagu berdasarkan genre
def searchByGenre(genre):
    # Fungsi akan mencari lagu berdasarkan genre yang di search

    # KAMUS LOKAL
    # results,library : list
    # song, genre, GenreLagu, result : string
    # c : integer

    # ALGORITMA
    results = []
    for song in library:
        if genre.title() in song.GenreLagu.title():
            results.append(song)
    if len(results) > 0:
        print("Hasil pencarian berdasarkan genre:")
        c = 1
        for result in results:
            print(c, end=" ")
            result.printSelf()
            c += 1
        putarMusikPilihan(results)
    else:
        print("Tidak ada lagu dengan genre tersebut.")


# Deklarasi fungsi untuk mendapatkan data playlist
def getPlayLists():
    # Fungsi akan mendapatkan dan mengambil playlist

    # KAMUS LOKAL
    # playL, library : list
    # g, PlayListLagu : string

    # ALGORITMA
    playL = []
    for g in library:
        if not g.PlayListLagu in playL:
            playL.append(g.PlayListLagu)
    return playL


# Deklarasi fungsi untuk mencari playlist
def searchInPlaylist(playlist):
    # Fungsi akan mencari playlist

    # KAMUS LOKAL
    # results, library : list
    # song, playlist, PlayListLagu : string
    # c : integer

    # ALGORITMA
    results = []
    for song in library:
        if playlist.title() == song.PlayListLagu.title():
            results.append(song)
    if len(results) > 0:
        print(f"Hasil pencarian di playlist {playlist}:")
        c = 1
        for result in results:
            print(c, end=" ")
            result.printSelf()
            c += 1
        putarMusikPilihan(results)
    else:
        print(f"Tidak ada lagu dalam playlist {playlist}.")


# Deklarasi fungsi untuk menghapus lagu dari library / playlist
def hapusLagu():
    # Fungsi akan menghapus lagu yang ada di library / playlist

    # KAMUS LOKAL
    # index : integer
    # library : list

    # ALGORITMA
    res = searchOutput()

    if not res:
        print("Library kosong. Tidak ada lagu yang bisa dihapus.")
        return

    try:
        index = int(input("Masukkan indeks lagu yang ingin dihapus (0 untuk membatalkan): "))
        while not validasiInput(index, 0, len(res) + 1):
            index = int(input("Masukkan indeks lagu yang ingin dihapus (0 untuk membatalkan): "))

        if index != 0 and index <= len(res):
            deleted_song = res[index - 1]
            library.remove(deleted_song)
            print(f"Lagu berhasil dihapus: {deleted_song.NamaLagu}")

            # Update the musiclib.json file
            with open("musiclib.json", "w") as outfile:
                json.dump([song.FormatJson() for song in library], outfile, indent=4)

            print("Lagu berhasil dihapus.")
        else:
            print("Indeks tidak valid. Tidak ada lagu yang dihapus.")
    except ValueError:
        print("Input tidak valid. Masukkan angka sebagai indeks.")


# Deklarasi fungsi untuk memutar playlist
def putarPlayList(NamaPlaylist):
    # Fungsi akan memutar playlist yang tersedia / dipilih

    # KAMUS LOKAL
    # play, library : list
    # g, NamaPlaylist, PlayListLagu, link, LinkLagu, NamaLagu, GrupLagu : string
    # durasi : float

    # ALGORITMA
    play = []
    for g in library:
        if NamaPlaylist.upper() == g.PlayListLagu.upper():
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


# Deklarasi fungsi untuk memutar lagu selanjutnya
def nextSong():
    # Fungsi akan memutar lagu selanjutnya

    # KAMUS LOKAL
    # Now_plaaying, lagu, NamaLagu, LinkLagu : string
    # library : list
    # index, i : integer

    # ALGORITMA
    global Now_playing, library, player
    if Now_playing:
        index = next((i for i, lagu in enumerate(library) if lagu.NamaLagu == Now_playing), None)
        if index is not None:
            if index + 1 < len(library):
                Now_playing = library[index + 1].NamaLagu
                playSong(library[index + 1].LinkLagu)
            else:
                # Jika lagu berada di akhir indeks, putar lagu indeks awal
                Now_playing = library[0].NamaLagu
                playSong(library[0].LinkLagu)


# Deklarasi fungsi untuk memutar lagu sebelumnya
def previousSong():
    # Fungsi akan memutar lagu sebelumnya

    # KAMUS LOKAL
    # Now_playing, lagu, NamaLagu, LinkLagu : string
    # library : list
    # index, i : integer

    # ALGORITMA
    global Now_playing, library, player
    if Now_playing:
        index = next((i for i, lagu in enumerate(library) if lagu.NamaLagu == Now_playing), None)
        if index is not None:
            if index - 1 >= 0:
                Now_playing = library[index - 1].NamaLagu
                playSong(library[index - 1].LinkLagu)
            else:
                # Jika lagu berada di awal indeks, putar lagu indeks terakhir
                Now_playing = library[-1].NamaLagu
                playSong(library[-1].LinkLagu)


# Deklarasi fungsi untuk memberikan delay pada print
def print_bertahap(teks, delay=1):
    # Fungsi membuat perintah 'print' dengan delay tertentu

    # KAMUS LOKAL
    # karakter, teks : string
    # flush : boolean
    # delay : integer

    # ALGORITMA
    for karakter in teks:
        print(karakter, end='', flush=True)
        time.sleep(delay)


# Deklarasi fungsi dalam membuat animasi loading
def loadanimasi():
    # Fungsi membuat animasi loading

    # KAMUS LOKAL
    # animasi : list
    # Tidak_selesai : boolean
    # i : integer

    # ALGORITMA
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


# ---------------------------------------------------------------------------- Main menu ----------------------------------------------------------------------------------------------------------------------

# Deklarasi fungsi dalam membuat interface utama
def menu():
    # Fungsi membuat interface display

    # KAMUS LOKAL
    # Musik_kini : boolean
    # opsi, tahun, c, i, index, delay : integer
    # Now_playing, judul, kreator, genre, PlayList, playlist, query : string
    # library : list
    # pilih : char

    # ALGORITMA
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
     1) Tambahkan ke library / playlist
     2) Tunjukkan library / playlist
     3) Cari lagu di library / playlist
     4) Cari berdasarkan genre
     5) Hapus lagu
     6) Cari Playlist
     7) Mainkan PlayList
     8) Mainkan langsung
     9) Tentang Program dan FAQ
    10) Keluar

    """)


    if Musik_kini:
        print(f"Now playing....  {Now_playing} " )
        print(r"""
       _________
     _|_________|_              11 -play        14 -next
    /             \             12 -pause       15 - previous
   | |||       ||| |            13 -stop
   | ---       --- |            
    \_____________/             
        """)



    opsi = int(input(" -->"))
    while not validasiInput(opsi, 1, 16):
        opsi = int(input(" -->"))



# ------------------------------------------------------------- Membuat algoritma utama dari music player --------------------------------------------------------------------------

# Menambahkan sebuah lagu ke library / playlist (opsi 1)
    if opsi == 1:
        judul = input("Masukkan judul lagu: ").title()
        while not validasiInputString(judul):
            judul = input("Masukkan judul lagu: ").title()
        kreator = input("Masukkan nama kreator: ").title()
        while not validasiInputString(kreator):
            kreator = input("Masukkan nama kreator: ").title()
        genre = input("Masukkan genre lagu: ").title()
        while not validasiInputString(genre):
            genre = input("Masukkan genre lagu: ").title()
        tahun = int(input("Masukkan tahun terbit lagu: "))
        while not validasiInput(tahun, 1500, 3000):
            tahun = int(input("Masukkan tahun terbit lagu: "))
        PlayList = input("Masukkan nama PlayList: ").title()
        while not validasiInputString(PlayList):
            PlayList = input("Masukkan nama PlayList: ").title()

        print_bertahap("Menambahkan", delay = 0); time.sleep(0)
        print_bertahap("."); time.sleep(0.05)
        print_bertahap("."); time.sleep(0.05)
        print_bertahap("."); time.sleep(0.05)
        Musik = Lagu(cariMusik(judul)["title"], kreator, tahun, genre, PlayList, cariMusik(judul)["link"])
        Musik.printSelf()
        tambahkeFile(Musik.FormatJson())


# Menunjukkan library / playlist (opsi 2)
    elif opsi == 2:
        print_bertahap("Ini adalah library Anda\n", delay = 0.05); time.sleep(0.5) 
        print_bertahap("-------------------------------------------------------------------------------------------------------------------------------", delay = 0.000001); time.sleep(0.5)
        print()
        if len(library) <= 0:
            bacaFile()
        c = 1
        for i in library:
            print(c,end=" "); time.sleep(1)
            i.printSelf()
            c += 1
        print()
        print()
        print_bertahap("-------------------------------------------------------------------------------------------------------------------------------\n", delay = 0.000001); time.sleep(0.5)

        putarMusikPilihan(library)


# Mencari lagu di library / playlist (opsi 3)
    elif opsi == 3:
        res = searchOutput()
        if res:
            putarMusikPilihan(res)
        else:
            print("Tidak ada lagu yang ditemukan.")


# Mencari lagu berdasarkan genre (opsi 4)
    elif opsi == 4:
        genre = input("Masukkan genre lagu yang ingin dicari: ")
        searchByGenre(genre)


# Menghapus lagu dari library / playlist (opsi 5)
    elif opsi == 5:
        hapusLagu()


# Mencari playlist (opsi 6)
    elif opsi == 6:
        playlist = input("Masukkan nama playlist yang ingin dicari: ")
        searchInPlaylist(playlist)


# Memainkan sebuah playlist (opsi 7)
    elif opsi == 7:
        pl = getPlayLists()
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


# Memainkan lagu secara langsung dengan algoritma 'search'
    elif opsi == 8:
        query = input("Masukkan lagu yang ingin diputar ==>")
        Now_playing = cariMusik(query)['title']
        player.stop()
        playSong(cariMusik(query)['link'])


# Tentang program dan FAQ
    elif opsi == 9:
        time.sleep(1)
        print_bertahap(r""""
                                                                                                                                                                                                                                                                                                                                                                                      
                                                        
                                                                                
                        :              .--+++=-=++=*=-.                       : 
                             :=++=+++++=:           .-+*=:                      
                         .=++-.                        ..-===-.                 
       : =:  :         -*+.        .    :.                   .==+=  .           
        :##--        -%*::         .:.:=.                      :::*#=.          
       :*-.*:      .**-             ..+.                        :.. :#=         
      .#+. ++-    +#:      :.      :. -::                     :: =+=. -#:       
        :+*:    -#-      ::          ..                           :#%=: *+      
         -*    *+       +.                                          +*=+=*#     
              #-       =.                          :       =.        =# .+%.  . 
            .%-       +.=             .            ##-    . =:        +*      = 
  :         %+  +=   -. -   :         %-        .  *%**-:.  :=.        %-   ::- 
:::.       -% :@#   .=......-        :@#       .-:.-@%#%-  =#:*        -# .-::=.
  .        =+*=%-       -   -    #   **%+       .: =@##*%+  @#==       *@   .:= 
           .+ .@        .   -   #@  +%*+%*.       --@%*%@@%=@@@%..    -:@.    : 
        ::    -*-   =       = :%#=.*%#:.-##. ..    -@%@@@@#%#@@@##    * =*      
        ..    -*+  .+       -#%+@++:   :-=*@+:@*+=::=#@+%*#+..=%*:   +:  :*-    
       ::   ::=@.   #       .%=   .:  ----. .=+: ..:*@: -%+*%.:*=  -*=     -+=. 
         : - .#.    #    .:::-# .+#%@@@@*+=:        =@*:+#**%: #-.-+## .     .+%
         : -=%:.    -+:......=*@@@@@@#*#+++*:       :%*-:..+@.:%-+#-.@-.#=+++++:
       :. -#=-    :+#%+:..:.+##-*@%+. .:=.        .  -*==-+#=.%#%* :+@* * .-    
        =*=     -*%##%@*:...=#=#*%@+==+.-.. .:     .=. .:-::-+-=*%+%%%#*+ .=    
       -#+==*+%%#####%@:*+:.*= @#-:* .-*:=....:---::  ..--::::-#@%%%%%%%-       
              @*####@#%#-:=##  =%@=*   * .:.       :   .:--=*%@%%%%%%%%%-     : 
              @####@#@*%@%+##   #%@#.  -#....      -  :=*#%@%#%%%%%%%####     = 
:.      ::--==%###%@#%%%%%%#*   -+**#**+##++=+++*##%@@%@%###%%%#@%%##%#%%+::.::.
    +++####*+++=--::..  :                   ...:-=+###########%%= =*%%%%%%#.  - 
       ::==+****@%@**####***=   -**####%%#%@**#%%#%#---%%%%%%%%%+     ...     = 
                .=+. +%%%%*#%   *@@@@@%%@*%%%+=-+%%+*=#*=%=+*%#%%+            . 
                     ++=:  :%+ .#--@*=+#=%%%#:::*%#- =====*.  +%%@              
                            +% +%##+-=+:-=@@+:::=-+. -*+%%+    .@#              
       .:. .:.              .%+%%+*+=: :: =-.  -#%# :-@%*#+   :-..::            
         . :                 -%%*.:=+=*+==:=   :.:+=##%####     ::              
        :: ::                 -%+-=*=-==-:-*##=+###*#*#+*#@-  .:..::            
       .     :                  .:-=+===##=:+#-+=+%=-:        .     .           
                                       :*:::#-#-::*-                            
                                       =====   -+=*-                            
                        .                        :=.                          . 
                                                                                                                                                                                                                                                      
                                                                                                                                                                
        """, delay = 0.000000000001)
        time.sleep(0.5)
        print_bertahap("\nHaloooooo!!! ", delay =0.05)

        time.sleep(0.5)
        print_bertahap("Aku Musi, ", delay = 0.05); time.sleep(0.5); print_bertahap("dan kali ini aku mau menjelaskan tentang program ini!\n\n" , delay = 0.05)
        time.sleep(0.5)
      
        print_bertahap("\nPertama, ", delay = 0.05); time.sleep(0.5); print_bertahap(r"""program ini merupakan hasil dari sebuah tugas besar mata kuliah pengenalan komputasi tahun 2023 / 2024, """, delay = 0.05); time.sleep(0.5); 
        print_bertahap("\nprogram ini dibuat menggunakan python dan dengan bantuan modul serta JSON.\n\n", delay = 0.05)
        
        time.sleep(1)
        print_bertahap("\nKedua, ", delay = 0.05); time.sleep(0.5); print_bertahap("jangan lupa membaca 'Readme.txt' file yang tertera yaa, ", delay = 0.05); time.sleep(0.5)
        print_bertahap("agar membantu dalam menjalankan program ini >_<\n\n", delay = 0.05); time.sleep(0.5)
              
        print_bertahap("\nFAQ     :", delay= 0.05); time.sleep(0.5)

        print_bertahap("\n1. Spill kelompoknya dong!", delay = 0.05); time.sleep(0.5)
        print_bertahap("\n--> Oke, berikut ini daftar nama kelompok 13 : ", delay = 0.05); time.sleep(0.5)
        print_bertahap("\n1. Dimas Anggiat (16523052)", delay = 0.05); time.sleep(0.5)
        print_bertahap("\n2. Julian Benedict (16523178)", delay = 0.05); time.sleep(0.5)
        print_bertahap("\n3. Nayaka Ghana Subrata (19623031)", delay = 0.05); time.sleep(0.5)
        print_bertahap("\n4. Karol Yangqian Poetracahya (19623206)\n\n", delay = 0.05); time.sleep(0.5)
        
        print_bertahap("\n2. Berapa lama program ini dibuat ?", delay = 0.05); time.sleep(0.5)
        print_bertahap("\n--> Program ini kurang lebih dibuat selama 3 minggu\n\n", delay = 0.05); time.sleep(0.5)
        
        print_bertahap("\n3. Hal terberat apa yang dialami dalam membuat program ini ?", delay = 0.05); time.sleep(0.5)
        print_bertahap("\n--> Pastinya debugging dong! Hehe.... (Nayaka)\n\n", delay = 0.05); time.sleep(0.5)
        
              
        print_bertahap("\nFootnote        : ", delay = 0.05); time.sleep(0.5)
        print_bertahap("\nTerima kasih sudah ingin mencoba program ini, ", delay = 0.05); time.sleep(0.5) 
        print_bertahap("salam hangat untuk Pak Fadhil! :D \n\n", delay = 0.05); time.sleep(2)

        print_bertahap("\nKembali ke halaman utama", delay = 0.05); time.sleep(0.5)
        print_bertahap(".", delay = 1); time.sleep(1.5)
        print_bertahap(".", delay = 1); time.sleep(1.5)
        print_bertahap(".", delay = 1); time.sleep(1.5)
        

# --------------------------------------------------------------------------- Input button --------------------------------------------------------------------------------------------------

# Memutar musik (opsi 11)
    elif opsi == 11:
        player.play()

# Menjeda musik (opsi 12)
    elif opsi == 12:
        player.pause()

# Stop pemutaran musik (opsi 13)
    elif opsi == 13:
        player.stop()
        Musik_kini = False

# Skip lagu ke depan (opsi 14)
    elif opsi == 14:
        nextSong()

# Skip lagu ke belakang (opsi 15)
    elif opsi == 15:
        previousSong()

# Exit Program (opsi 10)
    elif opsi == 10:
        exit()


# -------------------------------------------------------------------------- Interface ------------------------------------------------------------------------------------------------------

# Deklarasi fungsi untuk mengatur sistem
def main():
    # Fungsi untuk mengatur sistem

    # ALGORITMA
    bacaFile() # Menampilkan file history ke interface
    while True:
        print(clear)
        menu()
        Thr = threading.Thread(target=loadanimasi())
        Thr.start()


if __name__ == "__main__":
    main()


"""
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                            Akhir dari Program
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
