import requests
from bs4 import BeautifulSoup
from cs50 import SQL


POTY = ['Alessandro Arlotti','TJ Presthus']
ROTY = 'Alex Harris'
creators = ['Dylan Tellado', 'Yuta Hata']
first_team = ['Leo Burney','Connor Drought','Nick Christoffersen','Connor Miller','Michael Hewes','Max Rogers','Kojo Dadzie','Daniel Ittycheria']
second_team = ['Hudson Blatteis','Michael Collodi','Chris Edwards','Jan Riecke','Wilson Eisner','Nik White','Jack Jasinski','Jack Cloherty','Trenton Blake','Nico Nee','Stas Korzeniowski','Eric Lagos','Vasilis Moiras']
honorable_mention = ['Lorenzo Amaral','Harri Sprofera','Taha Kina','Joao Lima','Kisa Kiingi','Tom Collins','Kristian Feed','Sebastian Manon','Erik Dalaker','Ethan Veghte','Ben Do','Jack Schaffer']

#dict where index 1 is # of games and index 2 is # of goals conceded
school_dict = {'Harvard': [17, 1.41,12.5], 'Yale': [20,1,9.9], 'Brown': [18, 1.11,11.6], 'Cornell':[15,1.07,6.9],"Penn": [16,0.75,10.5], 'Princeton':[15,2.07,15.5],'Dartmouth':[15,1.67,13.5],'Columbia':[14,1.57,13.7]}

def calculate_player_value(games_played, games_started, goals, assists, team_games, goals_against, position,cr,shots_conceded):
    games_played_ratio = int(games_played) / int(team_games)
    if games_played > 3:
        games_started_ratio = games_started/games_played
    else:
        games_started_ratio = games_started/team_games
    # Goals ratio
    goals_ratio = goals/5
    if goals_ratio > 1:
        goals_ratio = 1
    # Assists ratio
    assists_ratio = assists/5
    if assists_ratio > 1:
        assists_ratio = 1
    # Goals against ratio
    goals_against_ratio = 1/goals_against
    if goals_against_ratio > 1:
        goals_against_ratio = 1
    #Conversion rate ratio
    cr = float(cr) * 3.5
    if cr > 1:
        cr = 1

    shots_against_ratio = 5/shots_conceded

    if position == 'F':
        # Define weights for each factor

        weight_games_played = 9
        weight_games_started = 8
        weight_goals = 15
        weight_assists = 3
        weight_cr = 5

        # Calculate the weighted sum
        value = (
            weight_games_played * games_played_ratio +
            weight_games_started * games_started_ratio +
            weight_goals * goals_ratio +
            weight_assists * assists_ratio +
            weight_cr * cr
        )
    elif position == 'M':
        weight_games_played = 10
        weight_games_started = 9
        goals_ratio = max(goals_ratio, assists_ratio)
        assists_ratio = goals_ratio
        weight_goals = 8
        weight_assists = 8


        value = (
            weight_games_played * games_played_ratio +
            weight_games_started * games_started_ratio +
            weight_goals * goals_ratio +
            weight_assists * assists_ratio
        )

    elif position == 'D':
        weight_games_played = 9
        weight_games_started = 12.5
        weight_goals_against = 8
        weight_shots_conceded = 5
        weight_goals = 3
        weight_assists = 3

        value = (
            weight_games_played * games_played_ratio +
            weight_games_started * games_started_ratio +
            weight_goals * goals_ratio +
            weight_assists * assists_ratio +
            weight_goals_against * goals_against_ratio +
            weight_shots_conceded * shots_against_ratio
        )

    else:
        weight_games_played = 7.5
        weight_games_started = 12.5
        weight_goals_against = 18

        value = (
            weight_games_played * games_played_ratio +
            weight_games_started * games_started_ratio +
            weight_goals_against * goals_against_ratio

        )


    return value


