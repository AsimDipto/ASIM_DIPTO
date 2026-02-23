import requests
from concurrent.futures import ThreadPoolExecutor

# ১. মূল আইপি ঠিক থাকলে চ্যানেল হারাবে না
base_url = "http://203.18.159.115/"
# লোগো ফোল্ডারের পাথ
logo_base = "https://raw.githubusercontent.com/AsimDipto/ASIM_DIPTO/main/logos/"

# আপনার সিরিয়াল অনুযায়ী ডাটা
CHANNELS_DATA = [
    ("COLORSHD", "Colors HD", "colorshd.png"),
    ("ZEETVHD", "Zee TV HD", "zeetvhd.png"),
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
    ("NATGEOWILDHD", "National Geo Wild HD", "natgeowild.png")
    # এভাবে বাকি সব চ্যানেলের আইডি ও ছবির নাম যোগ করবেন
]

# মালিক যদি লিঙ্কের শেষ অংশ বদলায়, এই লিস্ট সেটা খুঁজে বের করবে
POSSIBLE_SUFFIXES = [
    "/tracks-v1a1/mono.m3u8", 
    "/mono.m3u8", 
    "/index.m3u8", 
    "/playlist.m3u8",
    "/chunks.m3u8",
    "/video.m3u8"
]

def deep_scan(ch, session, found_list):
    ch_id, ch_name, logo_file = ch
    
    # মালিক বড় বা ছোট হাতের নাম বদলালে এটি ধরবে
    id_variants = [ch_id.upper(), ch_id.lower(), ch_id.capitalize()]
    
    for variant in id_variants:
        for sfx in POSSIBLE_SUFFIXES:
            test_url = f"{base_url}{variant}{sfx}"
            try:
                # User-Agent যোগ করা হয়েছে যাতে সার্ভার ব্লক না করে
                headers = {'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12'}
                r = session.head(test_url, headers=headers, timeout=2.0, allow_redirects=True)
                
                if r.status_code == 200:
                    full_logo = f"{logo_base}{logo_file}"
                    found_list.append((ch_name, test_url, full_logo))
                    print(f"✅ FOUND: {ch_name} (at {variant}{sfx})")
                    return # সচল লিঙ্ক পাওয়া গেলে লুপ বন্ধ হবে
            except:
                continue

def main():
    session = requests.Session()
    found_channels = []

    print("🔍 Deep Scanning starting... Please wait.")

    # ১০ জন একসাথে কাজ করবে যাতে দ্রুত হয়
    with ThreadPoolExecutor(max_workers=10) as executor:
        for ch in CHANNELS_DATA:
            executor.submit(deep_scan, ch, session, found_channels)

    # সিরিয়াল ঠিক রেখে সেভ করা
    with open("only_new_channels.m3u", "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for original in CHANNELS_DATA:
            for item in found_channels:
                if item[0] == original[1]:
                    f.write(f'#EXTINF:-1 tvg-logo="{item[2]}" group-title="Asim_BDIX",{item[0]}\n{item[1]}\n\n')

if __name__ == "__main__":
    main()
