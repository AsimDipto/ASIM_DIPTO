import requests
import itertools
import string

# আপনার স্থায়ী আইপি
base_url = "http://203.18.159.115/"

# ফ্লুসোনিক সার্ভারের সম্ভাব্য সব পাথ (যাতে ফরম্যাট বদলালেও কাজ করে)
suffixes = [
    "/tracks-v1a1/mono.m3u8", 
    "/index.m3u8", 
    "/mono.m3u8",
    "/video.m3u8",
    "/playlist.m3u8"
]

def generate_scan_list():
    scan_set = set()
    
    # ১. সাধারণ নাম (বড়, ছোট ও ক্যাপিটাল লেটার)
    keywords = ['Sony', 'Star', 'Zee', 'Colors', 'Ten', 'Sports', 'Jalsha', 'Movies', 'Nick', 'Discovery']
    for k in keywords:
        scan_set.add(k.upper())
        scan_set.add(k.lower())
        scan_set.add(k.capitalize())
        scan_set.add(k.upper() + "HD")

    # ২. সংখ্যা স্ক্যান (০ থেকে ৯৯৯)
    for i in range(0, 1000):
        scan_set.add(str(i))

    # ৩. ২ অক্ষরের সব হিজিবিজি কোড (যেমন: a1, q9, zz)
    chars = string.ascii_lowercase + string.digits
    brute_2 = [''.join(i) for i in itertools.product(chars, repeat=2)]
    scan_set.update(brute_2)
    
    return sorted(list(scan_set))

def main():
    scan_list = generate_scan_list()
    found_channels = []
    headers = {'User-Agent': 'VLC/3.0.12'}
    
    print(f"Starting Scan... Total combinations: {len(scan_list)}")

    for channel in scan_list:
        for sfx in suffixes:
            url = f"{base_url}{channel}{sfx}"
            try:
                # দ্রুত স্ক্যান করার জন্য timeout ০.৩ সেকেন্ড রাখা হয়েছে
                r = requests.head(url, headers=headers, timeout=0.3)
                if r.status_code == 200:
                    print(f"FOUND: {channel}")
                    found_channels.append(url)
                    break 
            except:
                continue

    # ফাইলটি 'only_new_channels.m3u' নামেই সেভ হবে
    with open("only_new_channels.m3u", "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for link in found_channels:
            # ইউআরএল থেকে নাম আলাদা করা
            parts = link.split('/')
            name = parts[-3] if 'tracks' in link else parts[-2]
            f.write(f'#EXTINF:-1 group-title="AUTO_DETECTED",{name}\n{link}\n\n')

    print(f"Scan Finished! Total {len(found_channels)} streams found.")

if __name__ == "__main__":
    main()
