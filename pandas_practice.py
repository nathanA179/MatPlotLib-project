import sqlite3 as sql
import pandas as pd
import os

# connecting the tables to this file 
base_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(base_dir, "data/golf_stats.db")

connection = sql.connect("data/golf_stats.db")
cursor = connection.cursor()

# querying all the data from Top_Five_golfers_2017
cursor.execute("""
SELECT * FROM Top_Five_golfers_2017
""")
Top_5 = cursor.fetchall()

# storing all the column names from the tables 
labels = ['Player', 'NUMBER_OF_WINS', 'TOTAL_SG:PUTTING', 'AVG_Driving_DISTANCE', 'UP_AND_DOWN_%', 'FAIRWAY_HIT_%', 'GIR_RANK', 'HOLE_OUTS', 'SG:OTT', 'AVG_CLUB_HEAD_SPEED', 'TOTAL_3_PUTTS']
labelslst = ", ".join(f'"{label}"' for label in labels)
# creating a dataframe from the labels and data from Top_Five_golfers_2017
df_Top_5 = pd.DataFrame(Top_5, columns = labels )
for coulumn in df_Top_5:
    print(df_Top_5[coulumn].describe())
print(labelslst)

#querying all the data from golf_stats
cursor.execute(f"""
SELECT {labelslst} FROM golf_stats
""")
Comparison = cursor.fetchall()
print(Comparison)
# creating a dataframe from labels and the data from comparison_golfers
df_Comparison = pd.DataFrame(Comparison, columns = labels)
for coulumn in df_Comparison:
    print(df_Comparison[coulumn].describe())

# narrowed down the relavant data to answer my question and used the describe function from pandas to get analyze the data from both dataframes
print(df_Top_5['SG:OTT'].describe(), "Top 5 2017")
print(df_Comparison['SG:OTT'].describe(), "Comparison Golfers")
print(df_Top_5['TOTAL_SG:PUTTING'].describe(), "Top 5 2017")
print(df_Comparison['TOTAL_SG:PUTTING'].describe(), "Comparison Golfers")
print(df_Top_5['AVG_Driving_DISTANCE'].describe(), "Top 5 2017")
print(df_Comparison['AVG_Driving_DISTANCE'].describe(), "Comparison Golfers")
print(df_Comparison["FAIRWAY_HIT_%"].describe(), "Comparison Golfers")
print(df_Top_5['FAIRWAY_HIT_%'].describe(), "Top 5 2017")
print(df_Comparison['TOTAL_3_PUTTS'].describe(), "Comparison Golfers")
print(df_Top_5['TOTAL_3_PUTTS'].describe(), "Top 5 2017")

connection.close()