import csv
from roster import Position, Roster


def draft_player_espn(eligible_players, espn_roster, taken_players):
    drafted_player = ""
    drafted_position = Position.NONE
    with open("Player Stats NFL - ESPN 2025 ADP.csv", mode='r') as file:
        csv_reader = csv.DictReader(file)
        espn_data = []
        for row in csv_reader:
            espn_data.append(row)

    #this data is presorted in the csv rendering sorting unnecessary here
    for player in espn_data:
        drafted_player = player["Player Name"]
        drafted_position = Position.from_str(player["Position"])
        if drafted_player not in espn_roster.getPlayerList() and drafted_player not in taken_players and (espn_roster.getPosNumber(drafted_position) + 1 <= Roster.getMaxPosition(drafted_position)):
            
            break
    return drafted_player, drafted_position