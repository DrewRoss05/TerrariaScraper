import requests
import json

from bs4 import BeautifulSoup, Tag

# returns the text of an HTML element
def get_text(element: Tag):
    return element.text

# removes leading and trailing spaces from a piece of text
def strip_text(text: str):
    return text.strip()

# returns a dictonary of a given weapon's stats
def search_weapon(weapon: str) -> dict:
    r = requests.get(f"https://terraria.fandom.com/wiki/{weapon.replace(' ', '_').title()}")
    if r.status_code != 200: 
        raise ValueError(f"Data couldn't be scraped. HTTP Status Code: {r.status_code}")
    parser = BeautifulSoup(r.text, "html.parser")
    # get stat names and stats from the infobox
    item_info = parser.find("div", {"class": "infobox item"})
    # create a dictionary of stats
    names =  list(map(get_text, item_info.find_all("th")))
    stats = list(map(get_text, item_info.find_all("td")))
    stat_dict = {}
    for i in range(len(names)):
        stat_dict[names[i]] = stats[i]
    # associate the rarity value with the correpsonding text color
    stat_dict['Rarity'] = {"01*": "White", "02*": "Blue", "03*": "Green", "04*": "Orange", "05*": "Light Red",
                           "06*": "Pink", "07*": "Light Purple", "08*": "Lime", "09*": "Yellow", "10*": "Cyan", 
                           "11*": "Red", "12*": "Purple"}[stat_dict["Rarity"]]
    # remove (largely) uselss stats
    del stat_dict['Use'], stat_dict['Type'], stat_dict['']
    return stat_dict

def create_json(file_name: str, items: tuple):
    item_dict = {}
    for i in items:
        try:
            item_dict[i] = search_weapon(i)
        except ValueError:
            item_dict[i] = "N/A"
    with open(file_name, 'w') as f:
        json.dump(item_dict, f)


weapons = input("What weapon(s) would you like to search for (seperate all weapon names with a comma)")
weapon_list = map(strip_text, weapons.split(","))
use_json = input("Would you like to save the search(es) to a JSON file? (Y/N)")
while use_json.lower() not in ("y", "n"):
    use_json = input("Would you like to save the search(es) to a JSON file? (Y/N)")
if use_json == "y":
    file_name = input("What would you like to name the JSON file?")
    create_json(file_name, weapon_list)
else:
    for i in weapon_list:
        try:
            print(f"{i}: {search_weapon(i)}")
        except ValueError:
            print(f"{i}: N/A")
