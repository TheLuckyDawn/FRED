from roster import Roster, Position
import csv

def simulate_week(roster1: Roster, roster2: Roster, week):
    roster1_score = calculate_roster_score(roster1, week)
    roster2_score = calculate_roster_score(roster2, week)
    if (roster1_score > roster2_score):
        roster1.win()
        roster2.lose()
    elif (roster1_score < roster2_score):
        roster1.lose()
        roster2.win()
    else:
        roster1.tie()
        roster2.tie()
    return roster1_score, roster2_score

def calculate_roster_score(roster: Roster, week):
    total_score = 0.0
    for player in roster.getRBs():
        total_score += calculate_player_score(player, Position.RB, week)
    for player in roster.getWRs():
        total_score += calculate_player_score(player, Position.WR, week)

    return total_score

def calculate_player_score(player, position, week):
    player_score = 0.0
    with open(f"./Week By Week Data/{week}/{position.value}.csv") as file:
        csv_reader = csv.DictReader(file)
        player_data = []
        for row in csv_reader:
            if row["PlayerName"] == player:
                player_data.append(row)
                break
        if len(player_data) == 0:
            return 0
    #standard PPR scoring
    if player_data[0]["RushingYDS"] != "":
        player_score += float(int(player_data[0]["RushingYDS"]))*0.1
    if player_data[0]["RushingTD"] != "":
        player_score += float(int(player_data[0]["RushingTD"]))*6
    if player_data[0]["ReceivingRec"] != "":
        player_score += float(int(player_data[0]["ReceivingRec"]))
    if player_data[0]["ReceivingYDS"] != "":
        player_score += float(int(player_data[0]["ReceivingYDS"]))*0.1
    if player_data[0]["ReceivingTD"] != "":
        player_score += float(int(player_data[0]["ReceivingTD"]))*6
    if player_data[0]["RetTD"] != "":
        player_score += float(int(player_data[0]["RetTD"]))*6
    if player_data[0]["FumTD"] != "":
        player_score += float(int(player_data[0]["FumTD"]))
    if player_data[0]["2PT"] != "":
        player_score += float(int(player_data[0]["2PT"]))*2
    if player_data[0]["Fum"] != "":
        player_score += float(int(player_data[0]["Fum"]))*-2
    return player_score