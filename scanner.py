import requests
from concurrent.futures import ThreadPoolExecutor

# ১. সার্ভার ইউআরএল
base_url = "http://stvlive.net:8080/"

# ২. পূর্ণাঙ্গ চ্যানেলের তালিকা (GitHub HD Logo URL shoho)
CHANNELS_DATA = [
    # --- Bangladesh (BD) ---
    ("btv", "BTV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/btv-hd-bd.png"),
    ("btvchotto", "BTV Chottogram", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/btv-chattogram-bd.png"),
    ("btvnews", "BTV News HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/btv-news-hd-bd.png"),
    ("sangsad", "Sangsad TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/sangsad-television-bd.png"),
    ("atnbangla", "ATN Bangla HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/atn-bangla-hd-bd.png"),
    ("channeli", "Channel I HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/channel-i-hd-bd.png"),
    ("ntv", "N TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/n-tv-hd-bd.png"),
    ("atnnews", "ATN News HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/atn-news-hd-bd.png"),
    ("rtv", "R TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/r-tv-hd-bd.png"),
    ("ekushey", "Ekushey TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/ekushey-tv-hd-bd.png"),
    ("boishakhi", "Boishakhi TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/boishakhi-tv-hd-bd.png"),
    ("banglavision", "Banglavision HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/banglavision-hd-bd.png"),
    ("desh", "Desh TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/desh-tv-hd-bd.png"),
    ("mytv", "My TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/my-tv-hd-bd.png"),
    ("bijoy", "Bijoy TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/bijoy-tv-hd-bd.png"),
    ("mohona", "Mohona TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/mohona-tv-hd-bd.png"),
    ("moviebangla", "Movie Bangla", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/movie-bangla-tv-bd.png"),
    ("somoy", "Somoy News", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/somoy-bd.png"),
    ("independent", "Independent TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/independent-bd.png"),
    ("maasranga", "Maasranga HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/maasranga-hd-bd.png"),
    ("channel9", "Channel 9 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/channel-9-hd-bd.png"),
    ("channel24", "Channel 24", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/channel-24-bd.png"),
    ("gtv", "GTV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/gtv-hd-bd.png"),
    ("ekattor", "Ekattor TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/ekattor-tv-hd-bd.png"),
    ("asian", "Asian TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/asian-tv-bd.png"),
    ("satv", "SA TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/sa-tv-hd-bd.png"),
    ("gaanbangla", "Gaan Bangla", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/gaan-bangla-bd.png"),
    ("jamuna", "Jamuna TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/jamuna-tv-bd.png"),
    ("ekhon", "Ekhon TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/ekhon-bd.png"),
    ("deepto", "Deepto TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/deepto-tv-hd-bd.png"),
    ("news24", "News 24 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/news-24-hd-bd.png"),
    ("banglatv", "Bangla TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/bangla-tv-hd-bd.png"),
    ("duranta", "Duronto TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/duronto-bd.png"),
    ("ananda", "Ananda TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/ananda-tv-bd.png"),
    ("dbcnews", "DBC News", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/dbc-news-bd.png"),
    ("tsports", "T Sports HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/t-sports-hd-bd.png"),
    ("greentv", "Green TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/green-tv-bd.png"),
    ("globaltv", "Global TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/global-television-hd-bd.png"),
    ("nexustv", "Nexus TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/nexus-television-hd-bd.png"),

    # --- India (West Bengal & Hindi) ---
    ("starjalsha", "Star Jalsha HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/star-jalsha-hd-in.png"),
    ("zeebangla", "Zee Bangla HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/zee-bangla-hd-in.png"),
    ("jalshamovies", "Jalsha Movies HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/jalsha-movies-hd-in.png"),
    ("colorsbangla", "Colors Bangla HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/colors-bangla-hd-in.png"),
    ("zeebanglacinema", "Zee Bangla Cinema", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/zee-bangla-cinema-in.png"),
    ("sonyent", "Sony Entertainment TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-entertainment-television-hd-in.png"),
    ("starplus", "Star Plus HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/star-plus-hd-in.png"),
    ("zeetv", "Zee TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/zee-tv-hd-in.png"),
    ("sonymax", "Sony Max HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-max-hd-in.png"),
    ("stargold", "Star Gold HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/star-gold-hd-in.png"),
    ("colors", "Colors HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/colors-hd-in.png"),
    ("colorscineplex", "Colors Cineplex HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/colors-cineplex-hd-in.png"),
    ("sonyaath", "Sony Aath", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-aath-in.png"),
    ("sunbangla", "Sun Bangla HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sun-bangla-hd-in.png"),
    ("aakashaath", "Aakash Aath", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/aakash-aath-in.png"),
    ("abpananda", "ABP Ananda", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/abp-ananda-in.png"),
    ("zee24ghanta", "Zee 24 Ghanta", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/zee-24-ghanta-in.png"),
    ("news18bangla", "News18 Bangla", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/news-18-india-in.png"), # Variant check-e ashbe
    
    # --- Sports ---
    ("starsports1", "Star Sports 1 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/star-sports-1-in.png"),
    ("starsports2", "Star Sports 2", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/star-sports-2-in.png"),
    ("sonyten1", "Sony Ten 1 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-ten-1-hd-in.png"),
    ("sonyten2", "Sony Ten 2 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-ten-2-hd-in.png"),
    ("sonyten3", "Sony Ten 3 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-ten-3-hd-in.png"),
    ("sonyten5", "Sony Ten 5 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-ten-5-hd-in.png"),
    ("sports18", "Sports 18 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sports-18-in.png"),
    ("ptvsports", "PTV Sports HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/ptv-sports-in.png"),

    # --- Movies & English ---
    ("starmovies", "Star Movies HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/star-movies-hd-in.png"),
    ("sonypix", "Sony Pix HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-pix-hd-in.png"),
    ("moviesnow", "Movies Now HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/movies-now-hd-in.png"),
    ("mnx", "MNX HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/mnx-hd-in.png"),
    ("andflix", "And Flix HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/and-flix-hd-in.png"),
    ("andpictures", "And Pictures HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/and-pictures-hd-in.png"),
    ("zeecafe", "Zee Cafe HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/zee-cafe-hd-in.png"),

    # --- Infotainment & Kids ---
    ("discovery", "Discovery HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/discovery-kids-in.png"),
    ("natgeo", "Nat Geo HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/dd-india-hd-in.png"), # Replacement
    ("historytv18", "History TV18 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/history-tv18-hd-in.png"),
    ("sonybbcearth", "Sony BBC Earth HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-bbc-earth-hd-in.png"),
    ("nick", "Nick HD+", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/nick-hd-plus-in.png"),
    ("pogo", "Pogo", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/pogo-in.png"),
    ("hungama", "Hungama", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/hungama-in.png"),
    ("cartoonnetwork", "Cartoon Network HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/cartoon-network-hd-plus-in.png"),
    ("sonyyay", "Sony Yay", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/India/sony-yay-in.png")
]

# ৩. সম্ভাব্য সাফিক্স
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
    print(f"🔍 Deep Scan starting on {base_url} (Full HD Logo List)...")

    # Fast scan-er jonno 50 threads
    with ThreadPoolExecutor(max_workers=50) as executor:
        for ch in CHANNELS_DATA:
            executor.submit(scan_logic, ch, session, found_channels)

    output_file = "Fuck-you-Ankita.m3u"
    with open(output_file, "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        # Serial maintain korar jonno
        for original in CHANNELS_DATA:
            for item in found_channels:
                if item[0] == original[1]:
                    # group-title bad, logo URL shoho
                    f.write(f'#EXTINF:-1 tvg-logo="{item[2]}",{item[0]}\n{item[1]}\n\n')
    
    print(f"\n✨ Scan Complete. Total {len(found_channels)} found. Saved as: {output_file}")

if __name__ == "__main__":
    main()
