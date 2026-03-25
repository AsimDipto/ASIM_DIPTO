import requests
from concurrent.futures import ThreadPoolExecutor

# ১. সার্ভার ইউআরএল (Port shoho)
base_url = "http://stvlive.net:8080/"

# ২. আপনার দেওয়া সকল চ্যানেলের পূর্ণাঙ্গ ডাটা
CHANNELS_DATA = [
    # --- জাতীয় ও সাধারণ বিনোদন ---
    ("BTV", "BTV", ""),
    ("BTVCHOTTO", "BTV Chottogram", ""),
    ("BTVNEWS", "BTV News", ""),
    ("SANGSADTV", "Sangsad TV", ""),
    ("ATNNEWS", "ATN News", "https://i.postimg.cc/9fqFNKZ0/ATN-News-Logo-without-slogan-svg.png"),
    ("BANGLAVISION", "Banglavision", ""),
    ("NTV", "N TV", ""),
    ("CHANNELI", "Channel I", ""),
    ("BOISHAKHITV", "Boishakhi TV", ""),
    ("RTV", "R TV", ""),
    ("EKUSHEYTV", "Ekushey TV", ""),
    ("ATNBANGLA", "ATN Bangla", "https://i.ibb.co.com/9H65SwCG/ATN-BANGLA-HD.png"),
    ("DESHTV", "Desh TV", ""),
    ("MYTV", "My TV", ""),
    ("MOVIEBANGLA", "Movie Bangla", ""),
    ("MOHONATV", "Mohona TV", ""),
    ("BIJOYTV", "Bijoy TV", ""),
    ("INDEPENDENTTV", "Independent TV", "https://i.imgur.com/kviJN1i.png"),
    ("SOMOYTV", "Somoy TV", "https://i.ibb.co.com/fYCbByKT/SOMOY-TV-HD.png"),
    ("MAASRANGAHD", "Maasranga HD", "https://i.postimg.cc/GmFLcvNB/Maasranga-Television-Logo.jpg"),
    ("GTV", "G TV", "https://i.postimg.cc/s2qpdYbJ/Logo-of-GTV-(Bangladesh).png"),
    ("CHANNEL9", "Channel 9", ""),
    ("CHANNEL24", "Channel 24", "https://i.imgur.com/MmhxR5E.png"),
    ("SATV", "SA TV", ""),
    ("ASIANTV", "Asian TV", ""),
    ("EKHONTV", "Ekhon TV", ""),
    ("JAMUNATV", "Jamuna TV", "https://i.imgur.com/ds3aThu.jpg"),
    ("DEEPTOTV", "Deepto TV", ""),
    ("GAANBANGLA", "Gaan Bangla", ""),
    ("DBCNEWS", "DBC news", ""),
    ("DURANTATV", "Duronto TV", "https://i.imgur.com/PK9Gm5g.png"),
    ("NAGORIK", "Nagorik TV", "https://i.postimg.cc/hvn7pf00/Logo-of-Nagorik-TV.png"),
    ("BANGLATV", "Bangla TV", ""),
    ("ANANDATV", "Ananda TV", ""),

    # --- কলকাতা ও মুভি ---
    ("JALSHAMOVIESHD", "Jalsha Movies HD", "https://i.postimg.cc/3RQcFQdV/starjalshahd.png"),
    ("COLORSBANGLACINEMA", "Colors Bangla Cinema", ""),
    ("ZEEBANGLACINEMA", "Zee Bangla Cinema", ""),
    ("COLORSBANGLAHD", "Colors Bangla HD", ""),
    ("SONYAAT", "Sony Aath", ""),
    ("STARJALSHAHD", "Star Jalsha HD", ""),
    ("ZEEBANGLAHD", "Zee Bangla HD", ""),
    ("ENTERR10", "Enter10 Bangla", ""),
    ("SONYYAY", "Sony Yay", ""),
    ("TSPORTS", "T Sports HD", ""),
    ("SUNBANGLAHD", "Sun Bangla HD", ""),
    ("AAKASHAATH", "Aakash Aath", ""),

    # --- হিন্দি এন্টারটেইনমেন্ট ---
    ("COLORSHD", "Colors HD", ""),
    ("COLORSCINEPLEXHD", "Colors Cineplex HD", ""),
    ("STARPLUSHD", "Star Plus HD", ""),
    ("STARGOLDHD", "Star Gold HD", ""),
    ("STARGOLDSELECTHD", "Star Gold Select HD", ""),
    ("STARBHARATHD", "Star Bharat HD", ""),
    ("SONYENTHD", "Sony Entertainment TV HD", ""),
    ("SONYMAXHD", "Sony Max", ""),
    ("ZEETVHD", "Zee TV HD", ""),
    ("ZOOM", "Zoom", ""),
    ("ZING", "Zing", ""),

    # --- স্পোর্টস ---
    ("PTVSPORTSHD", "PTV Sports HD", ""),
    ("ASPORTSHD", "A Sports HD", ""),
    ("SONYSPORTS1HD", "Sony Sports Ten 1 HD", ""),
    ("SONYSPORTS2HD", "Sony Sports Ten 2 HD", ""),
    ("STARSPORTS1HD", "Star Sports 1 HD", ""),
    ("STARSPORTS2HD", "Star Sports 2 HD", ""),
    ("EUROSPORTSHD", "Eurosports", ""),

    # --- মুভি ও ইংরেজি ---
    ("MOVIESNOWHD", "Movies Now HD", ""),
    ("STARMOVIESHD", "Star Movies HD", ""),
    ("SONYPIXHD", "Sony Pix HD", ""),
    ("ZEECAFEHD", "Zee Cafe HD", ""),
    ("ANDPICTURSHD", "And Pictures HD", ""),
    ("ANDFLIXHD", "And Flix HD", ""),

    # --- কার্টুন ও ইনফোটেইনমেন্ট ---
    ("HUNGAMA", "Hungama", ""),
    ("POGO", "Pogo", ""),
    ("NICKJR", "Nick Jr", ""),
    ("CARTOONNETWORK", "Cartoon Network HD", ""),
    ("ANIMALPLANETHD", "Animal Planet HD", ""),
    ("DISCOVERYHD", "Discovery HD", ""),
    ("NATGEOHD", "National Geographic HD", ""),
    ("SONYBBCEARTHHD", "Sony BBC Earth HD", ""),
    ("HISTORYTVHD", "History TV HD", ""),
    ("SONYEARTH", "Sony Earth", "")
]

