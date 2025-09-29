# analyzer.py
"""
A simple warm-up script for data analysis.
"""

# Libraries to be imported:
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("bp_Testdata.csv")

#print("Columns in DataFrame:", df.columns)
#print(df.head())

# Plot
plt.plot(df["time_s"], df["pressure_mmHg"], marker="o", linestyle="-")
plt.xlabel("Time [s]")
plt.ylabel("Pressure [mmHg]")
plt.title("Blood Pressure Over Time")
plt.grid(True)
plt.show()
