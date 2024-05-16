import requests
from bs4 import BeautifulSoup
from cs50 import SQL

url = 'https://cornellbigred.com/sports/mens-soccer/roster'
response = requests.get(url)
db = SQL("sqlite:///players.db")

soup = BeautifulSoup(response.text, 'html.parser')

# Initalize the dictionary to store information about players

players = soup.find_all('li', class_='sidearm-roster-player')  # Adjust class based on actual website structure


for player in players:

    name = player.find('h3').get_text(strip=True)
    position = player.find('span', class_='sidearm-roster-player-position-long-short hide-on-medium').get_text(strip=True)
    country = ''
    if name == "Jon Snider":
        country = "Iceland"
    elif name == "Balazs Feher":
        country = "Hungary"
    elif name == "Danny Lokko":
        country = "United Kingdom"
    else:
        country = "USA"

    school = "Cornell"
    grade = player.find('span', class_='sidearm-roster-player-academic-year').get_text(strip=True)
    number = player.find('span', class_='sidearm-roster-player-jersey-number').get_text(strip=True)
    #Find image url
    image_tag = player.find('img')
    if image_tag:
        # Prefer 'src' attribute, but fall back to 'data-src' if necessary
        image_url = image_tag.get('src') or image_tag.get('data-src')
    else:
        image_url = 'No image found'

    real_url = "https://cornellbigred.com" + image_url


    #print(real_url)
    #print(name, position, country, school, grade, number)
    db.execute("INSERT INTO players (p_name, position, country, college, grade, number, image_url) VALUES(:name, :position, :country, :school, :grade, :number, :real_url)",
    name = name, position = position, country = country, school = school, grade = grade, number = number, real_url = real_url)









