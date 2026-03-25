import requests
from concurrent.futures import ThreadPoolExecutor

# ১. সার্ভার ইউআরএল
base_url = "http://stvlive.net:8080/"

# ২. ১০৩+ চ্যানেলের পূর্ণাঙ্গ ডাটা (ID short & small letter-e kora hoyeche)
CHANNELS_DATA = [
    # --- BD Entertainment & News ---
    ("btv", "BTV", ""), ("btvchotto", "BTV Chottogram", ""), ("btvnews", "BTV News", ""),
    ("sangsad", "Sangsad TV", ""), ("atnnews", "ATN News", "https://i.postimg.cc/9fqFNKZ0/ATN-News-Logo-without-slogan-svg.png"),
    ("banglavision", "Banglavision", ""), ("ntv", "N TV", ""), ("channeli", "Channel I", ""),
    ("boishakhi", "Boishakhi TV", ""), ("rtv", "R TV", ""), ("ekushey", "Ekushey TV", ""),
    ("atnbangla", "ATN Bangla", ""), ("desh", "Desh TV", ""), ("mytv", "My TV", ""),
    ("moviebangla", "Movie Bangla", ""), ("mohona", "Mohona TV", ""), ("bijoy", "Bijoy TV", ""),
    ("independent", "Independent TV", "https://i.imgur.com/kviJN1i.png"),
    ("somoy", "Somoy TV", "https://i.ibb.co.com/fYCbByKT/SOMOY-TV-HD.png"),
    ("maasranga", "Maasranga HD", ""), ("gtv", "G TV", ""), ("channel9", "Channel 9", ""),
    ("channel24", "Channel 24", ""), ("satv", "SA TV", ""), ("asian", "Asian TV", ""),
    ("ekhon", "Ekhon TV", ""), ("jamuna", "Jamuna TV", ""), ("deepto", "Deepto TV", ""),
    ("gaanbangla", "Gaan Bangla", ""), ("dbcnews", "DBC news", ""), ("duranta", "Duronto TV", ""),
    ("nagorik", "Nagorik TV", ""), ("banglatv", "Bangla TV", ""), ("ananda", "Ananda TV", ""),

    # --- West Bengal (Kolkata) ---
    ("starjalsha", "Star Jalsha HD", ""), ("zeebangla", "Zee Bangla HD", ""),
    ("jalshamovies", "Jalsha Movies HD", ""), ("colorsbangla", "Colors Bangla HD", ""),
    ("colorsbanglacinema", "Colors Bangla Cinema", ""), ("zeebanglacinema", "Zee Bangla Cinema", ""),
    ("sonyaath", "Sony Aath", ""), ("sunbangla", "Sun Bangla HD", ""), ("aakashaath", "Aakash Aath", ""),
    ("enterr10", "Enter10 Bangla", ""), ("sonyyay", "Sony Yay", ""), ("ruposhi", "Ruposhi Bangla", ""),
    ("news18bangla", "News18 Bangla", ""), ("zeenews24", "Zee 24 Ghanta", ""),

    # --- Sports ---
    ("tsports", "T Sports HD", ""), ("ptvsports", "PTV Sports HD", ""), ("asports", "A Sports HD", ""),
    ("starsports1", "Star Sports 1 HD", ""), ("starsports2", "Star Sports 2 HD", ""),
    ("starsports3", "Star Sports 3", ""), ("starsportsselect1", "Star Sports Select 1 HD", ""),
    ("starsportsselect2", "Star Sports Select 2 HD", ""), ("sonysports1", "Sony Sports Ten 1 HD", ""),
    ("sonysports2", "Sony Sports Ten 2 HD", ""), ("sonysports3", "Sony Sports Ten 3", ""),
    ("sonysports5", "Sony Sports Ten 5 HD", ""), ("eurosports", "Eurosports", ""),
    ("willow", "Willow Cricket", ""), ("beinsports", "Bein Sports", ""), ("golf", "Golf Sports", ""),

    # --- Hindi Entertainment & Movies ---
    ("colors", "Colors HD", ""), ("starplus", "Star Plus HD", ""), ("sonyent", "Sony Entertainment TV HD", ""),
    ("zeetv", "Zee TV HD", ""), ("sabtv", "Sony SAB HD", ""), ("starbharat", "Star Bharat HD", ""),
    ("stargold", "Star Gold HD", ""), ("sonymax", "Sony Max HD", ""), ("colorscineplex", "Colors Cineplex HD", ""),
    ("zeecinema", "Zee Cinema HD", ""), ("andpictures", "And Pictures HD", ""), ("utvmovies", "UTV Movies", ""),
    ("zoom", "Zoom", ""), ("zing", "Zing", ""), ("bindass", "Bindass", ""),

    # --- English Movies & Infotainment ---
    ("starmovies", "Star Movies HD", ""), ("sonypix", "Sony Pix HD", ""), ("moviesnow", "Movies Now HD", ""),
    ("mnx", "MNX HD", ""), ("andflix", "And Flix HD", ""), ("andprive", "And Prive HD", ""),
    ("zeecafe", "Zee Cafe HD", ""), ("discovery", "Discovery HD", ""), ("animalplanet", "Animal Planet HD", ""),
    ("natgeo", "National Geographic HD", ""), ("natgeowild", "National Geo Wild HD", ""),
    ("history", "History TV HD", ""), ("sonybbcearth", "Sony BBC Earth HD", ""),
    ("tlc", "TLC HD", ""), ("travelxp", "Travel XP HD", ""), ("investigationdiscovery", "ID HD", ""),

    # --- Kids ---
    ("hungama", "Hungama", ""), ("pogo", "Pogo", ""), ("nick", "Nick", ""), ("nickjr", "Nick Jr", ""),
    ("sonic", "Sonic", ""), ("cartoonnetwork", "Cartoon Network HD", ""), ("disney", "Disney Channel", ""),
    ("balbharat", "ETV Bal Bharat", ""), ("marvelhq", "Marvel HQ", "")
]

