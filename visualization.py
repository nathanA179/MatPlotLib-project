import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import os
import seaborn as sns

# connected the data tables to this file 
basedir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(basedir, "data/golf_stats.db")
connection = sql.connect("data/golf_stats.db")
cursor = connection.cursor()

# querying all the data Top_Five_Golfers_2017
df_Top_5 = pd.read_sql_query(
    "SELECT * FROM Top_Five_Golfers_2017", connection
)
# querying all the data golf_stats
df_stats  = pd.read_sql_query(
        "SELECT * FROM golf_stats", connection)

# calculating the correlation between strokes gained putting to wins and strokes gained on the tee to wins from the top 5 golfers 
corr_Top5_PUTTING = df_Top_5["TOTAL_SG:PUTTING"].corr(df_Top_5["NUMBER_OF_WINS"])
corr_Top5_OTT = df_Top_5["SG:OTT"].corr(df_Top_5["NUMBER_OF_WINS"])

# calculating the correlation between strokes gained putting to wins and strokes gained on the tee to wins from all the golfers 
corr_comparison_PUTTING = df_stats["TOTAL_SG:PUTTING"].corr(df_stats["NUMBER_OF_WINS"])
corr_comparison_OTT = df_stats["SG:OTT"].corr(df_stats["NUMBER_OF_WINS"])

#printing all the correlation values 
print(corr_Top5_PUTTING)
print(corr_Top5_OTT)
print(corr_comparison_PUTTING)
print(corr_comparison_OTT)
# variable stores the column names from the tabels 
catorgies = ["SG:OTT", "TOTAL_SG:PUTTING", "NUMBER_OF_WINS"]


# creating a heatmap to visualize the correlations for all the golfers 
plt.figure(figsize = (14,10))
corr1 = df_stats[catorgies].corr()
sns.heatmap(corr1, annot = True, cmap = "binary",
fmt = ".3f",
xticklabels = catorgies,
yticklabels = catorgies)
plt.title("Strokes Gained to Wins(Aggregate)")
plt.show()

# creating a heatmap to visualize the correlations for all the top 5 golfers 
plt.figure(figsize = (14,10))
corr2 = df_Top_5[catorgies].corr()
sns.heatmap(corr2, annot = True, cmap = "binary",
fmt = ".3f",
xticklabels = catorgies,
yticklabels = catorgies)
plt.title("Strokes Gained to Wins(Top 5)")
plt.show()

