import requests
from concurrent.futures import ThreadPoolExecutor


base_url = "http://stvlive.net:8080/"


CHANNELS_DATA = [
    # --- BD Entertainment & News (GitHub URL use kora hoyeche) ---
    ("btv", "BTV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/btv-hd-bd.png"),
    ("btvchotto", "BTV Chottogram", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/btv-chattogram-bd.png"),
    ("btvnews", "BTV News HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/btv-news-hd-bd.png"),
    ("sangsad", "Sangsad TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/sangsad-television-bd.png"),
    ("atnnews", "ATN News HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/atn-news-hd-bd.png"),
    ("atnbangla", "ATN Bangla HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/atn-bangla-hd-bd.png"),
    ("banglavision", "Banglavision HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/banglavision-hd-bd.png"),
    ("ntv", "N TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/n-tv-hd-bd.png"),
    ("channeli", "Channel I HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/channel-i-hd-bd.png"),
    ("boishakhi", "Boishakhi TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/boishakhi-tv-hd-bd.png"),
    ("rtv", "R TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/r-tv-hd-bd.png"),
    ("ekushey", "Ekushey TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/ekushey-tv-hd-bd.png"),
    ("desh", "Desh TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/desh-tv-hd-bd.png"),
    ("mytv", "My TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/my-tv-hd-bd.png"),
    ("moviebangla", "Movie Bangla", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/movie-bangla-tv-bd.png"),
    ("mohona", "Mohona TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/mohona-tv-hd-bd.png"),
    ("bijoy", "Bijoy TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/bijoy-tv-hd-bd.png"),
    ("independent", "Independent TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/independent-bd.png"),
    ("somoy", "Somoy News", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/somoy-bd.png"),
    ("maasranga", "Maasranga HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/maasranga-hd-bd.png"),
    ("gtv", "GTV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/gtv-hd-bd.png"),
    ("channel9", "Channel 9 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/channel-9-hd-bd.png"),
    ("channel24", "Channel 24 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/channel-24-bd.png"),
    ("satv", "SA TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/sa-tv-hd-bd.png"),
    ("asian", "Asian TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/asian-tv-bd.png"),
    ("ekhon", "Ekhon TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/ekhon-bd.png"),
    ("jamuna", "Jamuna TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/jamuna-tv-bd.png"),
    ("deepto", "Deepto TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/deepto-tv-hd-bd.png"),
    ("gaanbangla", "Gaan Bangla", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/gaan-bangla-bd.png"),
    ("dbcnews", "DBC News", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/dbc-news-bd.png"),
    ("duranta", "Duronto TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/duronto-bd.png"),
    ("nagorik", "Nagorik TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/nagorik-tv-bd.png"),
    ("banglatv", "Bangla TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/bangla-tv-hd-bd.png"),
    ("ananda", "Ananda TV", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/ananda-tv-bd.png"),
    ("ekattor", "Ekattor TV HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/ekattor-tv-hd-bd.png"),
    ("news24", "News 24 HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/news-24-hd-bd.png"),

    # --- West Bengal (Kolkata) - Original Links ---
    ("starjalsha", "Star Jalsha HD", "https://i.postimg.cc/3RQcFQdV/starjalshahd.png"),
    ("zeebangla", "Zee Bangla HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/zee-bangla-hd-in.png"),
    ("jalshamovies", "Jalsha Movies HD", "https://i.postimg.cc/3RQcFQdV/starjalshahd.png"),
    ("colorsbangla", "Colors Bangla HD", "https://i.imgur.com/HVZHZGl.png"),
    ("colorsbanglacinema", "Colors Bangla Cinema", "https://static.wikia.nocookie.net/etv-gspn-bangla/images/7/7e/Colors_Bangla_Cinema_logo_%282024-present%29.png"),
    ("zeebanglacinema", "Zee Bangla Cinema", "https://i.postimg.cc/GmP3xqfn/1000102537.png"),
    ("sonyaath", "Sony Aath", "https://i.ibb.co/W4Lh50kc/SONY-AATH-HD.png"),
    ("sunbangla", "Sun Bangla HD", "https://static.wikia.nocookie.net/logopedia/images/2/20/Sun_Bangla_HD_logo_2023.png"),
    ("enterr10", "Enter10 Bangla", "https://i.imgur.com/Tp3Kead.png"),
    ("sonyyay", "Sony Yay", "https://i.ibb.co/77ByDrw/SONY-YAY.png"),

    # --- Sports ---
    ("tsports", "T Sports HD", "https://raw.githubusercontent.com/AsimDipto/Logo-box/refs/heads/main/Bangladesh/t-sports-hd-bd.png"),
    ("ptvsports", "PTV Sports HD", "https://i.postimg.cc/nrb9LTSs/PTV-Sports.png"),
    ("asports", "A Sports HD", "https://i.postimg.cc/mZmGBhcR/unnamed.png"),
    ("starsports1", "Star Sports 1 HD", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Star_Sports_1_HD.png/1200px-Star_Sports_1_HD.png"),
    ("starsports2", "Star Sports 2 HD", "https://static.wikia.nocookie.net/logopedia/images/a/ac/Star_Sports_2.jpg"),
    ("sonysports1", "Sony Sports Ten 1 HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/sony-ten-1-hd-in.png"),
    ("sonysports2", "Sony Sports Ten 2 HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/sony-ten-2-hd-in.png"),
    ("sonysports5", "Sony Sports Ten 5 HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/sony-ten-5-hd-in.png"),
    ("eurosports", "Eurosports", "https://i.postimg.cc/hGWd2DxW/Eurosport-Logo-2015.png"),

    # --- Hindi & English (Baki links same) ---
    ("colors", "Colors HD", "https://i.postimg.cc/pdj5yXrb/Colors-HD.png"),
    ("starplus", "Star Plus HD", "https://i.postimg.cc/QxDjxvmJ/Star-Plus.png"),
    ("sonyent", "Sony Entertainment TV HD", "https://i.postimg.cc/GhjBKLV8/SETHD.png"),
    ("zeetv", "Zee TV HD", "https://i.postimg.cc/tT2qPJYG/Zee-TV-HD-2025.png"),
    ("stargold", "Star Gold HD", "https://i.postimg.cc/GmvxR8Mm/Star-Gold-2020.png"),
    ("sonymax", "Sony Max HD", "https://i.postimg.cc/qqbPBCgB/Sony-max-hd.png"),
    ("colorscineplex", "Colors Cineplex HD", "http://jiotv.catchup.cdn.jio.com/dare_images/images/Color_Cineplex_HD.png"),
    ("zoom", "Zoom", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/zoom-in.png"),
    ("zing", "Zing", "https://i.postimg.cc/T18NYqJn/Zing-2025.png"),
    ("starmovies", "Star Movies HD", "https://i.ibb.co/k2Bd3SgH/STAR-MOVIES-HD.png"),
    ("sonypix", "Sony Pix HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/sony-pix-hd-in.png"),
    ("moviesnow", "Movies Now HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/movies-now-hd-in.png"),
    ("zeecafe", "Zee Cafe HD", "https://i.postimg.cc/k46VnWTv/Zee-Cafe-2025.png"),
    ("andpictures", "And Pictures HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/and-pictures-hd-in.png"),
    ("andflix", "And Flix HD", "https://raw.githubusercontent.com/abusaeeidx/Tv-Channel-Logo/refs/heads/main/countries/india/and-flix-hd-in.png"),
    ("discovery", "Discovery HD", "https://static.wikia.nocookie.net/logopedia/images/6/6a/Discovery_HD_2009.png"),
    ("animalplanet", "Animal Planet HD", "https://i.postimg.cc/6psvT4dX/Animal-Planet-HD-282018-n-v-29.png"),
    ("natgeo", "National Geographic HD", "https://i.postimg.cc/MKVttQbr/national-geographic-hd.png"),
    ("history", "History TV HD", "https://i.postimg.cc/XJq5rpgc/History-tv18-hd.png"),
    ("sonybbcearth", "Sony BBC Earth HD", "https://i.postimg.cc/qRMtW9KH/images-(4).jpg"),
    ("hungama", "Hungama", "https://i.imgur.com/t0Ecro6.png"),
    ("pogo", "Pogo", "https://i.imgur.com/i5J3zrE.png"),
    ("nickjr", "Nick Jr", "https://i.imgur.com/chT8xP5.png"),
    ("sonic", "Sonic", "https://static.wikia.nocookie.net/logopedia/images/3/35/Nickelodeon_Sonic_logo_2019.png"),
    ("cartoonnetwork", "Cartoon Network HD", "https://static.wikia.nocookie.net/telelibrary/images/c/cb/Cartoon_Network_HD%2B_-_logo.png"),
    ("balbharat", "Bal Bharat", "https://i.postimg.cc/VkM6JYwZ/ETV-Bal-Bharat-logo.png")
]


POSSIBLE_SUFFIXES = ["/tracks-v1a1/mono.m3u8", "/mono.m3u8", "/index.m3u8", "/playlist.m3u8"]

def scan_logic(ch, session, results):
    ch_id, display_name, logo_url = ch
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

    print(f"🔍 Deep Scan starting on {base_url} (With GitHub BD Logos)...")

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
                    # tvg-logo URL add kora holo
                    f.write(f'#EXTINF:-1 tvg-logo="{item[2]}",{item[0]}\n{item[1]}\n\n')
    
    print(f"\n✨ Scan Complete. Total {len(found_channels)} found. Saved as: {output_file}")

if __name__ == "__main__":
    main()
