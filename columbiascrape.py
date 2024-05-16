import requests
from bs4 import BeautifulSoup
from cs50 import SQL

url = 'https://gocolumbialions.com/sports/mens-soccer/roster'
response = requests.get(url)
db = SQL("sqlite:///players.db")

soup = BeautifulSoup(response.text,"html.parser")

players = soup.find_all('li', class_='sidearm-roster-player')  # Adjust class based on actual website structure

for player in players:
    name = player.find('h3').get_text(strip=True)
    # Special case where player doesn't have a position
    if name == "Elijah Albino":
        continue

    position = player.find('span', class_='sidearm-roster-player-position-long-short hide-on-medium').get_text(strip=True)[0]

    if name == "Ryan Yang" or name == "Chad Baker":
        country = "Canada"
    elif name == "Joao Lima":
        country = "Brazil"
    elif name == "Cristoph Kuttner":
        country = "Czech Republic"
    else:
        country = "USA"

    school = "Columbia"
    grade = player.find('span', class_='sidearm-roster-player-academic-year').get_text(strip=True)
    number = player.find('span', class_='sidearm-roster-player-jersey-number').get_text(strip=True)

    image_tag = player.find('img')
    if image_tag:
        # Prefer 'src' attribute, but fall back to 'data-src' if necessary
        image_url = image_tag.get('src') or image_tag.get('data-src')
    else:
        image_url = 'No image found'

    real_url = "https://gocolumbialions.com" + image_url

    #print(name, position, country, school, grade, number)

    db.execute("INSERT INTO players (p_name, position, country, college, grade, number, image_url) VALUES(:name, :position, :country, :school, :grade, :number, :real_url)",
    name = name, position = position, country = country, school = school, grade = grade, number = number, real_url = real_url)
    









