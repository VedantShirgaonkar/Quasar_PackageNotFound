import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("quizgenius.db")

# Load CSV into a DataFrame
df = pd.read_csv("questions.csv")

# Write DataFrame to SQLite table
df.to_sql("questions", conn, if_exists="replace", index=False)

# Close the connection
conn.close()
