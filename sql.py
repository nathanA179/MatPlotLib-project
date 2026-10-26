import sqlite3 as sql
import os
import csv
import pandas as pd
import random

# creating a connection so any created databases automatically route to my golf_stats.db file
base_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(base_dir, "data/golf_stats.db")

connection = sql.connect(database)
cursor = connection.cursor()

# opening the raw csv iterating through the first row to access the column names and creating a sql table with those columns and their types
with open("data/golf_stats.csv", "r") as fr: 
    reader = csv.reader(fr)
    columns = next(reader)
    column_definitions = []
    for column in columns:
        if column == "Player":
            column_definitions.append(f'"{column}" TEXT')
        else:
            column_definitions.append(f'"{column}" REAL')
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS golf_stats(
    {", ".join(column_definitions)})
    """)
# I creating a placeholder variable to represent the datapoints and column_name to corrospond them with the correct column 
    placeholders = ", ".join("?" for column in columns)
    column_name = ", ".join(f'"{column}"' for column in columns)
# looping through the rest of the csv and adding the values to the sql table
    for row in reader:
        cursor.execute(
          f"INSERT INTO golf_stats ({column_name}) VALUES ({placeholders})", row
        )

# querying all the players and number of wins from the table 
cursor.execute(""" 
SELECT Player, NUMBER_OF_WINS FROM golf_stats
""")
wins = cursor.fetchall()

# turning the tuple into a lsit so i can iterate over the data
cleaned =  [(i[0], int(i[1])) for i in wins]
top_5 = []

# searching through the list to see the 5 golfers with the most wins   
for i in cleaned:
    top_5.append(i)
    top_5.sort(key = lambda x: x[1], reverse = True)
    if len(top_5) > 5:
        top_5.pop()

# Narrowed down what I though was the most important data from those 5 golfers 
cursor.execute("""
    SELECT 
    Player, 
    NUMBER_OF_WINS, 
    "TOTAL_SG:PUTTING", 
    AVG_Driving_DISTANCE, 
    "UP_AND_DOWN_%", 
    "FAIRWAY_HIT_%", 
    GIR_RANK, 
    HOLE_OUTS, 
    "SG:OTT", 
    AVG_CLUB_HEAD_SPEED 
FROM golf_stats WHERE Player IN 
("Bryson DeChambeau",
"Bubba Watson", 
"Dustin Johnson",  
"Justin Thomas",  
"Brooks Koepka") 
""")
golfers = cursor.fetchall()

labels = ["Player", "NUMBER_OF_WINS", "TOTAL_SG:PUTTING", "AVG_Driving_DISTANCE", "UP_AND_DOWN_%", "FAIRWAY_HIT_%", "GIR_RANK", "HOLE_OUTS", "SG:OTT", "AVG_CLUB_HEAD_SPEED"]
# creating a pandas dataframe
df = pd.DataFrame(golfers, columns=labels)
df = df.sort_values(by = "NUMBER_OF_WINS", ascending = False)
print(df)
df.to_sql(
    "Top_Five_Golfers_2017",
    connection,
    if_exists = "replace",
    index = False
)

# adding and deleting Adam Scott from Top_Five_Golfers_2017
cursor.execute("""
INSERT INTO Top_Five_Golfers_2017 (
    Player, 
    NUMBER_OF_WINS, 
    "TOTAL_SG:PUTTING", 
    AVG_Driving_DISTANCE, 
    "UP_AND_DOWN_%", 
    "FAIRWAY_HIT_%", 
    GIR_RANK, 
    HOLE_OUTS,     
    "SG:OTT", 
    AVG_CLUB_HEAD_SPEED)
SELECT  
    Player, 
    NUMBER_OF_WINS, 
    "TOTAL_SG:PUTTING",
    AVG_Driving_DISTANCE, 
    "UP_AND_DOWN_%", 
    "FAIRWAY_HIT_%", 
    GIR_RANK, 
    HOLE_OUTS, 
    "SG:OTT", 
    AVG_CLUB_HEAD_SPEED 
