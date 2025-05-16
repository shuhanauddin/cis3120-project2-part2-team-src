import requests
from bs4 import BeautifulSoup
import pandas as pd

urls = {
    "mens_swimming": [
        ("https://csidolphins.com/sports/mens-swimming-and-diving/roster", "College of Staten Island"),
        ("https://yorkathletics.com/sports/mens-swimming-and-diving/roster", "York College"),
        ("https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster", "Baruch College"),
        ("https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster", "Brooklyn College"),
        ("https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster", "Lindenwood University"),
        ("https://mckbearcats.com/sports/mens-swimming-and-diving/roster", "McKendree University"),
        ("https://ramapoathletics.com/sports/mens-swimming-and-diving/roster", "Ramapo College"),
        ("https://oneontaathletics.com/sports/mens-swimming-and-diving/roster", "SUNY Oneonta"),
        ("https://bubearcats.com/sports/mens-swimming-and-diving/roster/2021-22", "SUNY Binghamton"),
        ("https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22", "Albright College")
    ],
    "womens_swimming": [
        ("https://csidolphins.com/sports/womens-swimming-and-diving/roster", "College of Staten Island"),
        ("https://queensknights.com/sports/womens-swimming-and-diving/roster", "Queens College"),
        ("https://yorkathletics.com/sports/womens-swimming-and-diving/roster", "York College"),
        ("https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?path=wswim", "Baruch College"),
        ("https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster", "Brooklyn College"),
        ("https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster", "Lindenwood University"),
        ("https://mckbearcats.com/sports/womens-swimming-and-diving/roster", "McKendree University"),
        ("https://ramapoathletics.com/sports/womens-swimming-and-diving/roster", "Ramapo College"),
        ("https://keanathletics.com/sports/womens-swimming-and-diving/roster", "Kean University"),
        ("https://oneontaathletics.com/sports/womens-swimming-and-diving/roster", "SUNY Oneonta")
    ],
    "mens_volleyball": [
        ("https://ccnyathletics.com/sports/mens-volleyball/roster", "CCNY"),
        ("https://lehmanathletics.com/sports/mens-volleyball/roster", "Lehman College"),
        ("https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster", "Brooklyn College"),
        ("https://johnjayathletics.com/sports/mens-volleyball/roster", "John Jay College"),
        ("https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster", "Baruch College"),
        ("https://mecathletics.com/sports/mens-volleyball/roster", "Medgar Evers College"),
        ("https://www.huntercollegeathletics.com/sports/mens-volleyball/roster", "Hunter College"),
        ("https://yorkathletics.com/sports/mens-volleyball/roster", "York College"),
        ("https://ballstatesports.com/sports/mens-volleyball/roster", "Ball State")
    ],
    "womens_volleyball": [
        ("https://bmccathletics.com/sports/womens-volleyball/roster", "BMCC"),
        ("https://yorkathletics.com/sports/womens-volleyball/roster", "York College"),
        ("https://hostosathletics.com/sports/womens-volleyball/roster", "Hostos CC"),
        ("https://bronxbroncos.com/sports/womens-volleyball/roster/2021", "Bronx CC"),
        ("https://queensknights.com/sports/womens-volleyball/roster", "Queens College"),
        ("https://augustajags.com/sports/wvball/roster", "Augusta University"),
        ("https://flaglerathletics.com/sports/womens-volleyball/roster", "Flagler College"),
        ("https://pacersports.com/sports/womens-volleyball/roster", "USC Aiken"),
        ("https://www.golhu.com/sports/womens-volleyball/roster", "Penn State Lock Haven")
    ]
}

def convert_height(height_str):
    try:
        if '-' in height_str or "'" in height_str:
            ft, inch = height_str.strip().split('-')
            return int(ft) * 12 + int(inch)
    except:
        return None
    return None

def scrape_roster(url, school):
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return pd.DataFrame()
        soup = BeautifulSoup(res.content, 'html.parser')
        name_tags = soup.find_all('td', class_='sidearm-table-player-name')
        height_tags = soup.find_all('td', class_='height')
        names = [n.get_text(strip=True) for n in name_tags]
        heights = []
        for h in height_tags:
            raw = h.get_text(strip=True)
            heights.append(convert_height(raw))
        return pd.DataFrame({'Name': names[:len(heights)], 'Height (in.)': heights, 'School': school})
    except Exception as e:
        print(f"Error scraping {url} for {school}: {e}")
        return pd.DataFrame()

for category, school_list in urls.items():
    all_data = pd.DataFrame()
    for url, school in school_list:
        df = scrape_roster(url, school)
        all_data = pd.concat([all_data, df], ignore_index=True)
    all_data.dropna(inplace=True)
    all_data.to_csv(f"{category}.csv", index=False)
    print(f"Saved {category}.csv with {len(all_data)} records. Avg Height: {round(all_data['Height'].mean(),2)} in.")

