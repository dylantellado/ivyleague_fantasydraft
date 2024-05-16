import requests
from bs4 import BeautifulSoup
from cs50 import SQL

school_dict = {'Harvard': [17, 24], 'Yale': [20,20], 'Brown': [18, 20], 'Cornell':[15,16],"Penn": [16,12], 'Princeton':[15,31],'Dartmouth':[15,25],'Columbia':[14,22]}

def calculate_player_value(games_played, games_started, goals, assists, team_games, goals_against, position):
    games_played_ratio = int(games_played) / int(team_games)
    if games_played > 3:
        games_started_ratio = games_started/games_played
    else:
        games_started_ratio = games_started/team_games
    goals_ratio = goals/5
    if goals_ratio > 1:
        goals_ratio = 1
    assists_ratio = assists/5
    if assists_ratio > 1:
        assists_ratio = 1
    goals_against_ratio = 1/goals_against

    if position == 'F':
        # Define weights for each factor

        weight_games_played = 10
        weight_games_started = 15
        weight_goals = 15
        weight_assists = 5

        # Calculate the weighted sum
        value = (
            weight_games_played * games_played_ratio +
            weight_games_started * games_started_ratio +
            weight_goals * goals_ratio +
            weight_assists * assists_ratio
        )
    elif position == 'M':
        weight_games_played = 10
        weight_games_started = 15
        weight_goals = 10
        weight_assists = 10

        value = (
            weight_games_played * games_played_ratio +
            weight_games_started * games_started_ratio +
            weight_goals * goals_ratio +
            weight_assists * assists_ratio
        )

    elif position == 'D':
        weight_games_played = 10
        weight_games_started = 17.5
        weight_goals_against = 10
        weight_goals = 5
        weight_assists = 2.5

        value = (
            weight_games_played * games_played_ratio +
            weight_games_started * games_started_ratio +
            weight_goals * goals_ratio +
            weight_assists * assists_ratio +
            weight_goals_against * goals_against_ratio
        )

    else:
        weight_games_played = 10
        weight_games_started = 20
        weight_goals_against = 15

        value = (
            weight_games_played * games_played_ratio +
            weight_games_started * games_started_ratio +
            weight_goals_against * goals_against_ratio

        )


    return value

db = SQL("sqlite:///players.db")
players ={'Kojo Dadzie':[17,17,7,0],'Charlie Adams':[18,14,3,1],'Carlo Brown':[16,7,2,3],'Levi Pillar':[18,9,2,2],'Tanner Barry':[18,17,0,4],
                  'Harri Sprofera':[18,14,1,2],'Scott Gustafson':[18,12,1,1],'Cal Walsh':[13,2,1,1],'Lorenzo Amaral':[17,12,0,2],'Dylan Ellis':[10,0,1,0],'Heechan Han':[7,6,1,0],
                  'Adolfo Diaz':[3,0,0,1],'Jamin Gogo Peters':[16,5,0,1],'Langdon Gryglas':[16,15,0,1],'Greyson Mitchell':[16,13,0,1],'Keegan Walpole':[3,0,0,1],'Noah Atanda':[11,3,0,0],
                  'Mike Balleani':[4,0,0,0],'Hudson Blatteis':[11,10,0,0],'Jack Cloherty':[15,14,0,0],'Iyke Dafe':[10,0,0,0],'Diego Elizalde':[6,1,0,0],'Kyle Gee':[14,7,0,0],'Gavin Tabije':[8,0,0,0],
                  'Shayne Thompson':[1,0,0,0],'Henrik Weiper':[8,8,0,0],'Zion Wharton':[6,0,0,0]}
player_points={}
for player in players:
    position = db.execute("SELECT position FROM players WHERE p_name = ?", player)
    position = position[0]["position"]
    college = db.execute("SELECT college FROM players WHERE p_name = ?", player)
    college = college[0]["college"]
    points = round(55 + calculate_player_value(players[player][0],players[player][1],players[player][2],players[player][3], school_dict[college][0], school_dict[college][1], position))
    if points > 99:
        points = 99
    player_points[player] = points
print(player_points)
