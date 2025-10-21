# analyzer.py
"""
Physiological Data Analyzer
Week 1 - Dummy Example. GitHub setup.
Week 2 – Algorithms & Data Handling: Implements moving average filtering, peak detection, and data export.
Week 3 – PDF report generation
"""

# Libraries to be imported:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# ---------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------
df = pd.read_csv("CBF.csv")
time = df["time_s"]
pressure = df["pressure_mmHg"]

# Check column names
#print("Columns in DataFrame:", df.columns)
#print(df.head())
print("✅ Data loaded.")

# Test Plot - Task Week01
plt.plot(
    time,
    pressure,
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
#plt.show()
print("✅ Raw data plotted.")

# ---------------------------------------------------------
# 2. Compute moving average and peaks
# ---------------------------------------------------------
window_size = 5  # adjust depending on sampling rate
df["pressure_smooth"] = pressure.rolling(window=window_size, center=True).mean()
print("✅ Moving Average Filter.")

# === Peak Detection ===
# Detect systolic (maxima)
systolic_peaks, _ = find_peaks(df["pressure_smooth"].fillna(0), distance=5)
# Detect diastolic (minima) by inverting the signal
diastolic_peaks, _ = find_peaks(-df["pressure_smooth"].fillna(0), distance=5)

print(f"✅ Found {len(systolic_peaks)} systolic and {len(diastolic_peaks)} diastolic peaks.")

# ---------------------------------------------------------
# 3. Save figure to CSV
# ---------------------------------------------------------
# === Create Results DataFrame ===
results = pd.DataFrame({
    "time_s": time,
    "pressure_mmHg": pressure,
    "pressure_smooth": df["pressure_smooth"]
})
results["is_systolic_peak"] = results.index.isin(systolic_peaks)
results["is_diastolic_peak"] = results.index.isin(diastolic_peaks)
results.to_csv("CBF_results.csv", index=False)
# === Save to CSV ===
print("✅ Results saved to CBF_results.csv")

# ---------------------------------------------------------
# 4. Plot full signal and zoomed region
# ---------------------------------------------------------
# === Full plot ===
plt.figure(figsize=(10, 5))
plt.plot(time, pressure, label="Raw Data", alpha=0.5)
plt.plot(time, df["pressure_smooth"], label="Smoothed", color="orange")

# Mark peaks
plt.scatter(time.iloc[systolic_peaks], df["pressure_smooth"].iloc[systolic_peaks],
            color="red", label="Systolic Peaks")
plt.scatter(time.iloc[diastolic_peaks], df["pressure_smooth"].iloc[diastolic_peaks],
            color="blue", label="Diastolic Peaks")

plt.xlabel("Time [s]")
plt.ylabel("Pressure [mmHg]")
plt.title("Blood Pressure with Systolic and Diastolic Peaks")
plt.legend()
plt.grid(True)
plt.tight_layout()
plot_full = "pressure_plot_full.png"
plt.savefig(plot_full, dpi=420)
plt.close()
print("✅ Full pressure plot saved.")

# === Zoomed plot ===
t_min, t_max = 50, 55
mask = (time >= t_min) & (time <= t_max)
systolic_in_mask = systolic_peaks[(time.iloc[systolic_peaks] >= t_min) & (time.iloc[systolic_peaks] <= t_max)]
diastolic_in_mask = diastolic_peaks[(time.iloc[diastolic_peaks] >= t_min) & (time.iloc[diastolic_peaks] <= t_max)]

plt.figure(figsize=(10, 5))
plt.plot(time[mask], pressure[mask], alpha=0.4, label="Raw Data")
plt.plot(time[mask], df["pressure_smooth"][mask], color="orange", label="Smoothed")

plt.scatter(time.iloc[systolic_in_mask], df["pressure_smooth"].iloc[systolic_in_mask],
            color="red", label="Systolic Peaks")
plt.scatter(time.iloc[diastolic_in_mask], df["pressure_smooth"].iloc[diastolic_in_mask],
            color="blue", label="Diastolic Peaks")
plt.xlabel("Time [s]")
plt.ylabel("Pressure [mmHg]")
plt.title(f"Zoomed-In Region ({t_min}s < t < {t_max}s)")
plt.legend()
plt.grid(True)
plt.xlim(t_min, t_max)  # enforce x-axis limits exactly
plt.tight_layout()
plot_zoom = "pressure_plot_zoom.png"
plt.savefig(plot_zoom, dpi=420)
plt.close()
print("✅ Zoomed plot saved.")

# ---------------------------------------------------------
# 5. Create PDF report
# ---------------------------------------------------------
pdf_filename = "Physiological_Report.pdf"
c = canvas.Canvas(pdf_filename, pagesize=A4)
width, height = A4

# === Header ===
c.setFont("Helvetica-Bold", 18)
c.drawString(2 * cm, height - 2.5 * cm, "Physiological Data Analysis Report")

# === Section title ===
c.setFont("Helvetica-Bold", 12)
c.drawString(2 * cm, height - 3.5 * cm, "Data report & Pressure-Time plot:")

# === Summary box ===
c.setFont("Helvetica", 12)
summary_y = height - 4.5 * cm
line_spacing = 0.6 * cm

summary_text = [
    f"Moving average window: {window_size}",
    f"Detected systolic peaks: {len(systolic_peaks)}",
    f"Detected diastolic peaks: {len(diastolic_peaks)}",
]

for i, line in enumerate(summary_text):
    c.drawString(2 * cm, summary_y - i * line_spacing, line)

# === Add main plot (centered, larger) ===
main_img_height = 9 * cm
main_img_y = summary_y - len(summary_text) * line_spacing - main_img_height + 0.25 * cm
c.drawImage(ImageReader(plot_full), 2 * cm, main_img_y, width - 4 * cm, main_img_height, preserveAspectRatio=True)

# === Section title for zoomed plot ===
zoom_title_y = main_img_y - 1 * cm
c.setFont("Helvetica-Bold", 12)
c.drawString(2 * cm, zoom_title_y, "Example Zoomed Region (50s–55s):")

# === Add zoomed plot below ===
zoom_img_height = 9 * cm
zoom_img_y = zoom_title_y - zoom_img_height - 0.3 * cm
c.drawImage(ImageReader(plot_zoom), 2 * cm, zoom_img_y, width - 4 * cm, zoom_img_height, preserveAspectRatio=True)

# === Footer ===
c.setFont("Helvetica-Oblique", 9)
c.setFillGray(0.3)
footer_text = "Rate & Download the free-access project on GitHub: https://github.com/querol22/DataAnalyzerWarmUp"
c.drawRightString(width - 2 * cm, 1.5 * cm, footer_text)

# === Save PDF ===
c.save()
print(f"✅ Report generated: {pdf_filename}")