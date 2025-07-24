# GM HDW Analytics Dashboard

A Streamlit-powered analytics dashboard for GM vehicle hardware diagnostics. This tool processes and visualizes prescreened ECU data, highlighting the most frequent year/make/model/hardware combinations, common immobilizer and starting failures, and diagnostic trouble code (DTC) patterns.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 🚀 Features

### **Interactive Analytics**
- **Vehicle/Hardware Filtering**: Interactive sidebar with top 10 most frequent year/make/model/hardware combinations
- **Failure Pattern Detection**: Word-pair analysis for identifying common immobilizer and starting issues
- **DTC Analysis**: Diagnostic Trouble Code frequency analysis with percentage breakdowns
- **Real-time Metrics**: Live calculation of affected ECUs and failure percentages

### **Data Insights**
- **Standardization Analysis**: Identifies data quality issues across diagnostic fields
- **Symptom Recognition**: Automated detection of known failure patterns
- **Frequency Analysis**: Statistical breakdown of most common issues
- **Visual Charts**: Interactive bar charts and data tables

### **Key Findings**
The dashboard reveals:
1. **Data standardization issues** across three critical diagnostic fields:
   - `fs1_ecu_problems`: Inconsistent problem descriptions
   - `fs1_dtcs`: Varying DTC formatting and completeness
   - `resolution`: Non-standardized solution descriptions

2. **Hybrid Analysis Methodology** successfully identifies well-known immobilizer/starting failure patterns

## 📊 Dashboard Sections

### 1. Immobilizer/Starting Failures
- Prescreen cases count
- ECUs affected metrics
- Percentage of affected units
- Interactive failure pattern visualization

### 2. DTC Frequency Analysis
- Complete diagnostic trouble code breakdown
- Frequency percentages
- Pattern recognition for multiple fault scenarios

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Streamlit charts, Matplotlib
- **Deployment**: PyInstaller (standalone executable)
- **Pattern Matching**: Regular expressions for DTC extraction
- **Text Analysis**: Word-pair methodology for failure detection

## 📋 Prerequisites

- Python 3.7+
- Virtual environment (recommended)



## 🔍 Analysis Methodology

### Word-Pair Analysis
The dashboard uses a sophisticated word-pair methodology to identify failure patterns:
1. Text preprocessing (lowercasing, regex cleaning)
2. Word tokenization and pair generation
3. Frequency analysis against known symptom patterns
4. Statistical reporting with percentage calculations

### DTC Pattern Recognition
Uses regex patterns to extract and standardize diagnostic trouble codes:
- Pattern: `[PBCUpbcu]\d{3}[0-9A-Za-z]`
- Automatic case normalization
- Frequency analysis and ranking



## Author
<<<<<<< HEAD
Developed by [Weverson Barbieri de Oliveira](https://github.com/weversonbarbieri)


=======
Developed by [Weverson Barbieri de Oliveira]([text](https://github.com/weversonbarbieri))
>>>>>>> 2baf8ede45dcb8317b46d12de6a25f6cc64beb0c
