"""
Physiological Data Analyzer
-------------------------------------------------
Week 1 - Dummy Example. GitHub setup.
Week 2 – Algorithms & Data Handling: Implements moving average filtering, peak detection, and data export.
Week 3 – PDF report generation
Week 4 - Final refinements
-------------------------------------------------
"""

# Libraries to be imported:
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from dataclasses import dataclass

# =========================================================
# 1. CONFIGURATION
# =========================================================
@dataclass
class Config:
    input_csv: str = "data/CBF.csv"
    results_csv: str = "Results/CBF_results.csv"
    plot_full: str = "Results/pressure_plot_full.png"
    plot_zoom: str = "Results/pressure_plot_zoom.png"
    pdf_report: str = "Results/Physiological_Report.pdf"
    window_size: int = 5
    zoom_t_min: float = 50.0
    zoom_t_max: float = 55.0
    peak_distance: int = 5
    # create folders if not exist
    def ensure_dirs(self):
        for p in ("data", "Results"):
            if not os.path.isdir(p):
                os.makedirs(p, exist_ok=True)

# =========================================================
# 2. DATA PROCESSING
# =========================================================
def load_data(file_path):
    """Load CSV into pandas DataFrame and return it."""
    df = pd.read_csv(file_path)
    print(f"✅ Data loaded: {df.shape[0]} samples, columns: {list(df.columns)}")
    return df

def smooth_signal(df, window_size):
    """Apply a centered moving average."""
    df["pressure_smooth"] = (
        df["pressure_mmHg"].rolling(window=window_size, center=True).mean()
    )
    print(f"✅ Moving average applied (window={window_size})")
    return df

def detect_peaks(df, distance):
    """Detect systolic and diastolic peaks."""
    y = df["pressure_smooth"].fillna(0)
    systolic_peaks, _ = find_peaks(y, distance=distance)
    diastolic_peaks, _ = find_peaks(-y, distance=distance)
    print(f"✅ Found {len(systolic_peaks)} systolic and {len(diastolic_peaks)} diastolic peaks.")
    return systolic_peaks, diastolic_peaks

def save_results(df, systolic_peaks, diastolic_peaks, output_csv):
    """Save processed results."""
    df_out = df.copy()
    df_out["is_systolic_peak"] = df.index.isin(systolic_peaks)
    df_out["is_diastolic_peak"] = df.index.isin(diastolic_peaks)
    df_out.to_csv(output_csv, index=False)
    print(f"✅ Results saved to {output_csv}")

# =========================================================
# 3. PLOTTING
# =========================================================
def save_full_plot(df, systolic_peaks, diastolic_peaks, path):
    time = df["time_s"]
    pressure = df["pressure_mmHg"]

    plt.figure(figsize=(10, 5))
    plt.plot(time, pressure, alpha=0.4, label="Raw Data")
    plt.plot(time, df["pressure_smooth"], color="orange", label="Smoothed")
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
    plt.savefig(path, dpi=420)
    plt.close()
    print(f"✅ Full plot saved to {path}")


def save_zoom_plot(df, systolic_peaks, diastolic_peaks, path, t_min, t_max):
    time = df["time_s"]
    pressure = df["pressure_mmHg"]
    mask = (time >= t_min) & (time <= t_max)

    systolic_in = systolic_peaks[(time.iloc[systolic_peaks] >= t_min) & (time.iloc[systolic_peaks] <= t_max)]
    diastolic_in = diastolic_peaks[(time.iloc[diastolic_peaks] >= t_min) & (time.iloc[diastolic_peaks] <= t_max)]

    plt.figure(figsize=(10, 5))
    plt.plot(time[mask], pressure[mask], alpha=0.4, label="Raw Data")
    plt.plot(time[mask], df["pressure_smooth"][mask], color="orange", label="Smoothed")
    plt.scatter(time.iloc[systolic_in], df["pressure_smooth"].iloc[systolic_in],
                color="red", label="Systolic Peaks")
    plt.scatter(time.iloc[diastolic_in], df["pressure_smooth"].iloc[diastolic_in],
                color="blue", label="Diastolic Peaks")
    plt.xlabel("Time [s]")
    plt.ylabel("Pressure [mmHg]")
    plt.title(f"Zoomed Region ({t_min}s–{t_max}s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xlim(t_min, t_max)
    plt.savefig(path, dpi=420)
    plt.close()
    print(f"✅ Zoomed plot saved to {path}")

# =========================================================
# 4. PDF REPORT
# =========================================================
def create_pdf_report(cfg, systolic_peaks, diastolic_peaks):
    c = canvas.Canvas(cfg.pdf_report, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, height - 2.5 * cm, "Physiological Data Analysis Report")

    # Summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, height - 3.5 * cm, "Summary:")
    c.setFont("Helvetica", 12)

    summary_y = height - 4.5 * cm
    line_spacing = 0.6 * cm

    summary = [
        f"Moving average window: {cfg.window_size}",
        f"Systolic peaks: {len(systolic_peaks)}",
        f"Diastolic peaks: {len(diastolic_peaks)}",
    ]
    for i, line in enumerate(summary):
        c.drawString(2 * cm, summary_y - i * line_spacing, line)
        #c.drawString(2 * cm, height - (4.5 + i * 0.6) * cm, line)

    # === Add main plot (centered, larger) ===
    main_img_height = 9 * cm
    main_img_y = summary_y - len(summary) * line_spacing - main_img_height + 0.25 * cm
    c.drawImage(ImageReader(cfg.plot_full), 2 * cm, main_img_y, width - 4 * cm, main_img_height, preserveAspectRatio=True)
#    c.drawImage(ImageReader(cfg.plot_full), 2 * cm, 9 * cm, width - 4 * cm, 8 * cm, preserveAspectRatio=True)

    # === Section title for zoomed plot ===
    zoom_title_y = main_img_y - 1 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, zoom_title_y, "Example Zoomed Region (50s–55s):")

    # === Add zoomed plot below ===
    zoom_img_height = 9 * cm
    zoom_img_y = zoom_title_y - zoom_img_height - 0.3 * cm
    c.drawImage(ImageReader(cfg.plot_zoom), 2 * cm, zoom_img_y, width - 4 * cm, zoom_img_height, preserveAspectRatio=True)

    # === Footer ===
    c.setFont("Helvetica-Oblique", 9)
    c.setFillGray(0.3)
    c.drawRightString(width - 2 * cm, 1.5 * cm,
                      "Project: https://github.com/querol22/DataAnalyzerWarmUp")

    # === Save PDF ===
    c.save()
    print(f"✅ PDF report generated: {cfg.pdf_report}")

# =========================================================
# 5. MAIN PIPELINE
# =========================================================
def main(cfg: Config):
    cfg.ensure_dirs()
    df = load_data(cfg.input_csv)
    df = smooth_signal(df, cfg.window_size)
    systolic_peaks, diastolic_peaks = detect_peaks(df, cfg.peak_distance)
    save_results(df, systolic_peaks, diastolic_peaks, cfg.results_csv)
    save_full_plot(df, systolic_peaks, diastolic_peaks, cfg.plot_full)
    save_zoom_plot(df, systolic_peaks, diastolic_peaks, cfg.plot_zoom,
                   cfg.zoom_t_min, cfg.zoom_t_max)
    create_pdf_report(cfg, systolic_peaks, diastolic_peaks)
    print("🎯 Data analysis and report generation completed successfully!")


if __name__ == "__main__":
    cfg = Config()
    main(cfg)