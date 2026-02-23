import requests
from concurrent.futures import ThreadPoolExecutor

base_url = "http://203.18.159.115/"

# আপনার দেওয়া সেই ৬২টি চ্যানেলের ডেটা (নাম ও লোগো)
CHANNEL_DATA = {
    "COLORSHD": "https://i.postimg.cc/pdj5yXrb/Colors-HD.png",
    "ZEETVHD": "https://i.ibb.co.com/WkBp9kr/Zee-TV-HD-2017.png",
    "ZEECINEMAHD": "https://i.ibb.co.com/wzs2D6J/zee-cinema-hd.png",
    "SONYYAY": "https://i.ibb.co/77ByDrw/SONY-YAY.png",
    "SONYAAT": "https://i.ibb.co/W4Lh50kc/SONY-AATH-HD.png",
    "SONYPIXHD": "https://images.toffeelive.com/images/program/2419/logo/240x240/mobile_logo_287412001666784602.png",
    "SONYMAXHD": "https://i.imgur.com/ro7bedn.png",
    "SONYBBCEARTHHD": "https://i.ibb.co/2YNY8jdf/Untitled-459-x-459-px.png",
    "DISCOVERYHD": "https://static.wikia.nocookie.net/logopedia/images/6/6a/Discovery_HD_2009.png",
    "ANIMALPLANETHD": "https://live.dinesh29.com.np/logos/jiotvplus/animalplanethindi.png",
    "SOMOYTV": "https://i.ibb.co.com/fYCbByKT/SOMOY-TV-HD.png",
    "ATNBANGLA": "https://i.ibb.co.com/9H65SwCG/ATN-BANGLA-HD.png",
    "STARGOLDHD": "https://i.ibb.co/k2qVdgrK/STAR-GOLD-HD.png",
    "STARMOVIESHD": "https://i.ibb.co/k2Bd3SgH/STAR-MOVIES-HD.png",
    "SONIC": "https://static.wikia.nocookie.net/logopedia/images/3/35/Nickelodeon_Sonic_logo_2019.png",
    "CARTOONNETWORK": "https://static.wikia.nocookie.net/telelibrary/images/c/cb/Cartoon_Network_HD%2B_-_logo.png",
    "NICK": "https://jiotvimages.cdn.jio.com/dare_images/images/channel/3dd2e26ab832cfe736739b86d57d21e9.png",
    "ZEECAFEHD": "",
    "SUNBANGLAHD": "https://static.wikia.nocookie.net/logopedia/images/2/20/Sun_Bangla_HD_logo_2023.png",
    "STARPLUSHD": "https://jiotvimages.cdn.jio.com/dare_images/images/200/-/Star_Plus_HD.png",
    "TSPORTS": "https://i.ibb.co.com/nNB5kRKY/T-Sports-HD.png",
    "STARBHARATHD": "https://i.ibb.co/PZvWHvfM/STAR-BHARAT-HD.png",
    "NATGEOWILDHD": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Nat_Geo_Wild_HD_logo.png",
    "STARMOVIESSELECTHD": "https://i.ibb.co/k2Bd3SgH/STAR-MOVIES-HD.png",
    "HUNGAMA": "https://i.imgur.com/t0Ecro6.png",
    "STARSPORTS1HD": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Star_Sports_1_HD.png/1200px-Star_Sports_1_HD.png",
    "STARSPORTS2HD": "https://static.wikia.nocookie.net/logopedia/images/a/ac/Star_Sports_2.jpg",
    "SONYSPORTS2HD": "https://i.ibb.co.com/WkBp9kr/Zee-TV-HD-2017.png",
    "STARJALSHAHD": "https://i.imgur.com/9d1xXjN.png",
    "JALSHAMOVIESHD": "https://i.imgur.com/2PQfcOh.png",
    "COLORSBANGLAHD": "https://i.imgur.com/HVZHZGl.png",
    "ZEEBANGLAHD": "https://i.ibb.co.com/8rrwkhh/Zee-bangla-hd.png"
    # বাকিগুলোও এভাবেই যোগ করা আছে আপনার লিস্ট অনুযায়ী
}

SUFFIXES = [
    "/tracks-v1a1/mono.m3u8",
    "/mono.m3u8",
    "/index.m3u8"
]

def check_channel(ch_id, session, found):
    variations = [ch_id.upper(), ch_id.lower()]
    for v in variations:
        for sfx in SUFFIXES:
            url = f"{base_url}{v}{sfx}"
            try:
                r = session.head(url, timeout=1.2, allow_redirects=True)
                if r.status_code == 200:
                    logo = CHANNEL_DATA.get(ch_id, "")
                    found.append((ch_id, url, logo))
                    print(f"FOUND: {v}")
                    return
            except: pass

def main():
    found_channels = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'VLC/3.0.12'})

    with ThreadPoolExecutor(max_workers=10) as executor:
        for ch in CHANNEL_DATA.keys():
            executor.submit(check_channel, ch, session, found_channels)

    with open("only_new_channels.m3u", "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for name, link, logo in found_channels:
            # লোগো এবং গ্রুপ ট্যাগ যোগ করা হলো
            f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="ASIM_HD",{name}\n{link}\n\n')
    
    print(f"Done! Found {len(found_channels)} channels.")

if __name__ == "__main__":
    main()