FROM golf_stats WHERE Player = "Adam Scott"
""")
cursor.execute("""
DELETE FROM Top_Five_Golfers_2017 WHERE Player = "Adam Scott"
""")

# querying all the players from golf stats 
cursor.execute("""
SELECT Player from golf_stats
""")
players = cursor.fetchall()

# selecting 5 random players from golf stats 
rand_player = [random.choice(players) for i in range(0,5)]
comparison_golfers = [i[0] for i in rand_player]

# creating a new table comparison_golfers
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS comparison_golfers(
    Player TEXT, 
    NUMBER_OF_WINS REAL,
    "TOTAL_SG:PUTTING" REAL,
    AVG_Driving_DISTANCE REAL,
    "UP_AND_DOWN_%" REAL,
    "FAIRWAY_HIT_%" REAL,
    GIR_RANK REAL,
    HOLE_OUTS REAL,
    "SG:OTT" REAL
    AVG_CLUB_HEAD_SPEED REAL)
""")

# placeholers stores the golfers names for compariosn golfers 
placeholders = ", ".join("?" for golfers in comparison_golfers)

# inserting the comparison golfers datapoints into comparison_golfers 
cursor.execute (f"""
INSERT INTO comparison_golfers (
    Players, 
    NUMBER_OF_WINS, 
    "TOTAL_SG:PUTTING", 
    AVG_Driving_DISTANCE, 
    "UP_AND_DOWN_%", 
    "FAIRWAY_HIT_%", 
    GIR_RANK, 
    HOLE_OUTS, 
    "SG:OTT", 
    AVG_CLUB_HEAD_SPEED)
SELECT 
    Player, 
    NUMBER_OF_WINS, 
    "TOTAL_SG:PUTTING", 
    AVG_Driving_DISTANCE, 
    "UP_AND_DOWN_%", 
    "FAIRWAY_HIT_%", 
    GIR_RANK, 
    HOLE_OUTS, 
    "SG:OTT", 
    AVG_CLUB_HEAD_SPEED 
FROM golf_stats WHERE Player IN ({placeholders}) """, comparison_golfers)

# adding a TOTAL_3_PUTTS column
cursor.execute("""
ALTER TABLE comparison_golfers ADD COLUMN TOTAL_3_PUTTS INTEGER;
""")

# adding the comparison golfers TOTAL_3_PUTTS data into comparison_golfers 
cursor.execute("""
UPDATE comparison_golfers 
SET TOTAL_3_PUTTS = (
    SELECT golf_stats.TOTAL_3_PUTTS 
    FROM golf_stats 
    WHERE golf_stats.Player = comparison_golfers.Players
)
WHERE Players IN (
    "Adam Scott", 
    "Charl Schwartzel",
    "Chez Reavie",
    "Chris Stroud",
    "Grayson Murray")
""")

# deleting extra rows from comparison_golfers  
cursor.execute("""
DELETE FROM comparison_golfers WHERE rowid BETWEEN 6 AND 15
""")

# adding a TOTAL_3_PUTTS column to Top_Five_Golfers_2017
cursor.execute("""
ALTER TABLE Top_Five_Golfers_2017 ADD COLUMN TOTAL_3_PUTTS INTEGER;
""")

# adding the top 5 golfers TOTAL_3_PUTTS data to Top_Five_Golfers_2017
cursor.execute("""
UPDATE Top_Five_Golfers_2017 
SET TOTAL_3_PUTTS = (
    SELECT golf_stats.TOTAL_3_PUTTS 
    FROM golf_stats 
    WHERE golf_stats.Player = Top_Five_Golfers_2017.Player
)
WHERE Player IN (
    "Bryson DeChambeau",
    "Bubba Watson", 
    "Dustin Johnson",  
    "Justin Thomas",  
    "Brooks Koepka")
""")

connection.commit()
connection.close()