# ৩. সম্ভাব্য সাফিক্স
POSSIBLE_SUFFIXES = ["/tracks-v1a1/mono.m3u8", "/mono.m3u8", "/index.m3u8", "/playlist.m3u8"]

def scan_logic(ch, session, results):
    ch_id, display_name, logo_url = ch
    
    # 4-ti variant auto generate korbe: mohona, mohonatv, mohonatvhd, mohonahd
    variants = [
        ch_id,
        ch_id + "tv",
        ch_id + "tvhd",
        ch_id + "hd"
    ]
    
    for variant in dict.fromkeys(variants):
        for sfx in POSSIBLE_SUFFIXES:
            url = f"{base_url}{variant}{sfx}"
            try:
                headers = {'User-Agent': 'VLC/3.0.12'}
                r = session.head(url, headers=headers, timeout=2.0, allow_redirects=True)
                
                if r.status_code == 200:
                    results.append((display_name, url, logo_url))
                    print(f"✅ Found: {variant}")
                    return 
            except:
                continue

def main():
    session = requests.Session()
    found_channels = []

    print(f"🔍 Deep Scanning 103+ Channels on {base_url}...")

    # Fast scan-er jonno 50 threads
    with ThreadPoolExecutor(max_workers=50) as executor:
        for ch in CHANNELS_DATA:
            executor.submit(scan_logic, ch, session, found_channels)

    # Serial maintain kore save kora
    output_file = "Fuck-you-Ankita.m3u"
    with open(output_file, "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for original in CHANNELS_DATA:
            for item in found_channels:
                if item[0] == original[1]:
                    # No group-title
                    f.write(f'#EXTINF:-1 tvg-logo="{item[2]}",{item[0]}\n{item[1]}\n\n')
    
    print(f"\n✨ Scan Complete. Total {len(found_channels)} channels found.")
    print(f"📁 File: {output_file}")

if __name__ == "__main__":
    main()
