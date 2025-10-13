# analyzer.py
"""
Physiological Data Analyzer
Week 2 – Algorithms & Data Handling
Implements moving average filtering, peak detection, and data export.
"""

# Libraries to be imported:
import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
from scipy.signal import find_peaks

# Load data
df = pd.read_csv("CBF.csv")
print("✅ Data loaded.")

#print("Columns in DataFrame:", df.columns)
#print(df.head())

# Plot
plt.plot(
    df["time_s"],
    df["pressure_mmHg"],
    marker="o",
    markerfacecolor="black",   # fill color of markers
    markeredgecolor="red",   # border color of markers
    linestyle="-",
    color="blue"            # line color
)
plt.xlabel("Time [s]")
plt.ylabel("Pressure [mmHg]")
plt.title("Blood Pressure Over Time")
plt.grid(True)
plt.show()

print("✅ Raw data plotted.")

# === Moving Average Filter ===
window_size = 3  # adjust depending on sampling rate
df["pressure_smooth"] = df["pressure_mmHg"].rolling(window=window_size, center=True).mean()
print("✅ Moving Average Filter.")

# === Peak Detection ===
# Detect systolic (maxima)
systolic_peaks, _ = find_peaks(df["pressure_smooth"].fillna(0), distance=5)
# Detect diastolic (minima) by inverting the signal
diastolic_peaks, _ = find_peaks(-df["pressure_smooth"].fillna(0), distance=5)
print("✅ Peak Detection.")

# === Create Results DataFrame ===
results = pd.DataFrame({
    "time_s": df["time_s"],
    "pressure_mmHg": df["pressure_mmHg"],
    "pressure_smooth": df["pressure_smooth"]
})
results["is_systolic_peak"] = results.index.isin(systolic_peaks)
results["is_diastolic_peak"] = results.index.isin(diastolic_peaks)
print("✅ Create Results DataFrame.")

# === Save to CSV ===
results.to_csv("CBF_results.csv", index=False)
print("✅ Results saved to CBF_results.csv")

# === Plot ===
plt.figure(figsize=(10, 5))
plt.plot(df["time_s"], df["pressure_mmHg"], label="Raw Data", alpha=0.5)
plt.plot(df["time_s"], df["pressure_smooth"], label="Smoothed", color="orange")

# Mark peaks
plt.scatter(df["time_s"].iloc[systolic_peaks], df["pressure_smooth"].iloc[systolic_peaks],
            color="red", label="Systolic Peaks")
plt.scatter(df["time_s"].iloc[diastolic_peaks], df["pressure_smooth"].iloc[diastolic_peaks],
            color="blue", label="Diastolic Peaks")

plt.xlabel("Time [s]")
plt.ylabel("Pressure [mmHg]")
plt.title("Blood Pressure with Systolic and Diastolic Peaks")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
print("✅ Smoothed data plotted.")