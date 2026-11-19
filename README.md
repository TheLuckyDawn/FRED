# FRED
Football Rankings for Expert Drafting, or F.R.E.D., is a project for COMP560 that goes through and compares different heuristics/algorithms against ESPN's ADP to see if they would've performed better in the 2025 season.

## Data Used
Auto Draft Ranking data comes from ESPN, which is publicly available on their website below:
https://g.espncdn.com/s/ffldraftkit/25/NFL25_CS_PPR300.pdf?adddata=2025CS_PPR300 

Week by Week Data:
https://github.com/hvpkod/NFL-Data 

Full Compiled Season Data came from Pro Football Reference using their "Scrimmage Statistics" tab, and making it into a CSV file. The link is below for 2025:
https://www.pro-football-reference.com/years/2025/scrimmage.htm
And for 2024:
https://www.pro-football-reference.com/years/2024/scrimmage.htm

##Set Up
To replicate results shown in the presentation, you can change the "ALG_TYPE" constant in main.py to be one of the three algorithms I showed in the presentation: RANDOM, WEIGHTED_RANK, or GREEDY. Ensure that it remains the Enumerable type that is declared in FRED.py, AlgorithmType.

To run the program, you simply can run main.py, and you should see the outputs in the console similarly formatted to how they were in the presentation and on my machine.