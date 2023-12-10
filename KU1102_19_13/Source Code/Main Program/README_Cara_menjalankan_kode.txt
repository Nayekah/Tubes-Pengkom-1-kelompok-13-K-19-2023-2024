Cara menjalankan kode	:
1. Download file 'Tubes' dan 'musiclib.json', letakkan mereka berdua di satu folder yang sama
2. Buka folder yang berisi file 'Tubes' dan 'musiclib.json' di source code editor seperti contoh Visual Studio Code
3. Run file 'Tubes'
4. Selamat mencoba :D !

# REQUIREMENTS		:
- Visual Studio Code (VSC)
- Visual Studio (VS)
- Another IDE for python

# INSTALL PACKAGES	: (lakukan di terminal)
- pip3 install pafy
- pip3 install python-vlc
- pip3 install youtube-dl
- pip3 install youtube-search-python


# PENTING!!!
Jika tidak bisa menjalankan kode, ada 2 cara yang harus dilakukan.

A. Ganti file youtube
Step :
    1. pergi ke AppData (bisa diakses melalui windows + r, lalu ketik AppData dan ok / enter)
    2. pergi ke Local (folder) --> Programs (folder) --> Python (folder) --> Python 311 (folder) --> Lib (folder) --> site-packages (folder)
    3. cari folder bernama youtube_dl, lalu pergi ke folder bernama extractor
    4. Cari file bernama 'youtube' (berformat .py, scroll ke bawah), lalu ganti file tersebut dengan file bernama dan berformat sama '(youtube.py)' yang ada di folder 'Tubes Modules'

B. Ganti file backend_youtube_dl
Step :
    1. pergi ke AppData (bisa diakses melalui windows + r, lalu ketik AppData dan ok / enter)
    2. pergi ke Local (folder) --> Programs (folder) --> Python (folder) --> Python 311 (folder) --> Lib (folder) --> site-packages (folder)
    3. cari folder bernama pafy
    Cari file bernama 'backend_youtube_dl' (berformat .py), lalu ganti file tersebut dengan file bernama dan berformat sama '(backend_youtube_dl.py)' yang ada di folder 'Tubes Modules'

Tambahan	:
Pastikan Anda terhubung dengan internet