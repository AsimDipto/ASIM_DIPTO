import requests
from concurrent.futures import ThreadPoolExecutor

# বেস ইউআরএল
base_url = "http://203.18.159.115/"

# আপনার দেওয়া সেই ৬২টি চ্যানেলের আইডি লিস্ট
CHANNELS = [
    "COLORSHD", "ZEETVHD", "ZEECINEMAHD", "SONYYAY", "SONYAAT", "SONYPIXHD", 
    "SONYMAXHD", "SONYBBCEARTHHD", "DISCOVERYHD", "ANIMALPLANETHD", "SOMOYTV", 
    "ATNBANGLA", "STARGOLDHD", "STARMOVIESHD", "SONIC", "CARTOONNETWORK", 
    "NICK", "ZEECAFEHD", "SUNBANGLAHD", "STARPLUSHD", "TSPORTS", "STARBHARATHD", 
    "NATGEOWILDHD", "STARMOVIESSELECTHD", "HUNGAMA", "STARSPORTS1HD", "STARSPORTS2HD", 
    "SONYSPORTS2HD", "SONYSPORTS1HD", "SONYSPORTS5HD", "ENTERR10", "POGO", 
    "NAGORIK", "DURANTATV", "CHANNEL24", "JAMUNATV", "NICKJR", "SONYENTHD", 
    "MOVIESNOWHD", "MNXHD", "TLCHD", "STARJALSHAHD", "JALSHAMOVIESHD", 
    "COLORSBANGLAHD", "COLORSBANGLACINEMA", "ZEEBANGLAHD", "ZEEBANGLACINEMA", 
    "COLORSCINEPLEXHD", "NATGEOHD", "INDEPENDENTTV", "MAASRANGAHD", "ZING", 
    "BALBHARAT", "AXNHD", "PTVSPORTSHD", "ASPORTSHD", "STARSPORTS3", 
    "STARSELECT1HD", "STARGOLDSELECTHD", "STARSPORTSSELECT2HD", "HISTORYTVHD", "BBCEARTHHD"
]

# মালিক যদি পাথ বা এক্সটেনশন চেঞ্জ করে, এই ৫টি ফরম্যাট চেক হবে
SUFFIXES = [
    "/tracks-v1a1/mono.m3u8",
    "/mono.m3u8",
    "/index.m3u8",
    "/chunks.m3u8",
    "/video.m3u8"
]

def check_channel(ch_id, session, found):
    # বড় হাত এবং ছোট হাত দুইভাবেই ট্রাই করবে (মালিকের ট্রিকস ধরার জন্য)
    variations = [ch_id.upper(), ch_id.lower()]
    
    for v in variations:
        for sfx in SUFFIXES:
            url = f"{base_url}{v}{sfx}"
            try:
                # ১.৫ সেকেন্ডের মধ্যে চেক করবে সচল কি না
                r = session.head(url, timeout=1.5, allow_redirects=True)
                if r.status_code == 200:
                    found.append((ch_id, url))
                    print(f"CRACKED: {v}{sfx}")
                    return # একটা পাওয়া গেলে ওই চ্যানেলের জন্য আর চেক করবে না
            except:
                pass

def main():
    found_channels = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'VLC/3.0.12'})

    print(f"Deep Scanning Started for {len(CHANNELS)} channels...")

    # একসাথে ১০টি করে রিকোয়েস্ট পাঠাবে (Speed & Safety)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for ch in CHANNELS:
            executor.submit(check_channel, ch, session, found_channels)

    # প্লেলিস্ট ফাইল তৈরি
    with open("only_new_channels.m3u", "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        if not found_channels:
            f.write("# No active channels found at this moment\n")
        else:
            for name, link in found_channels:
                f.write(f'#EXTINF:-1 group-title="ASIM_ULTRA_DEEP",{name}\n{link}\n\n')
    
    print(f"Successfully found {len(found_channels)} active channels.")

if __name__ == "__main__":
    main()
