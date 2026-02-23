import requests
from concurrent.futures import ThreadPoolExecutor
import itertools
import string

# আপনার টার্গেট আইপি
base_url = "http://203.18.159.115/"

def check_url(url, session, found_channels):
    try:
        # সুপার ফাস্ট করার জন্য timeout ০.২ সেকেন্ড
        r = session.head(url, timeout=0.2)
        if r.status_code == 200:
            print(f"CRACKED: {url}")
            found_channels.append(url)
    except:
        pass

def main():
    # ২-অক্ষরের সব কোড এবং ১০০০টি নম্বর জেনারেট করা
    scan_set = set()
    chars = string.ascii_lowercase + string.digits
    scan_set.update([''.join(i) for i in itertools.product(chars, repeat=2)])
    for i in range(0, 1001):
        scan_set.add(str(i))
    
    # ফ্লুসোনিক সার্ভারের ৩টি প্রধান পাথ
    suffixes = ["/mono.m3u8", "/index.m3u8", "/tracks-v1a1/mono.m3u8"]
    found_channels = []
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'VLC/3.0.12'})

    print(f"Ultra Fast Scan Started... Checking {len(scan_set)} IDs")

    # একসাথে ১৫টি থ্রেড বা কানেকশন ব্যবহার করে গতি বাড়ানো হয়েছে
    with ThreadPoolExecutor(max_workers=15) as executor:
        for channel in scan_set:
            for sfx in suffixes:
                url = f"{base_url}{channel}{sfx}"
                executor.submit(check_url, url, session, found_channels)

    # ফাইল সেভ করা (আপনার দেওয়া নামে)
    with open("only_new_channels.m3u", "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for link in found_channels:
            try:
                name = link.split('/')[-2]
            except:
                name = "Unknown"
            f.write(f'#EXTINF:-1 group-title="ASIM_ULTRA_FAST",{name}\n{link}\n\n')

    print(f"Finished! Found {len(found_channels)} streams.")

if __name__ == "__main__":
    main()
