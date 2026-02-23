import requests
from concurrent.futures import ThreadPoolExecutor

# ১. সার্ভার আইপি
base_url = "http://203.18.159.115/"

# ২. আপনার দেওয়া পারমানেন্ট লোগো লিঙ্কসহ ৬২টি চ্যানেলের ডাটা
CHANNELS_DATA = [
    ("COLORSHD", "Colors HD", "https://i.postimg.cc/pdj5yXrb/Colors-HD.png"),
    ("ZEETVHD", "Zee TV HD", "https://i.postimg.cc/tT2qPJYG/Zee-TV-HD-2025.png"),
    ("ZEECINEMAHD", "Zee Cinema HD", "https://i.postimg.cc/ZnsqknSy/1000102528.png"),
    ("SONYYAY", "Sony Yay", "https://i.ibb.co/77ByDrw/SONY-YAY.png"),
    ("SONYAAT", "Sony Aath", "https://i.ibb.co/W4Lh50kc/SONY-AATH-HD.png"),
    ("SONYPIXHD", "Sony Pix HD", "https://images.toffeelive.com/images/program/2419/logo/240x240/mobile_logo_287412001666784602.png"),
    ("SONYMAXHD", "Sony Max", "https://i.postimg.cc/qqbPBCgB/Sony-max-hd.png"),
    ("SONYBBCEARTHHD", "Sony BBC Earth HD", "https://i.postimg.cc/qRMtW9KH/images-(4).jpg"),
    ("DISCOVERYHD", "Discovery HD", "https://static.wikia.nocookie.net/logopedia/images/6/6a/Discovery_HD_2009.png"),
    ("ANIMALPLANETHD", "Animal Planet HD", "https://i.postimg.cc/6psvT4dX/Animal-Planet-HD-282018-n-v-29.png"),
    ("SOMOYTV", "Somoy TV", "https://i.ibb.co.com/fYCbByKT/SOMOY-TV-HD.png"),
    ("ATNBANGLA", "ATN Bangla", "https://i.ibb.co.com/9H65SwCG/ATN-BANGLA-HD.png"),
    ("STARGOLDHD", "Star Gold HD", "https://i.postimg.cc/GmvxR8Mm/Star-Gold-2020.png"),
    ("STARMOVIESHD", "Star Movies HD", "https://i.ibb.co/k2Bd3SgH/STAR-MOVIES-HD.png"),
    ("SONIC", "Sonic", "https://static.wikia.nocookie.net/logopedia/images/3/35/Nickelodeon_Sonic_logo_2019.png"),
    ("CARTOONNETWORK", "Cartoon Network HD", "https://static.wikia.nocookie.net/telelibrary/images/c/cb/Cartoon_Network_HD%2B_-_logo.png"),
    ("NICK", "Nick", "https://jiotvimages.cdn.jio.com/dare_images/images/channel/3dd2e26ab832cfe736739b86d57d21e9.png"),
    ("ZEECAFEHD", "Zee Cafe HD", "https://i.postimg.cc/k46VnWTv/Zee-Cafe-2025.png"),
    ("SUNBANGLAHD", "Sun Bangla HD", "https://static.wikia.nocookie.net/logopedia/images/2/20/Sun_Bangla_HD_logo_2023.png"),
    ("STARPLUSHD", "Star Plus HD", "https://i.postimg.cc/QxDjxvmJ/Star-Plus.png"),
    ("TSPORTS", "T Sports HD", "https://i.ibb.co.com/nNB5kRKY/T-Sports-HD.png"),
    ("STARBHARATHD", "Star Bharat HD", "https://i.postimg.cc/Kjkx3ywh/Star-Bharat-HD.png"),
    ("NATGEOWILDHD", "National Geo Wild HD", "https://upload.wikimedia.org/wikipedia/commons/3/3e/Nat_Geo_Wild_HD_logo.png"),
    ("STARMOVIESSELECTHD", "Star Movies Select HD", "https://i.ibb.co/k2Bd3SgH/STAR-MOVIES-HD.png"),
    ("HUNGAMA", "Hungama", "https://i.imgur.com/t0Ecro6.png"),
    ("STARSPORTS1HD", "Star Sports 1 HD", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Star_Sports_1_HD.png/1200px-Star_Sports_1_HD.png"),
    ("STARSPORTS2HD", "Star Sports 2 HD", "https://static.wikia.nocookie.net/logopedia/images/a/ac/Star_Sports_2.jpg"),
    ("SONYSPORTS2HD", "Sony Sports Ten 2 HD", "https://jiotvimages.cdn.jio.com/dare_images/images/Ten2_HD.png"),
    ("SONYSPORTS1HD", "Sony Sports Ten 1 HD", "https://jiotvimages.cdn.jio.com/dare_images/images/Ten_HD.png"),
    ("SONYSPORTS5HD", "Sony Sports Ten 5 HD", "https://i.postimg.cc/MTWsNKtv/7d0d368840908947f0e3bb344c29c53f.png"),
    ("ENTERR10", "Enter10 Bangla", "https://i.imgur.com/Tp3Kead.png"),
    ("POGO", "Pogo", "https://i.imgur.com/i5J3zrE.png"),
    ("NAGORIK", "Nagorik TV", "https://i.postimg.cc/hvn7pf00/Logo-of-Nagorik-TV.png"),
    ("DURANTATV", "Duronto TV", "https://i.imgur.com/PK9Gm5g.png"),
    ("CHANNEL24", "Channel 24", "https://i.imgur.com/MmhxR5E.png"),
    ("JAMUNATV", "Jamuna TV", "https://i.imgur.com/ds3aThu.jpg"),
    ("NICKJR", "Nick Jr", "https://i.imgur.com/chT8xP5.png"),
    ("SONYENTHD", "Sony Entertainment TV HD", "https://i.postimg.cc/GhjBKLV8/SETHD.png"),
    ("MOVIESNOWHD", "Movies Now HD", "https://imgur.com/BNaXQWX.png"),
    ("MNXHD", "MNX HD", "https://i.postimg.cc/4NTrQsRH/MNX-new-logo.png"),
    ("TLCHD", "TLC HD", "https://i.imgur.com/ELjuMyU.png"),
    ("STARJALSHAHD", "Star Jalsha HD", "https://i.imgur.com/9d1xXjN.png"),
    ("JALSHAMOVIESHD", "Jalsha Movies HD", "https://i.postimg.cc/3RQcFQdV/starjalshahd.png"),
    ("COLORSBANGLAHD", "Colors Bangla HD", "https://i.imgur.com/HVZHZGl.png"),
    ("COLORSBANGLACINEMA", "Colors Bangla Cinema", "https://static.wikia.nocookie.net/etv-gspn-bangla/images/7/7e/Colors_Bangla_Cinema_logo_%282024-present%29.png"),
    ("ZEEBANGLAHD", "Zee Bangla HD", "https://i.postimg.cc/RZvh8kK5/ja-ba-la-2025.png"),
    ("ZEEBANGLACINEMA", "Zee Bangla Cinema", "https://i.postimg.cc/GmP3xqfn/1000102537.png"),
    ("COLORSCINEPLEXHD", "Colors Cineplex HD", "http://jiotv.catchup.cdn.jio.com/dare_images/images/Color_Cineplex_HD.png"),
    ("NATGEOHD", "National Geographic HD", "https://i.postimg.cc/MKVttQbr/national-geographic-hd.png"),
    ("INDEPENDENTTV", "Independent TV", "https://i.imgur.com/kviJN1i.png"),
    ("MAASRANGAHD", "Maasranga HD", "https://i.postimg.cc/GmFLcvNB/Maasranga-Television-Logo.jpg"),
    ("ZING", "Zing", "https://i.postimg.cc/T18NYqJn/Zing-2025.png"),
    ("BALBHARAT", "Bal Bharat", "https://i.postimg.cc/VkM6JYwZ/ETV-Bal-Bharat-logo.png"),
    ("AXNHD", "AXN HD", "https://i.postimg.cc/FHcyh5nV/images-(8).png"),
    ("PTVSPORTSHD", "PTV Sports HD", "https://i.postimg.cc/nrb9LTSs/PTV-Sports.png"),
    ("ASPORTSHD", "A Sports HD", "https://i.postimg.cc/mZmGBhcR/unnamed.png"),
    ("STARSPORTS3", "Star Sports 3", "https://i.postimg.cc/tR8GYw54/sa-ta-ra-ka-ra-ka-ta.png"),
    ("STARSELECT1HD", "Star Sports Select 1 HD", "https://i.postimg.cc/1tFqGbLt/starselect-1.png"),
    ("STARGOLDSELECTHD", "Star Gold Select HD", "https://i.postimg.cc/9fr8hF7f/1000102566.png"),
    ("STARSPORTSSELECT2HD", "Star Sports Select 2 HD", "https://i.postimg.cc/QdD0HJWr/star-select-2.png"),
    ("HISTORYTVHD", "History TV HD", "https://i.postimg.cc/XJq5rpgc/History-tv18-hd.png"),
    ("BBCEARTHHD", "BBC Earth HD", "https://i.postimg.cc/YS1ndyc5/BBC-Earth-2023.png")
]

# ৩. মালিক যদি লিঙ্কের ফরম্যাট বদলায় (Deep Suffix Check)
POSSIBLE_SUFFIXES = [
    "/tracks-v1a1/mono.m3u8", 
    "/mono.m3u8", 
    "/index.m3u8", 
    "/playlist.m3u8"
]

def scan_logic(ch, session, results):
    ch_id, display_name, logo_url = ch
    # মালিক বড় বা ছোট হাতের নাম বদলালে এটি ধরবে
    id_variants = [ch_id.upper(), ch_id.lower()]
    
    for variant in id_variants:
        for sfx in POSSIBLE_SUFFIXES:
            url = f"{base_url}{variant}{sfx}"
            try:
                # নিজেকে অরিজিনাল প্লেয়ার হিসেবে পরিচয় দেওয়া যাতে ব্লক না করে
                headers = {'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12'}
                r = session.head(url, headers=headers, timeout=2.5, allow_redirects=True)
                
                if r.status_code == 200:
                    results.append((display_name, url, logo_url))
                    print(f"✅ Found: {display_name}")
                    return # সচল লিঙ্ক পাওয়া গেলে পরের ভ্যারিয়েন্টে যাবে না
            except:
                continue

def main():
    session = requests.Session()
    found_channels = []

    print("🔍 Deep Scanning starting with Permanent Logos...")

    # ১৫ জন 'শিকারী' একসাথে খুঁজবে যাতে দ্রুত শেষ হয়
    with ThreadPoolExecutor(max_workers=15) as executor:
        for ch in CHANNELS_DATA:
            executor.submit(scan_logic, ch, session, found_channels)

    # সিরিয়াল ঠিক রেখে ফাইল সেভ করা
    with open("only_new_channels.m3u", "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for original in CHANNELS_DATA:
            for item in found_channels:
                if item[0] == original[1]:
                    f.write(f'#EXTINF:-1 tvg-logo="{item[2]}" group-title="Asim_Dipto BDIX",{item[0]}\n{item[1]}\n\n')
    
    print(f"✨ Update Complete. Total {len(found_channels)} channels found.")

if __name__ == "__main__":
    main()