url_list = ['https://gocrimson.com/sports/mens-soccer/stats', 'https://yalebulldogs.com/sports/mens-soccer/stats', 'https://cornellbigred.com/sports/mens-soccer/stats/2023','https://pennathletics.com/sports/mens-soccer/stats/2023','https://dartmouthsports.com/sports/mens-soccer/stats', 'https://gocolumbialions.com/sports/mens-soccer/stats', 'https://goprincetontigers.com/sports/mens-soccer/stats/2023', 'https://brownbears.com/sports/mens-soccer/stats/2023']
url_list_xml = ['https://gocrimson.com/sports/mens-soccer/stats', 'https://yalebulldogs.com/sports/mens-soccer/stats', 'https://cornellbigred.com/sports/mens-soccer/stats/2023','https://pennathletics.com/sports/mens-soccer/stats/2023','https://dartmouthsports.com/sports/mens-soccer/stats', 'https://gocolumbialions.com/sports/mens-soccer/stats']
for url in url_list:
    if url in url_list_xml:
        formatted_names = []
        response = requests.get(url)
        db = SQL("sqlite:///players.db")

        soup = BeautifulSoup(response.text, 'html.parser')

        names= soup.find_all('a',class_='hide-on-medium-down')

        played = soup.find_all('td',{'data-label':'GP'})
        started = soup.find_all('td',{'data-label':'GS'})
        goals = soup.find_all('td',{'data-label':'G'})
        assists = soup.find_all('td',{'data-label':'A'})
        game_winners = soup.find_all('td',{'data-label':'GW'})
        conversion_rate = soup.find_all('td',{'data-label':'SH%'})


        names_list=[]
        for name in names:
            if not name.get_text(strip=True) in names_list:
                names_list.append(name.get_text(strip=True))



        for name in names_list:
            parts = name.split(', ')
            if not f'{parts[1]} {parts[0]}' in formatted_names:
                formatted_names.append(f'{parts[1]} {parts[0]}'.rstrip())
        player_points = {}

    for i in range(len(formatted_names)):
        gp = int(played[i].get_text(strip=True))
        gs = int(started[i].get_text(strip=True))
        goal = int(goals[i].get_text(strip=True))
        assist = int(assists[i].get_text(strip=True))
        gw = int(game_winners[i].get_text(strip=True))
        cr=conversion_rate[i].get_text(strip=True)
        position = db.execute("SELECT position FROM players WHERE p_name = ?", formatted_names[i])
        college = db.execute("SELECT college FROM players WHERE p_name = ?", formatted_names[i])
        position = position[0]["position"]
        college = college[0]["college"]
        points = round(55 + calculate_player_value(gp,gs,goal,assist, school_dict[college][0], school_dict[college][1], position,cr,school_dict[college][2]))
        points += gw
        if formatted_names[i]==ROTY:
            points = 97
        elif formatted_names[i] in POTY:
            points += 5
        elif formatted_names[i] in first_team:
            points += 3
        elif formatted_names[i] in second_team:
            points += 2
        elif formatted_names[i] in honorable_mention:
            points += 1
        elif formatted_names[i] in creators:
            points = 99
        if points > 99:
            points = 99
        player_points[formatted_names[i]] = points
        db.execute("INSERT INTO playerpoints (name, points) VALUES (:name, :points)", name = formatted_names[i], points = points,)
    if url == 'https://goprincetontigers.com/sports/mens-soccer/stats/2023':
        players = {'Daniel Ittycheria':[15,14,9,1,1,0.225],'Nico Nee':[15,14,3,5,1,0.091],'Will Francis':[14,8,4,1,1,0.364],'Walker Gillespie':[12,9,3,2,0,0.167],'Ian Nunez':[12,0,2,0,1,0.167],'Jack Jasinski':[15,15,0,3],
                'Ryan Winkler':[15,6,0,3],'Stephen Duncan':[14,13,1,0,0,0.5],'Whit Gamblin':[14,13,0,10],'Kevin Kelley':[14,5,0,10],'Logan Oyama':[12,2,0,1],'Sam Vigilante':[15,11,0,1],
                'Giuliano Fravolini Whitchurch':[9,9,0,1],'Francis Akomeah':[13,8,0,0],'Liam Beckwith':[15,12,0,0],'Heyward Bryan':[1,0,0,0],'Gabriel Duchovny':[11,3,0,0],
                'Spencer Fleurant':[2,0,0,0],'Khamari Hadaway':[10,10,0,0],'Bardia Hormozi':[14,3,0,0],'Jack Hunt':[11,0,0,0],'Ian MacIver':[2,0,0,0],
                'Issa Mudashiru':[9,2,0,0],'Harry Roberts':[11,3,0,0],'Sebastian Swary':[4,0,0,0],'Will Travis':[1,0,0,0],'James Wangsness':[2,0,0,0],'William Watson':[5,5,0,0]}
        player_points={}
        for player in players:
            position = db.execute("SELECT position FROM players WHERE p_name = ?", player)
            position = position[0]["position"]
            college = db.execute("SELECT college FROM players WHERE p_name = ?", player)
            college = college[0]["college"]
            gw=0
            cr=0.0
            if len(players[player]) ==6:
                gw=players[player][4]
                cr=players[player][5]
            points = round(55 + calculate_player_value(players[player][0],players[player][1],players[player][2],players[player][3], school_dict[college][0], school_dict[college][1], position,cr,school_dict[college][2]))
            points+=gw
            if formatted_names[i]==ROTY:
                points +=2
            elif formatted_names[i] in POTY:
                points += 5
            elif formatted_names[i] in first_team:
                points += 3
            elif formatted_names[i] in second_team:
                points += 2
            elif formatted_names[i] in honorable_mention:
                points += 1
            if points > 99:
                points = 99
            player_points[player] = points
            db.execute("INSERT INTO playerpoints (name, points) VALUES (:name, :points)", name = player, points = points,)
    if url == 'https://brownbears.com/sports/mens-soccer/stats/2023':
        players ={'Kojo Dadzie':[17,17,7,0,3,0.171],'Charlie Adams':[18,14,3,1,1,0.15],'Carlo Brown':[16,7,2,3,0,0.2],'Levi Pillar':[18,9,2,2,0,0.33],'Tanner Barry':[18,17,0,4],
                  'Harri Sprofera':[18,14,1,2,0,0.33],'Scott Gustafson':[18,12,1,1,0,0.125],'Cal Walsh':[13,2,1,1,0,0.2],'Lorenzo Amaral':[17,12,0,2],'Dylan Ellis':[10,0,1,0,1,0.33],'Heechan Han':[7,6,1,0,0,0.5],
                  'Adolfo Diaz':[3,0,0,1],'Jamin Gogo Peters':[16,5,0,1],'Langdon Gryglas':[16,15,0,1],'Greyson Mitchell':[16,13,0,1],'Keegan Walpole':[3,0,0,1],'Noah Atanda':[11,3,0,0],
                  'Mike Balleani':[4,0,0,0],'Hudson Blatteis':[11,10,0,0],'Jack Cloherty':[15,14,0,0],'Iyke Dafe':[10,0,0,0],'Diego Elizalde':[6,1,0,0],'Kyle Gee':[14,7,0,0],'Gavin Tabije':[8,0,0,0],
                  'Shayne Thompson':[1,0,0,0],'Henrik Weiper':[8,8,0,0],'Zion Wharton':[6,0,0,0]}
        player_points={}
        for player in players:
            position = db.execute("SELECT position FROM players WHERE p_name = ?", player)
            position = position[0]["position"]
            college = db.execute("SELECT college FROM players WHERE p_name = ?", player)
            college = college[0]["college"]
            gw=0
            cr=0.0
            if len(players[player]) == 6:
                gw=players[player][4]
                cr=players[player][5]
            points = round(55 + calculate_player_value(players[player][0],players[player][1],players[player][2],players[player][3], school_dict[college][0], school_dict[college][1], position,cr,school_dict[college][2]))
            points += gw
            if formatted_names[i]==ROTY:
                points +=2
            elif formatted_names[i] in POTY:
                points += 5
            elif formatted_names[i] in first_team:
                points += 3
            elif formatted_names[i] in second_team:
                points += 2
            elif formatted_names[i] in honorable_mention:
                points += 1
            if points > 99:
                points = 99
            player_points[player] = points
            db.execute("INSERT INTO playerpoints (name, points) VALUES (:name, :points)", name = player, points = points,)




