# 🧠 DataAnalyzerWarmUp

A compact physiological data analysis tool built in **Python** — part of a 4-week simulation warm-up series.  
The tool loads experimental cerebral blood flow (CBF) data, smooths the signal, detects systolic/diastolic peaks, and automatically generates a professional **PDF report** with annotated plots.

---

## 📅 Weekly Progress Overview

### **Week 1 – Data Setup**
- Added raw CBF pressure data (`CBF.csv`).
- Displays baseline cerebral blood pressure response with transient step increases at 100 s and 200 s.
- **Result:** `Results_00_RawData.png`

### **Week 2 – Signal Processing**
- Implemented moving-average smoothing and systolic/diastolic peak detection.
- Added CSV export of filtered data.
- **Results:**  
  - `Results_01_SmoothData.png`  
  - `CBF_results.csv`

### **Week 3 – Automated Reporting**
- Integrated **ReportLab** for PDF generation.
- Added **zoomed region (50 s–55 s)** visualization.
- **Result:** `Physiological_Report.pdf`

---

## 🧰 Features

- 🩸 Automatic signal smoothing and peak detection  
- 📈 Matplotlib-based visualizations  
- 📄 PDF report generation with embedded plots  
- 💾 CSV export of processed signals  
- ⚙️ Adjustable moving average window & zoom regions  

---

## 🧪 Usage

```bash
# Clone repository
git clone https://github.com/querol22/DataAnalyzerWarmUp.git
cd DataAnalyzerWarmUp

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run analysis
python src/analyzer.py
