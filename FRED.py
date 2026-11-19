from roster import Roster, Position
from espn_drafter import draft_player_espn
from simulate_scoring import simulate_week
import csv
import random
import numpy as np
from enum import Enum

class AlgorithmType(Enum):
    GREEDY = 2
    RANDOM = 1
    WEIGHTED_RANK = 3
    TRAIN = 4
    PREDETERMINED_WEIGHTS = 5

def draft_player_fred(eligible_players, fred_roster: Roster, taken_players, algorithm, weights=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], bias=0.0, mean=[], std=[]):
    drafted_player = ""
    drafted_position = Position.NONE
    with open("Player Stats NFL - 2024 Season No Duplicates.csv", mode='r') as file:
        csv_reader = csv.DictReader(file)
        fred_data = []
        rows = list(csv_reader)

        for row in csv_reader:
            fred_data.append(row)

    #random drafting
    if algorithm == AlgorithmType.RANDOM:
        while(True):
            random_player = random.choice(fred_data)
            drafted_player = random_player["Player"]
            drafted_position = Position.from_str(random_player["Pos"])
            
            if drafted_player not in fred_roster.getPlayerList() and drafted_player not in taken_players and (fred_roster.getPosNumber(drafted_position) + 1 <= Roster.getMaxPosition(drafted_position)) and drafted_player in eligible_players:
                break
    
    else:
        if algorithm == AlgorithmType.GREEDY:               
            rows.sort(key=lambda row: int(row["Total TD"]), reverse=True)

            for row in rows:
                drafted_player = row["Player"]
                drafted_position = Position.from_str(row["Pos"])
                if drafted_player not in fred_roster.getPlayerList() and drafted_player not in taken_players and (fred_roster.getPosNumber(drafted_position) + 1 <= Roster.getMaxPosition(drafted_position)) and drafted_player in eligible_players:
                    break

        if algorithm == AlgorithmType.WEIGHTED_RANK:
            rows.sort(key=lambda row: int(row["Total TD"]), reverse=True)
            rank = 1
            for row in rows:
                row["td rank"] = rank
                rank += 1
            rows.sort(key=lambda row: int(row["YScm"]), reverse=True)
            rank = 1
            for row in rows:
                row["yd rank"] = rank
                rank += 1
            current_drafted_player = ""
            current_drafted_position = Position.NONE
            current_drafted_score = 999999999999
            for row in rows:
                current_drafted_player = row["Player"]
                current_drafted_position = Position.from_str(row["Pos"])
                if current_drafted_player not in fred_roster.getPlayerList() and current_drafted_player not in taken_players and (fred_roster.getPosNumber(current_drafted_position) + 1 <= Roster.getMaxPosition(current_drafted_position)) and current_drafted_player in eligible_players:
                    #the weights here can be changed for some effect on scoring
                    drafted_score = float(int(row["td rank"])) * 0.5 + float(int(row["yd rank"])) * 0.5
                    if drafted_score < current_drafted_score:
                        current_drafted_score = drafted_score
                        drafted_player = current_drafted_player
                        drafted_position = current_drafted_position

        if algorithm == AlgorithmType.PREDETERMINED_WEIGHTS:
            current_drafted_player = ""
            current_drafted_position = Position.NONE
            current_drafted_score = -99999
            for row in rows:
                current_drafted_player = row["Player"]
                current_drafted_position = Position.from_str(row["Pos"])
                inputs = [np.array([float(row["Age"]), float(row["Games"]), float(row["Started"]), float(row["Tgt"]), float(row["Rec"]), float(row["Rec Yds"]), float(row["Y/R"]), float(row["Rec TD"]), float(row["1D Rec"]), float(row["Rec Succ%"]), float(row["Lng Rec"]), float(row["R/G"]), float(row["Y/G"]), float(row["Y/Tgt"]), float(row["Att"]), float(row["Rsh Yds"]), float(row["Rsh TD"]), float(row["1D Rsh"]), float(row["Rsh Succ%"]), float(row["Lng Rsh"]), float(row["Y/A"]), float(row["Y/G"]), float(row["A/G"]), float(row["Touch"]), float(row["Y/Tch"]), float(row["YScm"]), float(row["Total TD"]), float(row["Fmb"])])]
                predicted_score = 0

                #normalize the inputs so yardage doesn't overblow the size of the numbers (I was getting a lot of overflow errors before doing this)
                #trained on normalized, gets normalized now using training values
                inputs = np.array(inputs)
                inputs = (inputs - mean) / std

                for i in range(28):
                    predicted_score += inputs[0][i]*weights[i]
                predicted_score += bias
                if current_drafted_player not in fred_roster.getPlayerList() and current_drafted_player not in taken_players and (fred_roster.getPosNumber(current_drafted_position) + 1 <= Roster.getMaxPosition(current_drafted_position)) and current_drafted_player in eligible_players:
                    if predicted_score > current_drafted_score:
                        current_drafted_score = predicted_score
                        drafted_player = current_drafted_player
                        drafted_position = current_drafted_position

        if algorithm == AlgorithmType.TRAIN:
            train_weights = np.random.randn(28)
            train_bias = 0.0
            learn_rate = 0.001

            max_ticks = 30000
            TRAINING_DATA = ["Bijan Robinson","Christian McCaffrey","Jonathan Taylor","James Cook","Jahmyr Gibbs","De'Von Achane","Jaxon Smith-Njigba","Puka Nacua","Derrick Henry","Kyren Williams","Chase Brown","George Pickens","Ja'Marr Chase","Breece Hall","Saquon Barkley","Amon-Ra St. Brown","Travis Etienne","D'Andre Swift","Rico Dowdle","Javonte Williams","Kenneth Walker III","Jaylen Warren","Tony Pollard","Zay Flowers","Josh Jacobs","Chris Olave","Nico Collins","Jameson Williams","CeeDee Lamb","Justin Jefferson","Tyrone Tracy Jr.","Kenneth Gainwell","Wan'Dale Robinson","Courtland Sutton","Stefon Diggs","DeVonta Smith","Michael Wilson","A.J. Brown","Alec Pierce","Rhamondre Stevenson","Jaylen Waddle","Drake London","David Montgomery","Zach Charbonnet","Bucky Irving","D.K. Metcalf","Jakobi Meyers","Parker Washington","Tee Higgins","J.K. Dobbins","Jordan Mason","Deebo Samuel","Rachaad White","Davante Adams","Ladd McConkey","Michael Pittman Jr.","Blake Corum","Kimani Vidal","Keenan Allen","D.J. Moore","Rashid Shaheed","Kareem Hunt","Aaron Jones","Tre Tucker","Quentin Johnston","Chuba Hubbard","Brian Thomas","Romeo Doubs","Khalil Shakir","Troy Franklin","Jordan Addison","Rome Odunze","Alvin Kamara","Jauan Jennings","Cam Skattebo","Christian Watson","Tyler Allgeier","Marvin Harrison Jr.","Jerry Jeudy","Michael Carter","Emanuel Wilson","Cooper Kupp","Rashee Rice","Devin Singletary","Marquise Brown","Terry McLaurin","Nick Chubb","Josh Downs","Isiah Pacheco","Mack Hollins","Kendrick Bourne","Kayshon Boutte","Tyjae Spears","Darius Slayton","Chris Rodriguez","Ricky Pearsall","Ryan Flournoy","KaVontae Turpin","Samaje Perine","DeMario Douglas","Ty Johnson","Jalen Nailor","Xavier Hutchinson","Andrei Iosivas","Darnell Mooney","Chimere Dike","Tyquan Thornton","Zonovan Knight","Malik Washington","Brian Robinson Jr.","Isaiah Davis","Jeremy McNichols","Emari Demercado","Keon Coleman","Keaton Mitchell","Marvin Mims","Garrett Wilson","Jalen Coker","Sterling Shepard","Tank Bigsby","Calvin Austin III","Mike Evans","Xavier Legette","Ray Davis","Chris Godwin","Sean Tucker","Van Jefferson","JuJu Smith-Schuster","Tez Johnson","Dontayvion Wicks","Olamide Zaccheaus","DeAndre Hopkins","Devin Neal","Kalif Raymond","Josh Palmer","Calvin Ridley","Xavier Smith","Devaughn Vele","Tyler Lockett","Demarcus Robinson","Brandin Cooks","Malik Nabers","Cedric Tillman","John Metchie","Malik Davis","Tyreek Hill","Jahan Dotson","Justice Hill","Dyami Brown","Tyrell Shavers","Christian Kirk","Jayden Reed","Jaylin Lane","Jawhar Jordan","Isaiah Williams","Rashod Bateman","Jack Bech","Trey Benson","Kendre Miller","Greg Dortch","Chris Moore","Jaleel McLaughlin","Zavier Scott","Kyle Williams","Malachi Corley","Luke McCaffrey","Jalen Tolbert","Chris Brooks","Tyler Johnson","Tutu Atwell","David Sills V","Tim Patrick","Adam Thielen","Zay Jones","Jordan Whittington","Hunter Luepke","Jalen McMillan","Jimmy Horn","Jerome Ford","Raheem Mostert","Jaret Patterson","Roman Wilson","Tyler Badie","Tory Horton","Brycen Tremayne","Ameer Abdullah","Lil'Jordan Humphrey","Ashton Dulin","Miles Sanders","Gunner Olszewski","Bo Melton","Kevin Austin","Theo Wease","Elijah Moore","Devontez Walker","Dont'e Thornton","James Conner","Treylon Burks","Gabe Davis","Dante Pettis","Marquez Valdes-Scantling","Mitchell Tinsley","Isaiah Hodgins","Savion Williams","Raheim Sanders","Antonio Gibson","Jamari Thrash","Will Shipley","Dare Ogunbowale","Josh Reynolds","Skyy Moore","Mason Tipton","Casey Washington","Rasheen Ali","Darius Cooper","Konata Mumpfield","Trayveon Williams","Cody White","Hunter Renfrow","Nick Westbrook-Ikhine","George Holani","Jahdae Walker","Najee Harris","Malik Heath","Noah Brown","Terrell Jennings","AJ Dillon","Austin Ekeler","Curtis Samuel","British Brooks","Kameron Johnson","Efton Chism III","Gage Larvadain","Corey Kiner","Allen Lazard","Ben Skowronek","Ray-Ray McCloud","Xavier Weaver","James Proche","D'Wayne Eskridge","Scotty Miller","Nathan Carter","Hassan Haskins","Shedrick Jackson","Ty Chandler","Khalil Herbert","Zamir White","Tahj Brooks","Evan Hull","Robbie Chosen","Jalen Brooks","KeAndre Lambert-Smith","Michael Bandy","Kene Nwangwu","Mason Kinsey","Dareke Young","Ronnie Rivers","Austin Trammell","Tylan Wallace","Cedrick Wilson Jr.","Dylan Drummond","Xavier Restrepo","Julius Chestnut","Braxton Berrios","Brittain Brown","Tahj Washington","Tom Kennedy","Dameon Pierce","Jalin Hyatt","Ryan Miller","Tyler Goodson","Velus Jones Jr.","Nikko Remigio","Deven Thompkins","KhaDarel Hodge","Justin Watson","Phil Mafah","Dylan Laube","Devin Duvernay","Jordan Watkins","Beaux Collins","Tai Felton","D'Ernest Johnson","Jacoby Jones","Jonathan Mingo","Ronnie Bell","Tay Martin","Clyde Edwards-Helaire","DeeJay Dallas","Cody Ford","Trent Sherfield","Jake Bobo","Britain Covey","Jared Wayne","Jacardia Wright","Cam Akers","Roschon Johnson","David Moore","Derius Davis","Tim Jones","Jakobie Keeney-James","Ke'Shawn Williams","Alex Bachman","Jacob Saylors","Josh Williams","Quentin Skinner","Andre Baccellia","Amar Johnson","Bryce Oliver","Kalel Mullings","Myles Gaskin","Xavier Gipson","Anthony Gould","Owen Wright","Craig Reynolds","Jalen Royals","Sione Vaki","Samori Toure","Kendall Milton","Malik Cunningham","Ulysses Bentley","Jason Brownlee","Mecole Hardman","Charlie Jones","Elijah Mitchell","Coleman Owen","Steven Sims","Malik Turner","Nyheim Hines","Travis Homer"]
            target_fantasy_points_array = []
            #training on four different players
            inputs = []
            for i in range(15):
                training_choice = random.choice(TRAINING_DATA)
                with open("Player Stats NFL - 2025 Season Training Data.csv", 'r') as training_file:
                    csv_reader = csv.DictReader(training_file)
                    rows = list(csv_reader)

                    training_stats = []
                    target_fantasy_points = 0
                    for row in rows:
                        if row["Player"] == training_choice:
                            training_stats = row
                            target_fantasy_points += float(int(row["Total TD"]))*6
                            target_fantasy_points += float(row["YScm"])*0.1
                            target_fantasy_points += float(int(row["Fmb"]))*-2
                            target_fantasy_points += float(int(row["Rec"]))
                            break
                    target_fantasy_points_array.append(target_fantasy_points)

                for row in rows:
                    if row["Player"] == training_choice:
                        inputs.append(np.array([float(row["Age"]), float(row["Games"]), float(row["Started"]), float(row["Tgt"]), float(row["Rec"]), float(row["Rec Yds"]), float(row["Y/R"]), float(row["Rec TD"]), float(row["1D Rec"]), float(row["Rec Succ%"]), float(row["Lng Rec"]), float(row["R/G"]), float(row["Y/G"]), float(row["Y/Tgt"]), float(row["Att"]), float(row["Rsh Yds"]), float(row["Rsh TD"]), float(row["1D Rsh"]), float(row["Rsh Succ%"]), float(row["Lng Rsh"]), float(row["Y/A"]), float(row["Y/G"]), float(row["A/G"]), float(row["Touch"]), float(row["Y/Tch"]), float(row["YScm"]), float(row["Total TD"]), float(row["Fmb"])]))
                        break

            #normalize the inputs so yardage doesn't overblow the size of the numbers (I was getting a lot of overflow errors before doing this)
            mean_train = np.mean(inputs, axis=0)
            std_train = np.std(inputs, axis=0)

            std_train[std_train == 0] = 1  # Avoid division by zero

            inputs = (inputs - mean_train) / std_train
            target_fantasy_points_array = np.array(target_fantasy_points_array)
            #gradient descent
            for tick in range(max_ticks):
                #new trick I learned with the @ in numpy, its vector/matrix multiplication
                predictions = inputs @ train_weights + train_bias

                error = predictions - target_fantasy_points_array

                dw = np.transpose(np.atleast_2d(inputs)) @ error / len(target_fantasy_points_array)
                db = np.mean(error)

                train_weights -= learn_rate * dw
                train_bias -= learn_rate * db
            return draft_player_fred(eligible_players, fred_roster, taken_players, AlgorithmType.PREDETERMINED_WEIGHTS, weights=train_weights, bias=train_bias, mean=mean_train, std=std_train)

    return drafted_player, drafted_position