# ৩. সম্ভাব্য সাফিক্স (Suffixes)
POSSIBLE_SUFFIXES = [
    "/tracks-v1a1/mono.m3u8", 
    "/mono.m3u8", 
    "/index.m3u8",
    "/playlist.m3u8"
]

def scan_logic(ch, session, results):
    ch_id, display_name, logo_url = ch
    
    # Nam theke 'hd' ba 'tv' thakle seta muche die base name ber kora
    clean_base = ch_id.lower().replace("hd", "").replace("tv", "")
    
    # Apnar chawa 4-ti variants (Deep Scan)
    # Jemon: deepto, deeptotv, deeptotvhd, deeptohd
    variants = [
        clean_base,               # deepto
        clean_base + "tv",        # deeptotv
        clean_base + "tvhd",      # deeptotvhd
        clean_base + "hd"         # deeptohd
    ]
    
    # Duplicate variant bad die check kora
    for variant in dict.fromkeys(variants):
        for sfx in POSSIBLE_SUFFIXES:
            url = f"{base_url}{variant}{sfx}"
            try:
                # User-Agent VLC player set kora hoyeche
                headers = {'User-Agent': 'VLC/3.0.12'}
                r = session.head(url, headers=headers, timeout=2.5, allow_redirects=True)
                
                if r.status_code == 200:
                    results.append((display_name, url, logo_url))
                    print(f"✅ Found: {variant} ({display_name})")
                    return # Link peye gele porer variant check dorkar nai
            except:
                continue

def main():
    session = requests.Session()
    found_channels = []

    print(f"🔍 New Py Deep Scanning starting on {base_url}...")

    # fast scan-er jonno Thread count 30
    with ThreadPoolExecutor(max_workers=30) as executor:
        for ch in CHANNELS_DATA:
            executor.submit(scan_logic, ch, session, found_channels)

    # Serial onujayi M3U file save
    output_file = "Fuck-you-Ankita.m3u"
    with open(output_file, "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for original in CHANNELS_DATA:
            for item in found_channels:
                if item[0] == original[1]:
                    # group-title parameter ti bad dewa hoyeche
                    f.write(f'#EXTINF:-1 tvg-logo="{item[2]}",{item[0]}\n{item[1]}\n\n')
    
    print(f"\n✨ Update Complete. Total {len(found_channels)} channels found.")
    print(f"📁 File saved as: {output_file}")

if __name__ == "__main__":
    main()
