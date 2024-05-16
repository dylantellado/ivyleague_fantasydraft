import requests
from bs4 import BeautifulSoup
from cs50 import SQL

url = 'https://yalebulldogs.com/sports/mens-soccer/roster'
response = requests.get(url)
db = SQL("sqlite:///players.db")

soup = BeautifulSoup(response.text, 'html.parser')

# Initalize the dictionary to store information about players
players_dict = {}

players = soup.find_all('li', class_='sidearm-roster-player')  # Adjust class based on actual website structure


for player in players:

    name = player.find('h2').get_text(strip=True)
    position = player.find('span', class_='text-bold').get_text(strip=True)
    country = player.find('span', class_='sidearm-roster-player-hometown').get_text(strip=True)

    if country[-1] == "." or country.count("Texas") != 0 or country.count("Ohio") != 0:
        country = "USA"
    else:
        country = country[country.find(',')+2:]

    school = "Yale"
    grade = player.find('span', class_='sidearm-roster-player-academic-year').get_text(strip=True)
    number = player.find('span', class_='sidearm-roster-player-jersey-number').get_text(strip=True)

    image_tag = player.find('img')
    if image_tag:
        # Prefer 'src' attribute, but fall back to 'data-src' if necessary
        image_url = image_tag.get('src') or image_tag.get('data-src')
    else:
        image_url = 'No image found'




    #print(image_url)
    #print(name, position, country, school, grade, number)
    db.execute("INSERT INTO players (p_name, position, country, college, grade, number, image_url) VALUES(:name, :position, :country, :school, :grade, :number, :image_url)",
    name = name, position = position, country = country, school = school, grade = grade, number = number, image_url = image_url)







