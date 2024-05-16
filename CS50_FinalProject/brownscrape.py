import requests
from bs4 import BeautifulSoup
from cs50 import SQL

url = 'https://brownbears.com/sports/mens-soccer/roster'
response = requests.get(url)
db = SQL("sqlite:///players.db")

soup = BeautifulSoup(response.text,"html.parser")

players = soup.find_all('div', class_="s-person-card s-person-card--list flex flex-col overflow-hidden rounded-[10px] border s-person-card--theme-light-theme shadow-level-1 border")

for player in players:
    name_soup = player.find("div", class_="s-person-details__personal-single-line s-text-paragraph-bold flex items-center gap-2")
    name = name_soup.find("span").get_text(strip=True)

    others_soup = player.find("div", class_="s-person-details__bio-stats s-text-details s-text-details-bold py-0.5")
    position_soup = others_soup.find_all("span", class_="s-person-details__bio-stats-item")[0]
    position = position_soup.get_text(strip = True)[8:]

    grade_soup = others_soup.find_all("span", class_="s-person-details__bio-stats-item")[1]
    grade = grade_soup.get_text(strip = True)[13:]

    if name == "Henrik Weiper":
        country = "Germany"
    else:
        country = "USA"


    school = "Brown"
    number = player.find('span', class_="s-stamp__text text-center s-text-small-bold").get_text(strip=True)

    source = player.find('source', media="(min-width:0px)")
    srcset = source.get('srcset')

    if srcset:
        # Split the srcset into a list of individual URLs
        image_urls = srcset.split(',')
        # Here, you can pick the first URL or apply other logic to choose the appropriate one
        image_url = image_urls[0].strip().split(' ')[0]  # This gets the first URL
    else:
        image_url = 'No image found'

    real_url = image_url

    #print(real_url)
    db.execute("INSERT INTO players (p_name, position, country, college, grade, number, image_url) VALUES(:name, :position, :country, :school, :grade, :number, :real_url)",
    name = name, position = position, country = country, school = school, grade = grade, number = number, real_url = real_url)
