import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # hide insecure request warnings

BASE_URL = "https://vimm.net"

# Define the 'extra' variable (the part you want to append for letter-based URLs)
extra = "2"  # You can change this value as needed

# Your main NES URL
main_url = BASE_URL + "/vault/NES"
response = requests.get(main_url, verify=False)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

selected_console = ""

all_rom_ids = set()

selections = [
    {
        0: 'Atari2600'
    },
    {
        1: 'Atari5200'
    },
    {
        2: 'NES'
    },
    {
        3: 'SMS'
    },
    {
        4: 'Atari7800'
    },
    {
        5: 'TG16'
    },
    {
        6: 'Genesis'
    },
    {
        7: 'TGCD'
    },
    {
        8: 'SNES'
    },
    {
        9: 'CDi'
    },
    {
        10: 'SegaCD'
    },
    {
        11: 'Jaguar'
    },
    {
        12: '32X'
    },
    {
        13: 'Saturn'
    },
    {
        14: 'PS1'
    },
    {
        15: 'JaguarCD'
    },
    {
        16: 'N64'
    },
    {
        17: 'Dreamcast'
    },
    {
        18: 'PS2'
    },
    {
        19: 'GameCube'
    },
    {
        20: 'Xbox'
    },
    {
        21: 'Xbox360'
    },
    {
        22: 'PS3'
    },
    {
        23: 'Wii'
    },
    {
        24: 'WiiWare'
    },
    {
        25: 'GB'
    },
    {
        26: 'Lynx'
    },
    {
        27: 'GG'
    },
    {
        28: 'VB'
    },
    {
        29: 'GBC'
    },
    {
        30: 'GBA'
    },
    {
        31: 'DS'
    },
    {
        32: 'PSP'
    },
    {
        33: '3DS'
    },
]

region_options = {
    1: "Argentina",
    2: "Asia",
    3: "Australia",
    4: "Brazil",
    5: "Canada",
    6: "China",
    7: "Denmark",
    8: "Europe",
    9: "Finland",
    10: "France",
    11: "Germany",
    12: "Greece",
    13: "Hong Kong",
    14: "Italy",
    15: "Japan",
    16: "Korea",
    17: "Mexico",
    18: "Netherlands",
    19: "Norway",
    20: "Russia",
    21: "Spain",
    22: "Sweden",
    23: "Taiwan",
    24: "United Kingdom",
    25: "USA",
    26: "World",
    27: "India",
    28: "Poland",
    29: "Portugal",
    30: "Latin America",
    31: "Belgium",
    32: "Scandinavia",
    33: "Ireland",
    34: "Israel",
    35: "Austria",
    36: "Switzerland",
    37: "South Africa",
    38: "Croatia",
    39: "Turkey",
    40: "New Zealand",
    41: "UAE",
}


#----------------------------------------------------------------#


def print_welcome():
    print(r"""
 __      ___                                _____                                
 \ \    / (_)                              / ____|                               
  \ \  / / _ _ __ ___  _ __ ___  ___ _____| (___   ___ _ __ __ _ _ __   ___ _ __ 
   \ \/ / | | '_ ` _ \| '_ ` _ \/ __|______\___ \ / __| '__/ _` | '_ \ / _ \ '__|
    \  /  | | | | | | | | | | | \__ \      ____) | (__| | | (_| | |_) |  __/ |   
     \/   |_|_| |_| |_|_| |_| |_|___/     |_____/ \___|_|  \__,_| .__/ \___|_|   
                                                                | |              
                                                                |_|              
    """)
  print(f"This is a tool for scraping VaultIDs from the ROM site vimm.net or vimm's lair")

def print_console_list():
    total = len(selections)
    half = (total + 1) // 2

    for i in range(half):
        left_idx = i
        right_idx = i + half
        left_console = selections[left_idx][left_idx]

        if right_idx < total:
            right_console = selections[right_idx][right_idx]
            print(f"{left_idx:5d} ==> {left_console:15} | {right_idx:5d} ==> {right_console:10}")
        else:
            print(f"{left_idx:5d} ==> {left_console:15}")

def prompt_select_console():
    print_console_list()
    try:
        user_input = int(input("Enter Console Number: "))

        if 0 <= user_input < len(selections):
            selected_console = get_selection_from_num(user_input)
            print(f"Selected Console: {selected_console}")
            return selected_console
        else:
            print("Invalid Number Selection")
    except ValueError:
        print("Try a Valid Integer")
    return None

def get_selection_from_num(selection: int):
    return selections[selection][selection]

def prompt_select_regions():
    print("\nSelect regions(s) by number: ")
    for code, name in region_options.items():
        print(f" {code:>2} => {name}")
    
    user_input = input("Enter region codes: ")

    separators = [",", " "]
    for sep in separators:
        if sep in user_input:
            raw_parts = user_input.split(sep)
            break
    else:
        raw_parts = [user_input]

    try:
        selected = [int(x.strip()) for x in raw_parts if x.strip().isdigit() and int(x.strip()) in region_options]
        if not selected:
            print("No valid regions selected. Defaulting to the USA and Europe")
            return [8, 25]
        print("Selected regions:", ", ".join(region_options[code] for code in selected))
        return selected
    except ValueError:
        print("Invalid input. Defaulting to the USA and Europe.")
        return [8, 25]
    


#----------------------------------------------------------------#


# Letter URLs
letter_url1 = "?p=list&action=filters&section="
letter_url2 = "&system="
letter_url3 = "&translated=1&version=new&discs="


#----------------------------------------------------------------#


def scrape_urls(selected_console, selected_regions):
    all_rom_ids.clear()

    main_url = f"{BASE_URL}/vault/{selected_console}"
    resp = requests.get(main_url, verify=False)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    region_filter = "".join(f"&countries%5B%5D={c}" for c in selected_regions)

    prefix = f"/vault/{selected_console}/"
    letter_paths = sorted({
        a['href']
        for a in soup.find_all("a", href=True)
        if a['href'].startswith(prefix) and len(a['href']) == len(prefix) + 1
    })
    print(f"Found letter sections: {letter_paths}")

    urls = []
    for path in letter_paths:
        letter = path[len(prefix):]  # e.g. "A"
        url = (
            f"{BASE_URL}/vault/"
            f"{letter_url1}{letter}"
            f"{letter_url2}{selected_console}"
            f"{region_filter}"
            f"{letter_url3}"
        )
        urls.append(url)

    num_url = (
        f"{BASE_URL}/vault/"
        f"?p=list&action=filters"
        f"&section=number"
        f"{letter_url2}{selected_console}"
        f"{region_filter}"
        f"{letter_url3}"
    )
    urls.append(num_url)

    for url in urls:
        print(f"Fetching ROMs from {url}...")
        r = requests.get(url, verify=False)
        if r.status_code == 404:
            print(f"Page {url} not found (404). Skipping.")
            continue
        r.raise_for_status()

        page = BeautifulSoup(r.text, "html.parser")
        for a_tag in page.find_all("a", href=True):
            h = a_tag['href']
            if h.startswith("/vault/") and h[7:].isdigit():
                all_rom_ids.add(h[7:])

    print(f"Total unique ROM IDs found: {len(all_rom_ids)}")
    print(all_rom_ids)


#----------------------------------------------------------------#


print_welcome()
selected_console = prompt_select_console()

if selected_console:
    selected_regions = prompt_select_regions()
    scrape_urls(selected_console, selected_regions)
else:
    print("No console selected. Exiting...")
