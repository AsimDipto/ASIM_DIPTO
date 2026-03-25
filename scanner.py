import requests
from concurrent.futures import ThreadPoolExecutor

# ১. সার্ভার ইউআরএল (Port shoho)
base_url = "http://stvlive.net:8080/"

# ২. ১০৩+ চ্যানেলের পূর্ণাঙ্গ ডাটা (Logo URL shoho)
CHANNELS_DATA = [
    # --- BD Entertainment & News ---
    ("btv", "BTV", "https://i.postimg.cc/qM9nQpDk/btv.png"),
    ("btvchotto", "BTV Chottogram", ""),
    ("btvnews", "BTV News", ""),
    ("sangsad", "Sangsad TV", ""),
    ("atnnews", "ATN News", "https://i.postimg.cc/9fqFNKZ0/ATN-News-Logo-without-slogan-svg.png"),
    ("banglavision", "Banglavision", "https://i.postimg.cc/7L46Z2q7/banglavision.png"),
    ("ntv", "N TV", "https://i.postimg.cc/zX30tN0v/ntv.png"),
    ("channeli", "Channel I", "https://i.postimg.cc/NjZ3x3K7/channel-i.png"),
    ("boishakhi", "Boishakhi TV", "https://i.postimg.cc/C1QyHkLp/boishakhi.png"),
    ("rtv", "R TV", "https://i.postimg.cc/L5X0V6P4/rtv.png"),
    ("ekushey", "Ekushey TV", ""),
    ("atnbangla", "ATN Bangla", "https://i.ibb.co.com/9H65SwCG/ATN-BANGLA-HD.png"),
    ("desh", "Desh TV", ""),
    ("mytv", "My TV", ""),
    ("moviebangla", "Movie Bangla", ""),
    ("mohona", "Mohona TV", "https://i.postimg.cc/mD8zQ0Z3/mohona.png"),
    ("bijoy", "Bijoy TV", ""),
    ("independent", "Independent TV", "https://i.imgur.com/kviJN1i.png"),
    ("somoy", "Somoy TV", "https://i.ibb.co.com/fYCbByKT/SOMOY-TV-HD.png"),
    ("maasranga", "Maasranga HD", "https://i.postimg.cc/GmFLcvNB/Maasranga-Television-Logo.jpg"),
    ("gtv", "G TV", "https://i.postimg.cc/s2qpdYbJ/Logo-of-GTV-(Bangladesh).png"),
    ("channel9", "Channel 9", ""),
    ("channel24", "Channel 24", "https://i.imgur.com/MmhxR5E.png"),
    ("satv", "SA TV", ""),
    ("asian", "Asian TV", ""),
    ("ekhon", "Ekhon TV", ""),
    ("jamuna", "Jamuna TV", "https://i.imgur.com/ds3aThu.jpg"),
    ("deepto", "Deepto TV", ""),
    ("gaanbangla", "Gaan Bangla", ""),
    ("dbcnews", "DBC news", ""),
    ("duranta", "Duronto TV", "https://i.imgur.com/PK9Gm5g.png"),
    ("nagorik", "Nagorik TV", "https://i.postimg.cc/hvn7pf00/Logo-of-Nagorik-TV.png"),
    ("banglatv", "Bangla TV", ""),
    ("ananda", "Ananda TV", ""),

    # --- West Bengal (Kolkata) ---
    ("starjalsha", "Star Jalsha HD", "https://i.postimg.cc/3RQcFQdV/starjalshahd.png"),
    ("zeebangla", "Zee Bangla HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/zee-bangla-hd-in.png"),
    ("jalshamovies", "Jalsha Movies HD", "https://i.postimg.cc/3RQcFQdV/starjalshahd.png"),
    ("colorsbangla", "Colors Bangla HD", "https://i.imgur.com/HVZHZGl.png"),
    ("colorsbanglacinema", "Colors Bangla Cinema", "https://static.wikia.nocookie.net/etv-gspn-bangla/images/7/7e/Colors_Bangla_Cinema_logo_%282024-present%29.png"),
    ("zeebanglacinema", "Zee Bangla Cinema", "https://i.postimg.cc/GmP3xqfn/1000102537.png"),
    ("sonyaath", "Sony Aath", "https://i.ibb.co/W4Lh50kc/SONY-AATH-HD.png"),
    ("sunbangla", "Sun Bangla HD", "https://static.wikia.nocookie.net/logopedia/images/2/20/Sun_Bangla_HD_logo_2023.png"),
    ("aakashaath", "Aakash Aath", ""),
    ("enterr10", "Enter10 Bangla", "https://i.imgur.com/Tp3Kead.png"),
    ("sonyyay", "Sony Yay", "https://i.ibb.co/77ByDrw/SONY-YAY.png"),

    # --- Sports ---
    ("tsports", "T Sports HD", "https://i.ibb.co.com/nNB5kRKY/T-Sports-HD.png"),
    ("ptvsports", "PTV Sports HD", "https://i.postimg.cc/nrb9LTSs/PTV-Sports.png"),
    ("asports", "A Sports HD", "https://i.postimg.cc/mZmGBhcR/unnamed.png"),
    ("starsports1", "Star Sports 1 HD", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Star_Sports_1_HD.png/1200px-Star_Sports_1_HD.png"),
    ("starsports2", "Star Sports 2 HD", "https://static.wikia.nocookie.net/logopedia/images/a/ac/Star_Sports_2.jpg"),
    ("sonysports1", "Sony Sports Ten 1 HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/sony-ten-1-hd-in.png"),
    ("sonysports2", "Sony Sports Ten 2 HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/sony-ten-2-hd-in.png"),
    ("sonysports5", "Sony Sports Ten 5 HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/sony-ten-5-hd-in.png"),
    ("eurosports", "Eurosports", "https://i.postimg.cc/hGWd2DxW/Eurosport-Logo-2015.png"),

    # --- Hindi Entertainment & Movies ---
    ("colors", "Colors HD", "https://i.postimg.cc/pdj5yXrb/Colors-HD.png"),
    ("starplus", "Star Plus HD", "https://i.postimg.cc/QxDjxvmJ/Star-Plus.png"),
    ("sonyent", "Sony Entertainment TV HD", "https://i.postimg.cc/GhjBKLV8/SETHD.png"),
    ("zeetv", "Zee TV HD", "https://i.postimg.cc/tT2qPJYG/Zee-TV-HD-2025.png"),
    ("stargold", "Star Gold HD", "https://i.postimg.cc/GmvxR8Mm/Star-Gold-2020.png"),
    ("sonymax", "Sony Max HD", "https://i.postimg.cc/qqbPBCgB/Sony-max-hd.png"),
    ("colorscineplex", "Colors Cineplex HD", "http://jiotv.catchup.cdn.jio.com/dare_images/images/Color_Cineplex_HD.png"),
    ("zoom", "Zoom", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/zoom-in.png"),
    ("zing", "Zing", "https://i.postimg.cc/T18NYqJn/Zing-2025.png"),

    # --- English & Infotainment ---
    ("starmovies", "Star Movies HD", "https://i.ibb.co/k2Bd3SgH/STAR-MOVIES-HD.png"),
    ("sonypix", "Sony Pix HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/sony-pix-hd-in.png"),
    ("moviesnow", "Movies Now HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/movies-now-hd-in.png"),
    ("zeecafe", "Zee Cafe HD", "https://i.postimg.cc/k46VnWTv/Zee-Cafe-2025.png"),
    ("andpictures", "And Picturs HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/and-pictures-hd-in.png"),
    ("andflix", "And Flix HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/and-flix-hd-in.png"),
    ("discovery", "Discovery HD", "https://static.wikia.nocookie.net/logopedia/images/6/6a/Discovery_HD_2009.png"),
    ("animalplanet", "Animal Planet HD", "https://i.postimg.cc/6psvT4dX/Animal-Planet-HD-282018-n-v-29.png"),
    ("natgeo", "National Geographic HD", "https://i.postimg.cc/MKVttQbr/national-geographic-hd.png"),
    ("history", "History TV HD", "https://i.postimg.cc/XJq5rpgc/History-tv18-hd.png"),
    ("sonybbcearth", "Sony BBC Earth HD", "https://i.postimg.cc/qRMtW9KH/images-(4).jpg"),

    # --- Kids ---
    ("hungama", "Hungama", "https://i.imgur.com/t0Ecro6.png"),
    ("pogo", "Pogo", "https://i.imgur.com/i5J3zrE.png"),
    ("nickjr", "Nick Jr", "https://i.imgur.com/chT8xP5.png"),
    ("sonic", "Sonic", "https://static.wikia.nocookie.net/logopedia/images/3/35/Nickelodeon_Sonic_logo_2019.png"),
    ("cartoonnetwork", "Cartoon Network HD", "https://static.wikia.nocookie.net/telelibrary/images/c/cb/Cartoon_Network_HD%2B_-_logo.png"),
    ("balbharat", "Bal Bharat", "https://i.postimg.cc/VkM6JYwZ/ETV-Bal-Bharat-logo.png")
]

# ৩. সম্ভাব্য লিঙ্ক ফরম্যাট
POSSIBLE_SUFFIXES = ["/tracks-v1a1/mono.m3u8", "/mono.m3u8", "/index.m3u8", "/playlist.m3u8"]

def scan_logic(ch, session, results):
    ch_id, display_name, logo_url = ch
    
    # variants check: mohona, mohonatv, mohonatvhd, mohonahd
    variants = [ch_id, ch_id + "tv", ch_id + "tvhd", ch_id + "hd"]
    
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

    print(f"🔍 Deep Scan starting on {base_url} (With Logos)...")

    with ThreadPoolExecutor(max_workers=50) as executor:
        for ch in CHANNELS_DATA:
            executor.submit(scan_logic, ch, session, found_channels)

    output_file = "Fuck-you-Ankita.m3u"
    with open(output_file, "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for original in CHANNELS_DATA:
            for item in found_channels:
                if item[0] == original[1]:
                    # group-title bad dewa hoyeche, logo URL add kora holo
                    f.write(f'#EXTINF:-1 tvg-logo="{item[2]}",{item[0]}\n{item[1]}\n\n')
    
    print(f"\n✨ Scan Complete. Total {len(found_channels)} found. Saved as: {output_file}")

if __name__ == "__main__":
    main()
