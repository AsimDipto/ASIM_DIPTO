import requests
from concurrent.futures import ThreadPoolExecutor

# ১. সার্ভার এবং লোগো পাথ
base_url = "http://203.18.159.115/"
# এখানে 'AsimDipto' এবং 'ASIM_DIPTO' আপনার গিটহাব ইউজারনেম ও রিপোজিটরি অনুযায়ী ঠিক আছে কি না দেখে নিন
logo_base = "https://raw.githubusercontent.com/AsimDipto/ASIM_DIPTO/main/logos/"

# ২. সব ৬২টি চ্যানেলের লিস্ট (আইডি, নাম, লোগো ফাইল)
CHANNELS_DATA = [
    ("COLORSHD", "Colors HD", "colors.png"),
    ("ZEETVHD", "Zee TV HD", "zeetv.png"),
    ("ZEECINEMAHD", "Zee Cinema HD", "zeecinema.png"),
    ("SONYYAY", "Sony Yay", "sonyyay.png"),
    ("SONYAAT", "Sony Aath", "sonyaath.png"),
    ("SONYPIXHD", "Sony Pix HD", "sonypix.png"),
    ("SONYMAXHD", "Sony Max", "sonymax.png"),
    ("SONYBBCEARTHHD", "Sony BBC Earth HD", "sonybbcearth.png"),
    ("DISCOVERYHD", "Discovery HD", "discovery.png"),
    ("ANIMALPLANETHD", "Animal Planet HD", "animalplanet.png"),
    ("SOMOYTV", "Somoy TV", "somoy.png"),
    ("ATNBANGLA", "ATN Bangla", "atnbangla.png"),
    ("STARGOLDHD", "Star Gold HD", "stargold.png"),
    ("STARMOVIESHD", "Star Movies HD", "starmovies.png"),
    ("SONIC", "Sonic", "sonic.png"),
    ("CARTOONNETWORK", "Cartoon Network HD", "cn.png"),
    ("NICK", "Nick", "nick.png"),
    ("ZEECAFEHD", "Zee Cafe HD", "zeecafe.png"),
    ("SUNBANGLAHD", "Sun Bangla HD", "sunbangla.png"),
    ("STARPLUSHD", "Star Plus HD", "starplus.png"),
    ("TSPORTS", "T Sports HD", "tsports.png"),
    ("STARBHARATHD", "Star Bharat HD", "starbharat.png"),
    ("NATGEOWILDHD", "National Geo Wild HD", "natgeowild.png"),
    ("STARMOVIESSELECTHD", "Star Movies Select HD", "starmoviesselect.png"),
    ("HUNGAMA", "Hungama", "hungama.png"),
    ("STARSPORTS1HD", "Star Sports 1 HD", "starsports1.png"),
    ("STARSPORTS2HD", "Star Sports 2 HD", "starsports2.png"),
    ("SONYSPORTS2HD", "Sony Sports Ten 2 HD", "sonysports2.png"),
    ("SONYSPORTS1HD", "Sony Sports Ten 1 HD", "sonysports1.png"),
    ("SONYSPORTS5HD", "Sony Sports Ten 5 HD", "sonysports5.png"),
    ("ENTERR10", "Enter10 Bangla", "enter10.png"),
    ("POGO", "Pogo", "pogo.png"),
    ("NAGORIK", "Nagorik TV", "nagorik.png"),
    ("DURANTATV", "Duronto TV", "duronto.png"),
    ("CHANNEL24", "Channel 24", "channel24.png"),
    ("JAMUNATV", "Jamuna TV", "jamuna.png"),
    ("NICKJR", "Nick Jr", "nickjr.png"),
    ("SONYENTHD", "Sony Entertainment TV HD", "sonyent.png"),
    ("MOVIESNOWHD", "Movies Now HD", "moviesnow.png"),
    ("MNXHD", "MNX HD", "mnx.png"),
    ("TLCHD", "TLC HD", "tlc.png"),
    ("STARJALSHAHD", "Star Jalsha HD", "starjalsha.png"),
    ("JALSHAMOVIESHD", "Jalsha Movies HD", "jalshamovies.png"),
    ("COLORSBANGLAHD", "Colors Bangla HD", "colorsbangla.png"),
    ("COLORSBANGLACINEMA", "Colors Bangla Cinema", "colorsbanglacinema.png"),
    ("ZEEBANGLAHD", "Zee Bangla HD", "zeebangla.png"),
    ("ZEEBANGLACINEMA", "Zee Bangla Cinema", "zeebanglacinema.png"),
    ("COLORSCINEPLEXHD", "Colors Cineplex HD", "colorscineplex.png"),
    ("NATGEOHD", "National Geographic HD", "natgeo.png"),
    ("INDEPENDENTTV", "Independent TV", "independent.png"),
    ("MAASRANGAHD", "Maasranga HD", "maasranga.png"),
    ("ZING", "Zing", "zing.png"),
    ("BALBHARAT", "Bal Bharat", "balbharat.png"),
    ("AXNHD", "AXN HD", "axn.png"),
    ("PTVSPORTSHD", "PTV Sports HD", "ptvsports.png"),
    ("ASPORTSHD", "A Sports HD", "asports.png"),
    ("STARSPORTS3", "Star Sports 3", "starsports3.png"),
    ("STARSELECT1HD", "Star Sports Select 1 HD", "starsportsselect1.png"),
    ("STARGOLDSELECTHD", "Star Gold Select HD", "stargoldselect.png"),
    ("STARSPORTSSELECT2HD", "Star Sports Select 2 HD", "starsportsselect2.png"),
    ("HISTORYTVHD", "History TV HD", "history.png"),
    ("BBCEARTHHD", "BBC Earth HD", "bbcearth.png")
]

# ৩. মালিকের ট্রিকস ধরার সাফিক্স লিস্ট
POSSIBLE_SUFFIXES = [
    "/tracks-v1a1/mono.m3u8", 
    "/mono.m3u8", 
    "/index.m3u8", 
    "/playlist.m3u8"
]

def scan_logic(ch, session, results):
    ch_id, display_name, logo_file = ch
    id_variants = [ch_id.upper(), ch_id.lower(), ch_id.capitalize()]
    
    for variant in id_variants:
        for sfx in POSSIBLE_SUFFIXES:
            url = f"{base_url}{variant}{sfx}"
            try:
                headers = {'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12'}
                r = session.head(url, headers=headers, timeout=2.0)
                if r.status_code == 200:
                    full_logo = f"{logo_base}{logo_file}"
                    results.append((display_name, url, full_logo))
                    return
            except: continue

def main():
    session = requests.Session()
    found_channels = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        for ch in CHANNELS_DATA:
            executor.submit(scan_logic, ch, session, found_channels)

    with open("only_new_channels.m3u", "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for original in CHANNELS_DATA:
            for item in found_channels:
                if item[0] == original[1]:
                    f.write(f'#EXTINF:-1 tvg-logo="{item[2]}" group-title="ASIM_BDIX",{item[0]}\n{item[1]}\n\n')

if __name__ == "__main__":
    main()
